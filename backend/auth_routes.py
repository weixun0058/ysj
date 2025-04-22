from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
import re # 用于邮箱格式校验
import sys

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

def is_valid_email(email):
    """简单的邮箱格式校验"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "用户名、邮箱和密码不能为空"}), 400

    if not is_valid_email(email):
         return jsonify({"error": "无效的邮箱格式"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409 # 409 Conflict

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "邮箱已被注册"}), 409 # 409 Conflict

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"message": "用户注册成功", "user_id": new_user.id}), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        # Log the exception e
        return jsonify({"error": "注册失败，请稍后重试"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # --- DEBUG PRINT --- 
    # import sys
    # print(f"[DEBUG /api/login] Received data: {data}", file=sys.stderr)
    # --- END DEBUG --- 
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    # 允许使用用户名或邮箱登录
    login_identifier = data.get('login') # 前端发送 'login' 字段，可以是 username 或 email
    password = data.get('password')

    # --- DEBUG PRINT --- 
    # print(f"[DEBUG /api/login] Attempting login with identifier: {login_identifier}", file=sys.stderr)
    # --- END DEBUG --- 

    if not login_identifier or not password:
        return jsonify({"error": "登录标识（用户名/邮箱）和密码不能为空"}), 400

    user = User.query.filter((User.username == login_identifier) | (User.email == login_identifier)).first()

    # --- DEBUG PRINT ---
    password_check_result = False # 初始化
    if user:
        # print(f"[DEBUG /api/login] User found: {user.username}, ID: {user.id}", file=sys.stderr)
        # print(f"[DEBUG /api/login] Stored password hash: {user.password_hash}", file=sys.stderr)
        password_check_result = user.check_password(password)
        # print(f"[DEBUG /api/login] check_password result: {password_check_result}", file=sys.stderr)
    # else:
        # print(f"[DEBUG /api/login] User not found for identifier: {login_identifier}", file=sys.stderr)
    # --- END DEBUG ---

    # if user and user.check_password(password):
    if user and password_check_result: # 使用上面debug获取的结果
        # 密码正确，生成 JWT
        access_token = create_access_token(identity=str(user.id)) # 将 user.id 转为字符串
        # print("[DEBUG /api/login] Login successful, returning token.", file=sys.stderr)
        return jsonify(access_token=access_token)
    else:
        # 用户不存在或密码错误
        # print("[DEBUG /api/login] Login failed, returning 401.", file=sys.stderr)
        return jsonify({"error": "无效的登录凭证"}), 401 # 401 Unauthorized 