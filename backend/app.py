from flask import Flask, send_from_directory, jsonify, request
import os
from werkzeug.utils import secure_filename
import json
from urllib.parse import urljoin
from unicodedata import normalize
import re
# 加载.env文件中的环境变量
from dotenv import load_dotenv
load_dotenv()  # 从.env文件加载环境变量
# 从 models 导入 db 和 migrate 实例
from models import db, migrate, User # <-- 导入 User 模型
# 导入 JWT 扩展
from flask_jwt_extended import JWTManager
import secrets # 用于生成安全的密钥
from flask_cors import CORS # 导入 CORS
import sys # 导入 sys 用于打印到 stderr
from datetime import timedelta

# 创建 Flask 应用实例
app = Flask(__name__, static_folder='../', static_url_path='')

# --- 配置 CORS ---
# 最简单的配置：允许所有来源访问所有路由
# 在生产中应指定具体的 origins
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}}) # 应用 CORS 配置，允许 /api/* 下的所有路由跨域，并允许携带凭证
# --- CORS 配置结束 ---

# --- JWT 配置 ---
# 从环境变量或默认生成密钥
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
# 可以设置令牌过期时间（例如：15分钟）
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)

# --- 开始: 添加 JWT 错误处理回调 ---
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print("[JWT ERROR] Expired token received.", file=sys.stderr)
    return jsonify(error="令牌已过期"), 401 # 返回 401 更符合标准

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    print(f"[JWT ERROR] Invalid token received: {error_string}", file=sys.stderr)
    # 根据错误类型细化处理
    if "Signature verification failed" in error_string:
        return jsonify(error="令牌签名无效"), 422 # 保持 422 如果你想明确区分
    elif "User claims verification failed" in error_string:
         return jsonify(error="用户声明验证失败"), 422
    else:
        return jsonify(error=f"无效令牌: {error_string}"), 422 # 默认返回 422

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    print(f"[JWT ERROR] Missing token: {error_string}", file=sys.stderr)
    return jsonify(error="请求缺少认证令牌"), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    print("[JWT ERROR] Fresh token required.", file=sys.stderr)
    return jsonify(error="需要刷新令牌"), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    print("[JWT ERROR] Token has been revoked.", file=sys.stderr)
    return jsonify(error="令牌已被撤销"), 401

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # 这个回调在 get_current_user() 时被调用，不是 @jwt_required 强制的
    # 但如果配置了 JWT_USER_LOOKUP_CALLBACK，它需要能正确找到用户
    identity = jwt_data["sub"]
    user = User.query.get(identity)
    print(f"[JWT USER LOOKUP] Looking up user for identity {identity}, found: {user}", file=sys.stderr)
    return user # 如果找不到用户，返回 None

@jwt.user_lookup_error_loader
def user_lookup_error_callback(_jwt_header, jwt_data):
    # 当 user_lookup_callback 返回 None 时触发
    identity = jwt_data.get("sub")
    print(f"[JWT USER LOOKUP ERROR] User identity {identity} not found.", file=sys.stderr)
    return jsonify(error=f"未找到与令牌关联的用户 {identity}"), 404

# --- 结束: 添加 JWT 错误处理回调 ---

# --- 数据库配置 ---
basedir = os.path.abspath(os.path.dirname(__file__))
# 设置数据库 URI，这里使用 SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
# 关闭 SQLAlchemy 的事件通知系统，如果不使用可以节省资源
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy 和 Migrate，关联 app
db.init_app(app)
migrate.init_app(app, db)
# --- 数据库配置结束 ---

# --- 文件上传配置 ---
BASE_DIR = os.path.abspath(app.static_folder)  # 项目根目录
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads') # 通用上传目录
PRODUCT_IMG_DIR = os.path.join(UPLOADS_DIR, 'products') # 产品图片目录
SETTINGS_UPLOAD_DIR = os.path.join(UPLOADS_DIR, 'settings') # 设置相关上传目录
app.config['PRODUCT_IMG_DIR'] = PRODUCT_IMG_DIR
app.config['SETTINGS_UPLOAD_DIR'] = SETTINGS_UPLOAD_DIR

# 确保上传目录存在
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(PRODUCT_IMG_DIR, exist_ok=True)
os.makedirs(SETTINGS_UPLOAD_DIR, exist_ok=True)
# --- 文件上传配置结束 ---

# --- 注册蓝图 ---
# 导入认证蓝图
from auth_routes import auth_bp
app.register_blueprint(auth_bp)
# 导入资讯蓝图
from news_routes import news_bp
app.register_blueprint(news_bp)
# 导入用户管理蓝图
from user_routes import user_bp
app.register_blueprint(user_bp)
# 导入产品管理蓝图 (使用新的数据库驱动逻辑)
from product_routes import product_bp
app.register_blueprint(product_bp)
# 导入网站设置蓝图
from settings_routes import settings_bp
app.register_blueprint(settings_bp)
# 注册品牌联名合作蓝图
from collaboration_routes import collaboration_bp
app.register_blueprint(collaboration_bp)
# --- 蓝图注册结束 ---

@app.route('/')
def index():
    """
    定义根路由，用于提供 index.html 文件。
    它会从项目根目录（即 backend 目录的上一级）查找 index.html。
    """
    # 使用 send_from_directory 从项目根目录提供 index.html
    # os.path.abspath(os.path.join(app.static_folder)) 获取项目根目录的绝对路径
    return send_from_directory(os.path.abspath(app.static_folder), 'index.html')

# 提供上传文件访问的路由 (通用)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    # 为安全起见，可以限制只访问特定子目录，但目前 UPLOADS_DIR 下都是允许公开访问的
    return send_from_directory(UPLOADS_DIR, filename)

if __name__ == '__main__':
    # 启动 Flask 开发服务器
    # host='0.0.0.0' 使服务器可以从本地网络访问
    # debug=True 开启调试模式，方便开发
    app.run(host='0.0.0.0', port=5000, debug=True) 