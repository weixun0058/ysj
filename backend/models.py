from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Text # 导入 Text 类型用于较长内容
import re

# 创建 SQLAlchemy 和 Migrate 实例，但不关联 app
db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) # 调整长度以适应更强的哈希
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False, nullable=False) # 添加管理员标志字段
    # 添加用户与地址的一对多关系
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        # 使用 Werkzeug 生成密码哈希
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # 使用 Werkzeug 校验密码哈希
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>' 

# --- 新增：地址模型 ---
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