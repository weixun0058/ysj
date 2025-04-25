# backend/user_routes.py
from flask import Blueprint, jsonify, request, abort
from models import db, User, Address, UserCustomField, UserFieldDefinition, MemberLevel, PointsRecord, UserCoupon, Coupon
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash # 用于更新密码
from functools import wraps
from sqlalchemy import or_
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api')

# --- 权限检查装饰器 (示例) ---
def admin_required(fn):
    """装饰器：检查 JWT 身份是否为管理员"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 手动验证JWT
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "未提供有效的认证令牌"}), 401
            
        try:
            # 手动获取用户身份
            from flask_jwt_extended import decode_token
            token = auth_header.split(' ')[1]
            decoded_token = decode_token(token)
            current_user_id = decoded_token['sub']
            
            # 检查管理员权限
            user = User.query.get(current_user_id)
            if not user or not user.is_admin:
                return jsonify({"error": "管理员权限不足"}), 403
                
            # 验证通过，执行原函数
            return fn(*args, **kwargs)
        except Exception as e:
            # 处理验证失败的情况
            import sys
            print(f"[DEBUG] Admin验证失败: {str(e)}", file=sys.stderr)
            return jsonify({"error": "认证验证失败"}), 401
    return wrapper

# --- 序列化函数 (简化示例) ---
def serialize_user(user: User, include_email=False, include_details=False, include_custom_fields=False):
    """将 User 对象序列化为字典 (增强版)"""
    data = {
        'id': user.id,
        'username': user.username,
        'phone': user.phone,
        'created_at': user.created_at.isoformat(),
        'is_admin': user.is_admin
    }
    
    if include_email and user.email:
        data['email'] = user.email
    
    if include_details:
        # 添加基本信息字段
        data['gender'] = user.gender
        data['real_name'] = user.real_name
        data['birthday'] = user.birthday.isoformat() if user.birthday else None
        
        # 添加会员信息
        data['points'] = user.points
        data['total_spend'] = user.total_spend
        data['last_login'] = user.last_login.isoformat() if user.last_login else None
        
        # 包含会员等级
        if user.member_level:
            data['member_level'] = {
                'id': user.member_level.id,
                'name': user.member_level.name,
                'discount_rate': user.member_level.discount_rate
            }
    
    # 包含自定义字段
    if include_custom_fields:
        data['custom_fields'] = user.get_custom_fields()
        
    return data

def serialize_address(address: Address):
    """将 Address 对象序列化为字典"""
    return {
        'id': address.id,
        'user_id': address.user_id,
        'recipient_name': address.recipient_name,
        'phone_number': address.phone_number,
        'province': address.province,
        'city': address.city,
        'district': address.district,
        'detailed_address': address.detailed_address,
        'is_default': address.is_default,
        'created_at': address.created_at.isoformat(),
        'updated_at': address.updated_at.isoformat()
    }

def serialize_user_field_definition(field_def: UserFieldDefinition):
    """将用户字段定义序列化"""
    data = {
        'id': field_def.id,
        'field_key': field_def.field_key,
        'field_name': field_def.field_name,
        'field_type': field_def.field_type,
        'is_required': field_def.is_required,
        'is_visible': field_def.is_visible,
        'display_order': field_def.display_order
    }
    
    # 添加选项（如果有）
    if field_def.options:
        data['options'] = field_def.get_options()
    
    return data

def serialize_points_record(record: PointsRecord):
    """将积分记录序列化"""
    return {
        'id': record.id,
        'user_id': record.user_id,
        'points': record.points,
        'balance': record.balance,
        'description': record.description,
        'source_type': record.source_type,
        'source_id': record.source_id,
        'created_at': record.created_at.isoformat()
    }

def serialize_coupon(coupon: Coupon, include_usage=False):
    """将优惠券序列化"""
    data = {
        'id': coupon.id,
        'code': coupon.code,
        'name': coupon.name,
        'type': coupon.type,
        'discount_value': coupon.discount_value,
        'min_purchase': coupon.min_purchase,
        'start_date': coupon.start_date.isoformat(),
        'end_date': coupon.end_date.isoformat(),
        'is_active': coupon.is_active,
        'is_valid': coupon.is_valid()
    }
    
    if include_usage:
        data['max_uses'] = coupon.max_uses
        data['current_uses'] = coupon.current_uses
    
    return data

def serialize_user_coupon(user_coupon: UserCoupon):
    """将用户优惠券序列化"""
    data = {
        'id': user_coupon.id,
        'user_id': user_coupon.user_id,
        'coupon_id': user_coupon.coupon_id,
        'is_used': user_coupon.is_used,
        'acquired_at': user_coupon.acquired_at.isoformat()
    }
    
    if user_coupon.is_used and user_coupon.used_at:
        data['used_at'] = user_coupon.used_at.isoformat()
        data['order_id'] = user_coupon.order_id
    
    # 包含优惠券详情
    data['coupon'] = serialize_coupon(user_coupon.coupon)
    
    return data

# --- API 路由 ---

@user_bp.route('/me', methods=['GET'])
@jwt_required() # 需要有效 JWT 才能访问
def get_current_user():
    """获取当前登录用户的信息"""
    try:
        current_user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({"error": "无法解析用户信息"}), 422

    user = User.query.get(current_user_id)
    if not user:
         # 这种情况理论上不应发生，因为 JWT 验证通过了
        return jsonify({"error": "用户未找到"}), 404
    
    # 检查是否需要包含详细信息
    include_details = request.args.get('include_details') == 'true'
    include_custom_fields = request.args.get('include_custom_fields') == 'true'
    
    # 返回当前用户信息
    result = serialize_user(user, include_email=True, 
                           include_details=include_details,
                           include_custom_fields=include_custom_fields)
    
    # 获取用户地址（可选）
    if request.args.get('include_addresses') == 'true':
        addresses = user.addresses.order_by(Address.is_default.desc(), Address.created_at.desc()).all()
        result['addresses'] = [serialize_address(addr) for addr in addresses]
    
    # 获取积分记录（可选）
    if request.args.get('include_points_records') == 'true':
        points_records = user.points_records.order_by(PointsRecord.created_at.desc()).limit(10).all()
        result['points_records'] = [serialize_points_record(record) for record in points_records]
    
    # 获取优惠券（可选）
    if request.args.get('include_coupons') == 'true':
        coupons = user.coupons.filter(UserCoupon.is_used == False).all()
        result['coupons'] = [serialize_user_coupon(coupon) for coupon in coupons]
    
    return jsonify(result)

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """更新当前登录用户的信息"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    updated = False
    
    # 标准字段更新
    standard_fields = ['email', 'username', 'gender', 'real_name', 'birthday', 'phone']
    
    for field in standard_fields:
        if field in data:
            # 特殊字段处理
            if field == 'email' and data['email']:
                # 检查邮箱是否已被占用
                existing_user = User.query.filter(User.email == data['email'], 
                                                 User.id != current_user_id).first()
                if existing_user:
                    return jsonify({"error": "邮箱已被使用"}), 409
            
            if field == 'username' and data['username']:
                # 检查用户名是否已被占用
                existing_user = User.query.filter(User.username == data['username'], 
                                                 User.id != current_user_id).first()
                if existing_user:
                    return jsonify({"error": "用户名已被使用"}), 409
            
            if field == 'phone' and data['phone']:
                # 检查手机号是否已被占用
                existing_user = User.query.filter(User.phone == data['phone'], 
                                                 User.id != current_user_id).first()
                if existing_user:
                    return jsonify({"error": "手机号已被使用"}), 409
            
            # 特殊处理生日字段
            if field == 'birthday' and data['birthday']:
                try:
                    user.birthday = datetime.fromisoformat(data['birthday'])
                except ValueError:
                    return jsonify({"error": "生日格式无效，请使用YYYY-MM-DD格式"}), 400
            else:
                # 更新其他标准字段
                setattr(user, field, data[field])
            
            updated = True
    
    # 更新密码
    if 'password' in data:
        new_password = data['password']
        # TODO: 添加密码强度校验
        user.set_password(new_password)
        updated = True
    
    # 处理自定义字段
    if 'custom_fields' in data and isinstance(data['custom_fields'], dict):
        for key, value in data['custom_fields'].items():
            # 检查是否为有效的自定义字段
            field_def = UserFieldDefinition.query.filter_by(field_key=key).first()
            if field_def:
                user.set_custom_field(key, value)
                updated = True
    
    if updated:
        try:
            db.session.commit()
            return jsonify({"message": "用户信息更新成功"})
        except Exception as e:
            db.session.rollback()
            # log error e
            return jsonify({"error": f"更新失败: {str(e)}"}), 500
    else:
        return jsonify({"message": "没有提供需要更新的信息"}), 200

