from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Text # 导入 Text 类型用于较长内容
import re
import json

# 创建 SQLAlchemy 和 Migrate 实例，但不关联 app
db = SQLAlchemy()
migrate = Migrate()

class SlugMixin:
    """提供slug生成和管理功能的混合类"""
    
    @staticmethod
    def generate_slug(text):
        """根据文本生成URL友好的slug"""
        if not text:
            return 'item'
        # 使用现有的create_slug函数
        return create_slug(text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=True)  # 修改为非必填
    phone = db.Column(db.String(20), index=True, unique=True, nullable=False)  # 添加手机号码为必填字段
    password_hash = db.Column(db.String(256)) # 调整长度以适应更强的哈希
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False, nullable=False) # 添加管理员标志字段
    # 新增基本信息字段
    gender = db.Column(db.String(10), nullable=True)  # 性别：男/女/保密
    birthday = db.Column(db.Date, nullable=True)  # 生日
    real_name = db.Column(db.String(50), nullable=True)  # 真实姓名
    # 会员相关
    member_level_id = db.Column(db.Integer, db.ForeignKey('member_level.id'), nullable=True)
    points = db.Column(db.Integer, default=0)  # 积分
    total_spend = db.Column(db.Float, default=0.0)  # 累计消费金额
    last_login = db.Column(db.DateTime, nullable=True)  # 最后登录时间
    
    # 关系定义
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    custom_fields = db.relationship('UserCustomField', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    points_records = db.relationship('PointsRecord', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    coupons = db.relationship('UserCoupon', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    member_level = db.relationship('MemberLevel', backref='users')

    def set_password(self, password):
        # 使用 Werkzeug 生成密码哈希
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # 使用 Werkzeug 校验密码哈希
        return check_password_hash(self.password_hash, password)

    def get_custom_fields(self):
        """获取用户自定义字段"""
        fields = {}
        for field in self.custom_fields:
            fields[field.field_key] = field.field_value
        return fields
    
    def set_custom_field(self, key, value):
        """设置用户自定义字段"""
        field = UserCustomField.query.filter_by(user_id=self.id, field_key=key).first()
        if field:
            field.field_value = value
        else:
            field = UserCustomField(user_id=self.id, field_key=key, field_value=value)
            db.session.add(field)

    def add_points(self, points, description=""):
        """添加积分并记录"""
        self.points += points
        record = PointsRecord(
            user_id=self.id,
            points=points,
            balance=self.points,
            description=description
        )
        db.session.add(record)
        return record

    def __repr__(self):
        return f'<User {self.username}>'

# 用户自定义字段表 - 用于动态扩展用户属性
class UserCustomField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    field_key = db.Column(db.String(50), nullable=False)  # 字段名
    field_value = db.Column(db.Text)  # 字段值
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'field_key', name='user_field_key_unique'),)
    
    def __repr__(self):
        return f'<UserCustomField {self.field_key}={self.field_value[:20]}>'

# 用户字段定义表 - 用于在后台管理界面定义可用的自定义字段
class UserFieldDefinition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_key = db.Column(db.String(50), unique=True, nullable=False)  # 字段键名
    field_name = db.Column(db.String(100), nullable=False)  # 字段显示名称
    field_type = db.Column(db.String(20), nullable=False)  # 字段类型：text, number, date, select等
    is_required = db.Column(db.Boolean, default=False)  # 是否必填
    is_visible = db.Column(db.Boolean, default=True)  # 是否在前端显示
    display_order = db.Column(db.Integer, default=0)  # 显示顺序
    options = db.Column(db.Text, nullable=True)  # 选项值，JSON格式，用于select类型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_options(self):
        """获取字段选项列表"""
        if self.options and self.field_type in ['select', 'radio', 'checkbox']:
            try:
                return json.loads(self.options)
            except:
                return []
        return []
    
    def set_options(self, options_list):
        """设置字段选项列表"""
        if isinstance(options_list, list):
            self.options = json.dumps(options_list)
    
    def __repr__(self):
        return f'<UserFieldDefinition {self.field_name}>'

# 会员等级表
class MemberLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 等级名称
    description = db.Column(db.String(255))  # 等级描述
    min_points = db.Column(db.Integer, default=0)  # 所需最小积分
    min_spend = db.Column(db.Float, default=0.0)  # 所需最小消费金额
    discount_rate = db.Column(db.Float, default=1.0)  # 折扣率，1.0表示无折扣
    icon_url = db.Column(db.String(255))  # 等级图标
    benefits = db.Column(db.Text)  # 会员权益，JSON格式
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_benefits(self):
        """获取会员权益列表"""
        if self.benefits:
            try:
                return json.loads(self.benefits)
            except:
                return []
        return []
    
    def set_benefits(self, benefits_list):
        """设置会员权益列表"""
        if isinstance(benefits_list, list):
            self.benefits = json.dumps(benefits_list)
    
    def __repr__(self):
        return f'<MemberLevel {self.name}>'

# 积分记录表
class PointsRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)  # 变动积分数(正数为增加，负数为减少)
    balance = db.Column(db.Integer, nullable=False)  # 变动后余额
    description = db.Column(db.String(255))  # 变动描述
    source_type = db.Column(db.String(50))  # 来源类型：消费、活动、兑换等
    source_id = db.Column(db.Integer)  # 来源ID，如订单ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PointsRecord {self.points} for User {self.user_id}>'

