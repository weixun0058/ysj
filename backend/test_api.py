#!/usr/bin/env python3
from app import app
import json

def test_admin_login():
    """测试管理员登录并获取用户信息"""
    
    # 尝试不同的密码
    credentials_to_try = [
        {'login': 'superadmin', 'password': 'admin123'},
        {'login': 'superadmin', 'password': 'superadmin'},
        {'login': 'superadmin', 'password': 'password'},
        {'login': 'superadmin', 'password': '123456'},
    ]
    
    for cred in credentials_to_try:
        print(f"\n尝试登录: {cred['login']} / {cred['password']}")
        with app.test_client() as client:
            # 登录
            login_response = client.post('/api/login', json=cred)
            print(f"登录响应: {login_response.status_code}")
            
            if login_response.status_code == 200:
                data = json.loads(login_response.data)
                token = data.get('access_token')
                print(f"获取到Token: {token[:10]}..." if token else "无Token")
                
                if token:
                    # 获取用户信息
                    user_response = client.get('/api/me', 
                                             headers={'Authorization': f'Bearer {token}'})
                    print(f"获取用户信息响应: {user_response.status_code}")
                    
                    if user_response.status_code == 200:
                        user_data = json.loads(user_response.data)
                        print(f"用户信息: {user_data}")
                        print(f"用户是否为管理员: {user_data.get('is_admin', '未找到管理员字段')}")
                        return  # 找到正确密码，退出
                    else:
                        print(f"获取用户信息失败: {user_response.data}")
            else:
                print(f"登录失败: {login_response.data.decode('utf-8')}")

def reset_admin_password():
    """重置管理员密码"""
    print("\n尝试重置superadmin的密码...")
    with app.app_context():
        from models import db, User
        user = User.query.filter_by(username='superadmin').first()
        if user:
            user.set_password('superadmin123')
            db.session.commit()
            print("密码重置为: superadmin123")
        else:
            print("未找到superadmin用户")

if __name__ == "__main__":
    # 先测试登录
    test_admin_login()
    
    # 如果都失败，尝试重置密码
    reset_admin_password()
    
    # 使用新密码测试
    print("\n使用重置后的密码尝试登录:")
    with app.test_client() as client:
        login_response = client.post('/api/login', 
                                   json={'login': 'superadmin', 'password': 'superadmin123'})
        print(f"登录响应: {login_response.status_code}")
        
        if login_response.status_code == 200:
            data = json.loads(login_response.data)
            token = data.get('access_token')
            print(f"获取到Token: {token[:10]}..." if token else "无Token")
            
            if token:
                user_response = client.get('/api/me', 
                                         headers={'Authorization': f'Bearer {token}'})
                if user_response.status_code == 200:
                    user_data = json.loads(user_response.data)
                    print(f"登录成功! 用户信息: {user_data}")
                    print(f"用户是否为管理员: {user_data.get('is_admin', '未找到管理员字段')}")
                else:
                    print(f"获取用户信息失败: {user_response.data}")
        else:
            print(f"登录失败: {login_response.data.decode('utf-8')}") 