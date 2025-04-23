from flask import Blueprint, jsonify, request, current_app
import os
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from functools import wraps
import re
from unicodedata import normalize

# 创建蓝图
settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

# 设置文件路径
def get_settings_path():
    """获取设置文件路径"""
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, 'site_settings.json')

# 上传目录设置
def get_upload_dir():
    """获取上传目录"""
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    upload_dir = os.path.join(base_dir, 'uploads', 'settings')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

# 加载设置
def load_settings():
    """加载设置文件，如果不存在则创建默认设置"""
    settings_path = get_settings_path()
    
    # 默认设置
    default_settings = {
        "siteName": "塞外本草 / 壹世健",
        "logo": "",
        "contactEmail": "info@yishijian.com",
        "contactPhone": "+86 XXX-XXXX-XXXX",
        "address": "新疆伊犁尼勒克地区",
        "socialMedia": {
            "weixin": "",
            "weibo": ""
        },
        "footerText": "© 2024 塞外本草 - 壹世健. 版权所有。"
    }
    
    # 如果设置文件不存在，创建默认设置文件
    if not os.path.exists(settings_path):
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=2)
        return default_settings
    
    # 读取设置文件
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return settings
    except Exception as e:
        current_app.logger.error(f"加载设置文件时出错: {str(e)}")
        return default_settings

# 保存设置
def save_settings(settings):
    """保存设置到文件"""
    settings_path = get_settings_path()
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        current_app.logger.error(f"保存设置文件时出错: {str(e)}")
        return False

# 管理员检查装饰器
def admin_required(fn):
    """验证用户是否为管理员的装饰器"""
    @wraps(fn)
    @jwt_required()  # 首先需要有有效的JWT
    def wrapper(*args, **kwargs):
        # 获取当前用户身份
        current_user_id = get_jwt_identity()
        
        # 这里应该查询数据库判断用户是否为管理员
        # 简化版本：假设有个判断函数 is_admin
        from models import User
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "需要管理员权限"}), 403
            
        return fn(*args, **kwargs)
    return wrapper

# 安全文件名生成
def _slugify(text: str) -> str:
    """生成安全的slug，用于文件名"""
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_').lower()
    return text or 'file'

# 获取设置接口
@settings_bp.route('', methods=['GET'])
def get_site_settings():
    """获取网站设置"""
    try:
        settings = load_settings()
        return jsonify(settings), 200
    except Exception as e:
        return jsonify({"error": f"获取设置失败: {str(e)}"}), 500

# 更新设置接口
@settings_bp.route('', methods=['PUT'])
@admin_required
def update_site_settings():
    """更新网站设置，需要管理员权限"""
    try:
        # 获取当前设置
        current_settings = load_settings()
        
        # 获取请求中的新设置
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求中没有数据"}), 400
            
        # 更新设置，不包括logo（logo通过专门的上传接口处理）
        for key, value in data.items():
            if key != 'logo':  # logo不通过这个接口更新
                current_settings[key] = value
                
        # 保存更新后的设置
        if save_settings(current_settings):
            return jsonify({"message": "设置已更新", "settings": current_settings}), 200
        else:
            return jsonify({"error": "保存设置失败"}), 500
            
    except Exception as e:
        return jsonify({"error": f"更新设置失败: {str(e)}"}), 500

# 上传Logo接口
@settings_bp.route('/logo', methods=['POST'])
@admin_required
def upload_logo():
    """上传网站Logo，需要管理员权限"""
    try:
        # 检查是否有文件
        if 'logo' not in request.files:
            return jsonify({"error": "没有文件"}), 400
            
        file = request.files['logo']
        if not file or not file.filename:
            return jsonify({"error": "没有选择文件"}), 400
            
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext not in allowed_extensions:
            return jsonify({"error": "不支持的文件类型，仅允许 PNG, JPG, JPEG, GIF 和 SVG"}), 400
            
        # 检查文件大小 (5MB 最大)
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
        if len(file.read()) > MAX_FILE_SIZE:
            file.seek(0)  # 重置文件指针
            return jsonify({"error": "文件太大（最大5MB）"}), 400
            
        file.seek(0)  # 重置文件指针
            
        # 保存文件
        upload_dir = get_upload_dir()
        # 生成唯一文件名
        timestamp = int(os.path.getmtime(get_settings_path())) if os.path.exists(get_settings_path()) else 0
        new_filename = f"logo_{timestamp}_{_slugify('logo')}.{ext}"
        filepath = os.path.join(upload_dir, new_filename)
        
        # 保存文件
        file.save(filepath)
        
        # 更新设置中的logo URL
        logo_url = f"/uploads/settings/{new_filename}"
        
        # 加载并更新设置
        settings = load_settings()
        settings['logo'] = logo_url
        
        if save_settings(settings):
            return jsonify({
                "message": "Logo上传成功",
                "logo_url": logo_url
            }), 200
        else:
            return jsonify({"error": "保存设置失败"}), 500
            
    except Exception as e:
        return jsonify({"error": f"上传Logo失败: {str(e)}"}), 500 