# 优惠券定义表
class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # 优惠码
    name = db.Column(db.String(100), nullable=False)  # 优惠券名称
    type = db.Column(db.String(20), nullable=False)  # 类型：满减、折扣、直减等
    discount_value = db.Column(db.Float, nullable=False)  # 折扣值，根据type解释
    min_purchase = db.Column(db.Float, default=0.0)  # 最低消费
    start_date = db.Column(db.DateTime, nullable=False)  # 生效日期
    end_date = db.Column(db.DateTime, nullable=False)  # 过期日期
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    max_uses = db.Column(db.Integer, default=0)  # 最大使用次数，0为不限
    current_uses = db.Column(db.Integer, default=0)  # 当前使用次数
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_coupons = db.relationship('UserCoupon', backref='coupon', lazy='dynamic')
    
    def is_valid(self):
        """检查优惠券是否有效"""
        now = datetime.utcnow()
        is_date_valid = self.start_date <= now <= self.end_date
        is_usage_valid = self.max_uses == 0 or self.current_uses < self.max_uses
        return self.is_active and is_date_valid and is_usage_valid
    
    def __repr__(self):
        return f'<Coupon {self.name}>'

# 用户优惠券关联表
class UserCoupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'), nullable=False)
    is_used = db.Column(db.Boolean, default=False)  # 是否已使用
    used_at = db.Column(db.DateTime)  # 使用时间
    order_id = db.Column(db.Integer)  # 使用的订单ID
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)  # 获取时间
    
    def __repr__(self):
        return f'<UserCoupon {self.id}>'

# --- 地址模型 ---
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    detailed_address = db.Column(db.String(255), nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Address {self.id} for User {self.user_id}>'
# --- 地址模型结束 ---

def create_slug(text):
    """根据文本生成 URL 友好的 slug"""
    # 移除 & 符号，因为它在 URL 中有特殊含义
    text = text.replace('&', 'and')
    # 保持中文，但处理特殊字符和空格
    text = re.sub(r'[^\w\s-]', '', text).strip().lower() # 移除大部分非字母数字空格连字符
    text = re.sub(r'[-\s]+', '-', text) # 将空格和多个连字符替换为单个连字符
    return text

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), index=True, unique=True, nullable=False)
    content = db.Column(Text, nullable=False) # 使用 Text 类型存储文章内容
    publish_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True, index=True)
    # 可选: 作者关联
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = db.relationship('User', backref=db.backref('news_articles', lazy=True))

    def __init__(self, title, content, **kwargs):
        super(NewsArticle, self).__init__(title=title, content=content, **kwargs)
        if not self.slug: # 如果创建时没有提供 slug，则根据标题自动生成
            self.slug = create_slug(self.title)
            # 检查 slug 是否唯一，如果不唯一则添加后缀 (简单处理)
            original_slug = self.slug
            counter = 1
            while NewsArticle.query.filter_by(slug=self.slug).first():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

    def __repr__(self):
        return f'<NewsArticle {self.title[:50]}>'

# --- 产品分类模型 ---
class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(255))
    
    # 父子分类关系
    parent_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=True)
    parent = db.relationship('ProductCategory', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    
    # 关联产品 - 只在一侧定义backref
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    # 其他元数据
    display_order = db.Column(db.Integer, default=0)  # 用于排序
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, **kwargs):
        super(ProductCategory, self).__init__(name=name, **kwargs)
        if not kwargs.get('slug'):
            self.slug = create_slug(name)
            
    @property
    def is_leaf(self):
        """检查是否为叶子分类（无子分类）"""
        return self.children.count() == 0
    
    @property
    def breadcrumbs(self):
        """获取分类的面包屑路径"""
        result = []
        current = self
        while current:
            result.insert(0, {'id': current.id, 'name': current.name, 'slug': current.slug})
            current = current.parent
        return result
    
    def __repr__(self):
        return f'<ProductCategory {self.name}>'