# --- 新增：修改密码路由 ---
@user_bp.route('/me/password', methods=['PUT'])
@jwt_required()
def change_password():
    """修改当前登录用户的密码"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404 # 理论上不会发生

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({"error": "当前密码和新密码不能为空"}), 400

    # 1. 验证当前密码
    if not user.check_password(current_password):
        return jsonify({"error": "当前密码不正确"}), 401 # Unauthorized 或 400 Bad Request 也可以

    # 2. (可选) 验证新密码强度，例如长度
    if len(new_password) < 6:
        return jsonify({"error": "新密码长度至少需要6位"}), 400
    
    # 3. (可选) 避免新旧密码相同
    if current_password == new_password:
        return jsonify({"error": "新密码不能与当前密码相同"}), 400

    # 4. 设置新密码并保存
    try:
        user.set_password(new_password)
        db.session.commit()
        # 密码修改成功后，可以考虑让前端强制用户重新登录（可选，增加安全性）
        return jsonify({"message": "密码修改成功"})
    except Exception as e:
        db.session.rollback()
        # log error e
        return jsonify({"error": "密码更新失败，请稍后重试"}), 500
# --- 修改密码路由结束 ---

# 新增：获取用户积分记录
@user_bp.route('/me/points', methods=['GET'])
@jwt_required()
def get_my_points():
    """获取当前用户的积分记录"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404
    
    # 分页参数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # 获取积分记录
    points_query = user.points_records.order_by(PointsRecord.created_at.desc())
    points_paginated = points_query.paginate(page=page, per_page=per_page)
    
    # 序列化结果
    result = {
        'points_balance': user.points,
        'points_records': [serialize_points_record(record) for record in points_paginated.items],
        'pagination': {
            'total': points_paginated.total,
            'pages': points_paginated.pages,
            'page': page,
            'per_page': per_page,
            'has_next': points_paginated.has_next,
            'has_prev': points_paginated.has_prev
        }
    }
    
    return jsonify(result)

