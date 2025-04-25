"""
为现有用户更新手机号（临时值）
"""
from app import app
from models import db, User
import random

def generate_temp_phone():
    """生成一个临时手机号"""
    return f"1399999{random.randint(1000, 9999)}"

def update_existing_users():
    """为现有用户设置临时手机号"""
    with app.app_context():
        # 获取所有没有手机号的用户
        users = User.query.filter(User.phone.is_(None)).all()
        
        if not users:
            print("没有需要更新的用户")
            return
        
        print(f"找到 {len(users)} 个需要更新的用户")
        
        for user in users:
            # 为每个用户生成一个唯一的临时手机号
            while True:
                temp_phone = generate_temp_phone()
                # 检查是否已被使用
                if not User.query.filter_by(phone=temp_phone).first():
                    break
            
            user.phone = temp_phone
            print(f"用户 {user.username} (ID: {user.id}) 设置临时手机号: {temp_phone}")
        
        # 保存更改
        db.session.commit()
        print("所有用户更新完成")

if __name__ == "__main__":
    update_existing_users() 