# 产品和标签的关联表（多对多）
product_tag = db.Table('product_tag_relation',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('product_tag.id'), primary_key=True)
)

# 产品标签模型
class ProductTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(60), nullable=False, unique=True, index=True)
    
    def __init__(self, name, **kwargs):
        super(ProductTag, self).__init__(name=name, **kwargs)
        if not kwargs.get('slug'):
            self.slug = create_slug(name)
    
    def __repr__(self):
        return f'<ProductTag {self.name}>'

# 产品模型
class Product(db.Model, SlugMixin):
    """产品模型"""
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(150), unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)  # 是否为精选产品
    images = db.Column(db.JSON, nullable=True)  # 存储多个图片路径的JSON数组
    warning_stock = db.Column(db.Integer, default=10)  # 库存预警阈值
    
    # 外键和关系 - 移除这里的backref，因为已经在ProductCategory中定义
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id', ondelete='SET NULL'), nullable=True)
    
    # 标签关联
    tags = db.relationship('ProductTag', secondary=product_tag, 
                          backref=db.backref('products', lazy='dynamic'))
    
    # 库存关系
    stock = db.relationship("ProductStock", uselist=False, back_populates="product", 
                          cascade="all, delete-orphan")
    
    # 库存日志关系
    stock_logs = db.relationship("StockLog", back_populates="product", cascade="all, delete-orphan")
    
    # 有效库存属性
    @property
    def effective_stock(self):
        """有效库存 = 可用库存 - 预扣库存"""
        if self.stock:
            return self.stock.available_stock - self.stock.prelock_stock
        return 0
        
    @property
    def stock_status(self):
        """库存状态：0=无库存，1=库存警告，2=库存充足"""
        if not self.stock or self.effective_stock <= 0:
            return 0  # 无库存
        elif self.effective_stock <= self.warning_stock:
            return 1  # 库存警告
        else:
            return 2  # 库存充足
    
    def __init__(self, name, price, **kwargs):
        """
        初始化产品
        :param name: 产品名称
        :param price: 产品价格
        :param kwargs: 其他参数
        """
        self.name = name
        self.price = price
        self.slug = create_slug(name)  # 使用已定义的create_slug函数
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def to_dict(self, include_stock=True):
        """转换为字典"""
        result = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': float(self.price),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_featured': self.is_featured,
            'images': self.images,
            'warning_stock': self.warning_stock,
            'category_id': self.category_id,
            'category': self.category.name if self.category else None,
        }
        
        # 包含库存数据
        if include_stock and self.stock:
            result.update({
                'total_stock': self.stock.total_stock,
                'available_stock': self.stock.available_stock,
                'prelock_stock': self.stock.prelock_stock,
                'effective_stock': self.effective_stock,
                'stock_status': self.stock_status
            })
        
        return result

class ProductStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, unique=True)
    total_stock = db.Column(db.Integer, nullable=False, default=0) # 总库存
    available_stock = db.Column(db.Integer, nullable=False, default=0) # 可用库存
    prelock_stock = db.Column(db.Integer, nullable=False, default=0) # 预扣库存 (下单未支付)

    # 与Product的关系 - 添加back_populates
    product = db.relationship("Product", back_populates="stock")

    # 检查库存非负约束
    __table_args__ = (
        db.CheckConstraint('total_stock >= 0', name='check_total_stock_non_negative'),
        db.CheckConstraint('available_stock >= 0', name='check_available_stock_non_negative'),
        db.CheckConstraint('prelock_stock >= 0', name='check_prelock_stock_non_negative'),
        db.CheckConstraint('available_stock + prelock_stock <= total_stock', name='check_stock_logic')
    )

    def __repr__(self):
        return f'<ProductStock product_id={self.product_id}, available={self.available_stock}>'


