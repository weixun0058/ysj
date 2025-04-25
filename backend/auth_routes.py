from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
import re # 用于邮箱格式校验
import sys
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

def is_valid_email(email):
    """简单的邮箱格式校验"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """简单的手机号格式校验（中国大陆手机号）"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    username = data.get('username')
    phone = data.get('phone')  # 新增手机号作为必填字段
    email = data.get('email')  # 邮箱现为可选字段
    password = data.get('password')
    
    # 验证必填字段
    if not username or not phone or not password:
        return jsonify({"error": "用户名、手机号和密码不能为空"}), 400

    # 验证手机号格式
    if not is_valid_phone(phone):
        return jsonify({"error": "无效的手机号格式"}), 400
    
    # 如果提供了邮箱，则验证邮箱格式
    if email and not is_valid_email(email):
        return jsonify({"error": "无效的邮箱格式"}), 400

    # 验证用户名唯一性
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409 # 409 Conflict

    # 验证手机号唯一性
    if User.query.filter_by(phone=phone).first():
        return jsonify({"error": "手机号已被注册"}), 409 # 409 Conflict

    # 如果提供了邮箱，验证邮箱唯一性
    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已被注册"}), 409 # 409 Conflict

    # 创建新用户
    new_user = User(username=username, phone=phone, email=email)
    new_user.set_password(password)
    
    # 添加可选的其他字段
    if 'gender' in data:
        new_user.gender = data.get('gender')
    if 'real_name' in data:
        new_user.real_name = data.get('real_name')
    if 'birthday' in data and data.get('birthday'):
        try:
            new_user.birthday = datetime.fromisoformat(data.get('birthday'))
        except ValueError:
            # 如果生日格式不正确，忽略该字段
            pass
    
    # 设置最后登录时间
    new_user.last_login = datetime.utcnow()
    
    db.session.add(new_user)
    try:
        db.session.commit()
        # 生成访问令牌
        access_token = create_access_token(identity=str(new_user.id))
        return jsonify({
            "message": "用户注册成功", 
            "user_id": new_user.id,
            "access_token": access_token
        }), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        # Log the exception e
        return jsonify({"error": f"注册失败: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    # 允许使用用户名、邮箱或手机号登录
    login_identifier = data.get('login') # 前端发送 'login' 字段，可以是 username、email 或 phone
    password = data.get('password')

    if not login_identifier or not password:
        return jsonify({"error": "登录标识（用户名/邮箱/手机号）和密码不能为空"}), 400

    # 查找用户（使用用户名、邮箱或手机号）
    user = User.query.filter(
        (User.username == login_identifier) | 
        (User.email == login_identifier) | 
        (User.phone == login_identifier)
    ).first()

    if user and user.check_password(password):
        # 密码正确，更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成 JWT
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    else:
        # 用户不存在或密码错误
        return jsonify({"error": "无效的登录凭证"}), 401 # 401 Unauthorized 

# 保留原有代码的其他路由和功能... 