# 新增：获取用户优惠券
@user_bp.route('/me/coupons', methods=['GET'])
@jwt_required()
def get_my_coupons():
    """获取当前用户的优惠券"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404
    
    # 查询参数
    status = request.args.get('status', 'valid')  # valid, used, all
    
    # 根据状态筛选
    coupons_query = user.coupons
    if status == 'valid':
        coupons_query = coupons_query.filter(UserCoupon.is_used == False)
    elif status == 'used':
        coupons_query = coupons_query.filter(UserCoupon.is_used == True)
    
    # 获取优惠券
    coupons = coupons_query.all()
    
    # 序列化结果
    result = {
        'coupons': [serialize_user_coupon(coupon) for coupon in coupons]
    }
    
    return jsonify(result)

# 新增：获取会员等级
@user_bp.route('/member-levels', methods=['GET'])
def get_member_levels():
    """获取所有会员等级"""
    levels = MemberLevel.query.order_by(MemberLevel.min_points).all()
    
    result = []
    for level in levels:
        level_data = {
            'id': level.id,
            'name': level.name,
            'description': level.description,
            'min_points': level.min_points,
            'min_spend': level.min_spend,
            'discount_rate': level.discount_rate,
            'icon_url': level.icon_url,
            'benefits': level.get_benefits()
        }
        result.append(level_data)
    
    return jsonify({'member_levels': result})

# 新增：获取用户字段定义
@user_bp.route('/user-fields', methods=['GET'])
def get_user_field_definitions():
    """获取所有用户字段定义"""
    fields = UserFieldDefinition.query.filter_by(is_visible=True).order_by(UserFieldDefinition.display_order).all()
    
    result = [serialize_user_field_definition(field) for field in fields]
    
    return jsonify({'user_fields': result})

# 新增：管理端 - 添加/编辑用户字段定义
@user_bp.route('/admin/user-fields', methods=['POST'])
@admin_required
def add_user_field_definition():
    """添加新的用户字段定义（管理员专用）"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400
    
    # 必填字段验证
    required_fields = ['field_key', 'field_name', 'field_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400
    
    # 检查字段键是否已存在
    existing_field = UserFieldDefinition.query.filter_by(field_key=data['field_key']).first()
    if existing_field:
        return jsonify({"error": "字段键已存在"}), 409
    
    # 创建新字段
    field_def = UserFieldDefinition(
        field_key=data['field_key'],
        field_name=data['field_name'],
        field_type=data['field_type'],
        is_required=data.get('is_required', False),
        is_visible=data.get('is_visible', True),
        display_order=data.get('display_order', 0)
    )
    
    # 设置选项（如果有）
    if 'options' in data and isinstance(data['options'], list):
        field_def.set_options(data['options'])
    
    try:
        db.session.add(field_def)
        db.session.commit()
        return jsonify({
            "message": "字段定义添加成功",
            "field": serialize_user_field_definition(field_def)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"添加字段定义失败: {str(e)}"}), 500

@user_bp.route('/admin/user-fields/<int:field_id>', methods=['PUT'])
@admin_required
def update_user_field_definition(field_id):
    """更新用户字段定义（管理员专用）"""
    field_def = UserFieldDefinition.query.get(field_id)
    if not field_def:
        return jsonify({"error": "字段定义不存在"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400
    
    # 更新字段属性（不允许修改field_key）
    if 'field_name' in data:
        field_def.field_name = data['field_name']
    
    if 'field_type' in data:
        field_def.field_type = data['field_type']
    
    if 'is_required' in data:
        field_def.is_required = data['is_required']
    
    if 'is_visible' in data:
        field_def.is_visible = data['is_visible']
    
    if 'display_order' in data:
        field_def.display_order = data['display_order']
    
    # 更新选项（如果有）
    if 'options' in data and isinstance(data['options'], list):
        field_def.set_options(data['options'])
    
    try:
        db.session.commit()
        return jsonify({
            "message": "字段定义更新成功",
            "field": serialize_user_field_definition(field_def)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新字段定义失败: {str(e)}"}), 500

@user_bp.route('/admin/user-fields/<int:field_id>', methods=['DELETE'])
@admin_required
def delete_user_field_definition(field_id):
    """删除用户字段定义（管理员专用）"""
    field_def = UserFieldDefinition.query.get(field_id)
    if not field_def:
        return jsonify({"error": "字段定义不存在"}), 404
    
    try:
        # 删除相关的用户自定义字段数据
        UserCustomField.query.filter_by(field_key=field_def.field_key).delete()
        
        # 删除字段定义
        db.session.delete(field_def)
        db.session.commit()
        
        return jsonify({"message": "字段定义删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除字段定义失败: {str(e)}"}), 500

@user_bp.route('/users', methods=['GET'])
@admin_required # 使用我们定义的管理员权限检查装饰器
def get_user_list():
    """获取用户列表（仅管理员）- 支持分页和搜索筛选"""
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 防止恶意请求大量数据
    if per_page > 50:
        per_page = 50
        
    # 获取搜索和筛选参数
    search_query = request.args.get('search', '', type=str)
    admin_filter = request.args.get('admin', '', type=str)
    created_from = request.args.get('created_from', '', type=str)
    created_to = request.args.get('created_to', '', type=str)
    
    # 构建查询
    query = User.query
    
    # 应用搜索条件
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(or_(
            User.username.ilike(search_term),
            User.email.ilike(search_term)
        ))
    
    # 应用管理员筛选
    if admin_filter.lower() == 'true':
        query = query.filter(User.is_admin == True)
    elif admin_filter.lower() == 'false':
        query = query.filter(User.is_admin == False)
    
    # 应用创建时间筛选
    if created_from:
        try:
            from_date = datetime.fromisoformat(created_from.replace('Z', '+00:00'))
            query = query.filter(User.created_at >= from_date)
        except ValueError:
            # 无效的日期格式，忽略此筛选条件
            pass
    
    if created_to:
        try:
            to_date = datetime.fromisoformat(created_to.replace('Z', '+00:00'))
            query = query.filter(User.created_at <= to_date)
        except ValueError:
            # 无效的日期格式，忽略此筛选条件
            pass
    
    # 执行分页查询
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # 准备响应数据
    users_data = [serialize_user(user, include_email=True) for user in pagination.items]
    
    # 返回分页结果
    return jsonify({
        'users': users_data,
        'pagination': {
            'total_items': pagination.total,
            'total_pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })

# 新增：获取特定用户详情
@user_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_detail(user_id):
    """获取特定用户的详细信息（仅管理员）"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 管理员可以查看用户的更多信息，包括邮箱
    user_data = serialize_user(user, include_email=True)
    # 添加管理员状态
    user_data['is_admin'] = user.is_admin
    
    return jsonify(user_data)

# 新增：修改用户管理员状态
@user_bp.route('/users/<int:user_id>/admin', methods=['PUT'])
@admin_required
def update_user_admin_status(user_id):
    """修改用户的管理员状态（仅管理员）"""
    # 获取当前管理员ID
    current_admin_id = get_jwt_identity()
    
    # 防止管理员修改自己的状态
    if int(current_admin_id) == user_id:
        return jsonify({"error": "不能修改自己的管理员状态"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    data = request.get_json()
    if not data or 'is_admin' not in data:
        return jsonify({"error": "请求体应包含is_admin字段"}), 400
    
    try:
        user.is_admin = bool(data['is_admin'])
        db.session.commit()
        return jsonify({"message": f"用户{user.username}的管理员状态已更新", "is_admin": user.is_admin})
    except Exception as e:
        db.session.rollback()
        # 记录错误信息 e
        return jsonify({"error": "更新失败，请稍后重试"}), 500

# --- 新增：批量操作用户的API ---
@user_bp.route('/users/batch', methods=['POST'])
@admin_required
def batch_update_users():
    """批量更新用户状态（仅管理员）"""
    # 获取当前管理员ID
    current_admin_id = int(get_jwt_identity())
    
    data = request.get_json()
    if not data or 'user_ids' not in data or 'action' not in data:
        return jsonify({"error": "请求体应包含user_ids和action字段"}), 400
    
    user_ids = data['user_ids']
    action = data['action']
    
    # 验证用户ID列表
    if not isinstance(user_ids, list) or not all(isinstance(id, int) for id in user_ids):
        return jsonify({"error": "user_ids应为整数ID列表"}), 400
    
    # 防止管理员修改自己的状态
    if current_admin_id in user_ids:
        return jsonify({"error": "不能修改自己的状态"}), 403
    
    # 根据action执行对应的批量操作
    try:
        if action == 'make_admin':
            # 批量设为管理员
            affected_rows = User.query.filter(User.id.in_(user_ids)).update({User.is_admin: True}, synchronize_session=False)
            db.session.commit()
            return jsonify({"message": f"已将{affected_rows}个用户设为管理员", "affected_count": affected_rows})
            
        elif action == 'remove_admin':
            # 批量取消管理员
            affected_rows = User.query.filter(User.id.in_(user_ids)).update({User.is_admin: False}, synchronize_session=False)
            db.session.commit()
            return jsonify({"message": f"已取消{affected_rows}个用户的管理员权限", "affected_count": affected_rows})
        else:
            return jsonify({"error": f"不支持的操作: {action}"}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"批量操作失败: {str(e)}"}), 500

# --- 地址管理 API ---

@user_bp.route('/me/addresses', methods=['GET'])
@jwt_required()
def get_my_addresses():
    """获取当前用户的所有收货地址"""
    current_user_id = int(get_jwt_identity()) # JWT identity 是字符串，转为 int
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404 # 理论上不会发生

    addresses = user.addresses.order_by(Address.is_default.desc(), Address.created_at.desc()).all()
    return jsonify(addresses=[serialize_address(addr) for addr in addresses])

@user_bp.route('/me/addresses', methods=['POST'])
@jwt_required()
def add_my_address():
    """为当前用户添加新地址"""
    current_user_id = int(get_jwt_identity())
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    # 验证必要字段
    required_fields = ['recipient_name', 'phone_number', 'province', 'city', 'district', 'detailed_address']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": f"缺少必要字段: {required_fields}"}), 400

    # 处理 is_default 逻辑：如果新地址设为默认，则将该用户其他地址设为非默认
    is_default = data.get('is_default', False)
    if is_default:
        Address.query.filter_by(user_id=current_user_id, is_default=True).update({Address.is_default: False})

    new_address = Address(
        user_id=current_user_id,
        recipient_name=data['recipient_name'],
        phone_number=data['phone_number'],
        province=data['province'],
        city=data['city'],
        district=data['district'],
        detailed_address=data['detailed_address'],
        is_default=is_default
    )

    try:
        db.session.add(new_address)
        db.session.commit()
        return jsonify(serialize_address(new_address)), 201 # 返回新创建的地址
    except Exception as e:
        db.session.rollback()
        # log error e
        return jsonify({"error": "添加地址失败"}), 500

@user_bp.route('/me/addresses/<int:address_id>', methods=['PUT'])
@jwt_required()
def update_my_address(address_id):
    """更新当前用户的指定地址"""
    current_user_id = int(get_jwt_identity())
    
    address = Address.query.get(address_id)

    # 验证地址是否存在且属于当前用户
    if not address or address.user_id != current_user_id:
        return jsonify({"error": "地址未找到或无权限"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    updated = False
    # 处理 is_default 逻辑
    if 'is_default' in data and data['is_default'] and not address.is_default:
        Address.query.filter_by(user_id=current_user_id, is_default=True).update({Address.is_default: False})
        address.is_default = True
        updated = True
    elif 'is_default' in data and not data['is_default'] and address.is_default:
        # 不允许将唯一的默认地址取消默认，除非有其他地址设为默认
        # 简化处理：如果取消默认，就直接取消 (用户需要手动设置另一个默认)
        address.is_default = False
        updated = True
        
    # 更新其他字段
    for field in ['recipient_name', 'phone_number', 'province', 'city', 'district', 'detailed_address']:
        if field in data:
            setattr(address, field, data[field])
            updated = True

    if not updated:
        return jsonify({"message": "未提供需要更新的信息"}), 200

    try:
        db.session.commit()
        return jsonify(serialize_address(address))
    except Exception as e:
        db.session.rollback()
        # log error e
        return jsonify({"error": "更新地址失败"}), 500

@user_bp.route('/me/addresses/<int:address_id>', methods=['DELETE'])
@jwt_required()
def delete_my_address(address_id):
    """删除当前用户的指定地址"""
    current_user_id = int(get_jwt_identity())
    address = Address.query.get(address_id)

    # 验证地址是否存在且属于当前用户
    if not address or address.user_id != current_user_id:
        return jsonify({"error": "地址未找到或无权限"}), 404
        
    # 如果删除的是默认地址，需要考虑后续逻辑（例如不允许删除，或自动选择下一个为默认）
    # 简化处理：直接删除
    if address.is_default:
        # 可能需要处理没有默认地址的情况，或提示用户
        pass 

    try:
        db.session.delete(address)
        db.session.commit()
        return jsonify({"message": "地址删除成功"}), 200
    except Exception as e:
        db.session.rollback()
        # log error e
        return jsonify({"error": "删除地址失败"}), 500

# --- 地址管理 API 结束 ---

# --- 未来可以添加的路由 ---
# GET /api/users/<int:user_id> (获取特定用户信息，管理员或用户自己)
# DELETE /api/users/<int:user_id> (删除用户，仅管理员)
# PUT /api/users/<int:user_id> (管理员更新任意用户信息)

@user_bp.route('/debug', methods=['GET'])
def debug_info():
    """调试路由，返回请求信息和服务器状态"""
    import sys
    
    # 打印请求头到控制台
    print(f"[DEBUG] Request Headers:\n{request.headers}", file=sys.stderr)
    
    # 安全获取请求头
    safe_headers = {}
    for key in request.headers.keys():
        safe_headers[key] = request.headers.get(key)
    
    # 安全获取请求参数
    safe_args = {}
    for key in request.args.keys():
        safe_args[key] = request.args.get(key)
    
    # 准备调试信息
    debug_data = {
        "request": {
            "path": request.path,
            "method": request.method,
            "headers": safe_headers,
            "args": safe_args
        },
        "server": {
            "timestamp": datetime.utcnow().isoformat(),
            "api_version": "1.0"
        }
    }
    
    # 尝试获取当前用户（如果有JWT）
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            debug_data["auth"] = {"has_token": True}
            
            # 尝试解码令牌
            try:
                from flask_jwt_extended import decode_token
                token = auth_header.split(' ')[1]
                decoded_token = decode_token(token)
                debug_data["auth"]["decoded"] = {
                    "user_id": decoded_token.get('sub'),
                    "exp": decoded_token.get('exp'),
                    "iat": decoded_token.get('iat')
                }
            except Exception as e:
                debug_data["auth"]["error"] = str(e)
        else:
            debug_data["auth"] = {"has_token": False}
    except Exception as e:
        debug_data["auth_error"] = str(e)
    
    return jsonify(debug_data) 

@user_bp.route('/debug/make-admin/<int:user_id>', methods=['GET'])
def debug_make_admin(user_id):
    """调试路由：将指定用户设为管理员（仅用于开发测试）"""
    import sys
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"用户ID {user_id} 不存在"}), 404
            
        # 设置为管理员
        user.is_admin = True
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"用户 {user.username} (ID: {user.id}) 已设置为管理员",
            "user": serialize_user(user, include_email=True)
        })
    except Exception as e:
        db.session.rollback()
        print(f"[DEBUG] 设置管理员失败: {str(e)}", file=sys.stderr)
        return jsonify({"error": f"操作失败: {str(e)}"}), 500 