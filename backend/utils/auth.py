from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from ..models import User

def admin_required(fn):
    """
    装饰器函数，用于检查当前请求的用户是否具有管理员权限。
    
    对需要管理员权限的路由函数进行装饰，确保只有管理员用户可以访问特定的API端点。
    
    使用示例:
    
    @app.route('/admin-only', methods=['GET'])
    @jwt_required()
    @admin_required
    def admin_only_route():
        return jsonify(message="你拥有管理员权限")
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 获取当前用户的身份信息（JWT）
        current_user_id = get_jwt_identity()
        
        # 查询用户对象
        user = User.query.get(current_user_id)
        
        # 检查用户是否存在且是管理员
        if not user or not user.is_admin:
            return jsonify({"error": "此操作需要管理员权限"}), 403
            
        # 如果是管理员，继续执行原函数
        return fn(*args, **kwargs)
    
    return wrapper 