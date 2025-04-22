#!/usr/bin/env python3
from app import app
from models import db, User

# 检查所有用户
with app.app_context():
    users = User.query.all()
    print(f"系统中共有 {len(users)} 个用户:")
    
    for user in users:
        print(f"用户名: {user.username}, 邮箱: {user.email}, 管理员: {'是' if user.is_admin else '否'}")
    
    # 检查特定用户
    superadmin = User.query.filter_by(username='superadmin').first()
    if superadmin:
        print(f"\n特定检查 - superadmin 用户存在且管理员状态: {'是' if superadmin.is_admin else '否'}")
    else:
        print("\n特定检查 - superadmin 用户不存在") 