# backend/user_routes.py
from flask import Blueprint, jsonify, request, abort
from models import db, User, Address
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash # 用于更新密码

user_bp = Blueprint('user', __name__, url_prefix='/api')

# --- 权限检查装饰器 (示例) ---
from functools import wraps

def admin_required(fn):
    """装饰器：检查 JWT 身份是否为管理员"""
    @wraps(fn)
    @jwt_required() # 确保用户已登录
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "管理员权限不足"}), 403
        return fn(*args, **kwargs)
    return wrapper

# --- 序列化函数 (简化示例) ---
def serialize_user(user: User, include_email=False):
    """将 User 对象序列化为字典 (简化)"""
    data = {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at.isoformat(),
        'is_admin': user.is_admin  # 添加管理员状态字段
    }
    if include_email:
        data['email'] = user.email
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

# --- API 路由 ---

@user_bp.route('/me', methods=['GET'])
@jwt_required() # 需要有效 JWT 才能访问
def get_current_user():
    """获取当前登录用户的信息"""
    # --- DEBUG PRINT ---
    # import sys
    # print(f"[DEBUG /api/me] Request Headers:\n{request.headers}", file=sys.stderr)
    # --- END DEBUG ---
    try:
        current_user_id = get_jwt_identity()
        # --- DEBUG PRINT ---
        # print(f"[DEBUG /api/me] JWT Identity (user_id): {current_user_id}", file=sys.stderr)
        # --- END DEBUG ---
    except Exception as e:
         # --- DEBUG PRINT ---
        # print(f"[DEBUG /api/me] Error getting JWT identity: {e}", file=sys.stderr)
        # --- END DEBUG ---
        return jsonify({"error": "无法解析用户信息"}), 422

    user = User.query.get(current_user_id)
    # --- DEBUG PRINT ---
    # if user:
        # print(f"[DEBUG /api/me] User found in DB: {user.username}", file=sys.stderr)
    # else:
        # print(f"[DEBUG /api/me] User with ID {current_user_id} not found in DB!", file=sys.stderr)
    # --- END DEBUG ---
    if not user:
         # 这种情况理论上不应发生，因为 JWT 验证通过了
        return jsonify({"error": "用户未找到"}), 404
    # 返回当前用户信息，包含邮箱
    return jsonify(serialize_user(user, include_email=True))

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """更新当前登录用户的信息（例如邮箱、密码）"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "用户未找到"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    updated = False
    # 更新邮箱 (简单示例，实际应考虑邮箱验证流程)
    if 'email' in data:
        new_email = data['email']
        # TODO: 添加邮箱格式验证
        # 检查新邮箱是否已被其他用户使用
        existing_user = User.query.filter(User.email == new_email, User.id != current_user_id).first()
        if existing_user:
            return jsonify({"error": "邮箱已被使用"}), 409
        user.email = new_email
        updated = True

    # 更新密码
    if 'password' in data:
        new_password = data['password']
        # TODO: 添加密码强度校验
        user.set_password(new_password)
        updated = True

    # 可以添加更新其他字段的逻辑，如 username (需检查唯一性)

    if updated:
        try:
            db.session.commit()
            return jsonify({"message": "用户信息更新成功"})
        except Exception as e:
            db.session.rollback()
            # log error e
            return jsonify({"error": "更新失败，请稍后重试"}), 500
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

@user_bp.route('/users', methods=['GET'])
@admin_required # 使用我们定义的管理员权限检查装饰器
def get_user_list():
    """获取用户列表（仅管理员）"""
    # 可以添加分页逻辑
    users = User.query.all()
    # 对于列表，通常不包含敏感信息如邮箱
    user_list = [serialize_user(user) for user in users]
    return jsonify(users=user_list)

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

# --- 新增：地址管理 API ---

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