class StockLog(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    change_type = db.Column(db.SmallInteger, nullable=False) # 1:下单预扣, 2:支付确认, 3:取消/超时释放, 4:后台修改
    change_amount = db.Column(db.Integer, nullable=False) # 正数增加，负数减少 (相对于 available_stock 或 total_stock)
    # 可以增加 pre_available, post_available 等字段记录变动前后状态
    order_id = db.Column(db.String(50), nullable=True) # 关联的订单号 (可选)
    admin_id = db.Column(db.Integer, nullable=True) # 操作管理员ID (可选, 用于后台修改)
    remark = db.Column(db.String(200), nullable=True) # 备注
    created_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # 新增操作类型字段（用于区分不同的操作来源）
    operation_type = db.Column(db.String(20), nullable=True)  # admin_adjust, order_create, payment_confirm, order_cancel
    
    # 新增库存变动前数据记录
    before_total = db.Column(db.Integer, nullable=True)  # 变动前总库存
    before_available = db.Column(db.Integer, nullable=True)  # 变动前可用库存
    before_prelock = db.Column(db.Integer, nullable=True)  # 变动前预扣库存
    
    # 兼容旧字段别名
    @property
    def reason(self):
        return self.remark
        
    @reason.setter
    def reason(self, value):
        self.remark = value

    # 关联 Product (可选，方便查询)
    product = db.relationship('Product', back_populates="stock_logs")
            
    def __repr__(self):
        return f'<StockLog {self.log_id} product_id={self.product_id} type={self.change_type} amount={self.change_amount}>' 

# 添加品牌联名合作相关的模型

class BrandCollaboration(db.Model):
    """品牌联名合作申请表"""
    __tablename__ = 'brand_collaborations'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)  # 公司/品牌名称
    industry = db.Column(db.String(50), nullable=False)  # 行业
    contact_name = db.Column(db.String(50), nullable=False)  # 联系人姓名
    position = db.Column(db.String(50))  # 职位
    email = db.Column(db.String(100), nullable=False)  # 邮箱
    phone = db.Column(db.String(20), nullable=False)  # 电话
    product_types = db.Column(db.Text)  # 合作产品类型 (JSON存储)
    cooperation_type = db.Column(db.String(50))  # 合作类型
    expected_volume = db.Column(db.String(50))  # 预期年合作额度
    expected_start_date = db.Column(db.String(50))  # 预期开始日期
    details = db.Column(db.Text)  # 合作详情
    status = db.Column(db.String(20), default='pending')  # 状态: pending, processing, approved, rejected, completed
    is_priority = db.Column(db.Boolean, default=False)  # 是否优先级
    admin_notes = db.Column(db.Text)  # 管理员备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联的项目
    projects = db.relationship('CollaborationProject', backref='collaboration', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BrandCollaboration {self.company_name}>'

class CollaborationProject(db.Model):
    """联名合作项目表"""
    __tablename__ = 'collaboration_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    collaboration_id = db.Column(db.Integer, db.ForeignKey('brand_collaborations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # 项目名称
    description = db.Column(db.Text)  # 项目描述
    start_date = db.Column(db.Date)  # 开始日期
    end_date = db.Column(db.Date)  # 结束日期
    budget = db.Column(db.Float)  # 预算
    profit_share_model = db.Column(db.String(50))  # 利润分成模式
    profit_share_percentage = db.Column(db.Float)  # 利润分成比例
    status = db.Column(db.String(20), default='planning')  # 状态: planning, active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联的产品和活动
    products = db.relationship('CollaborationProduct', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    activities = db.relationship('CollaborationActivity', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CollaborationProject {self.name}>'

class CollaborationProduct(db.Model):
    """联名合作产品表"""
    __tablename__ = 'collaboration_products'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('collaboration_projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # 产品名称
    product_code = db.Column(db.String(50))  # 产品编码
    description = db.Column(db.Text)  # 产品描述
    specifications = db.Column(db.Text)  # 规格
    pricing = db.Column(db.Float)  # 定价
    cost = db.Column(db.Float)  # 成本
    launch_date = db.Column(db.Date)  # 上市日期
    status = db.Column(db.String(20), default='draft')  # 状态
    design_files = db.Column(db.Text)  # 设计文件路径 (JSON存储)
    images = db.Column(db.Text)  # 产品图片路径 (JSON存储)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CollaborationProduct {self.name}>'

class CollaborationActivity(db.Model):
    """联名合作营销活动表"""
    __tablename__ = 'collaboration_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('collaboration_projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # 活动名称
    description = db.Column(db.Text)  # 活动描述
    start_date = db.Column(db.Date)  # 开始日期
    end_date = db.Column(db.Date)  # 结束日期
    budget = db.Column(db.Float)  # 预算
    channels = db.Column(db.Text)  # 营销渠道 (JSON存储)
    target_audience = db.Column(db.Text)  # 目标受众
    kpis = db.Column(db.Text)  # KPI指标 (JSON存储)
    results = db.Column(db.Text)  # 结果数据 (JSON存储)
    status = db.Column(db.String(20), default='planned')  # 状态
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CollaborationActivity {self.name}>' 