from app import app
from models import db, User

with app.app_context():
    user = User(username='admin', email='admin@example.com', is_admin=True)
    user.set_password('165131')
    db.session.add(user)
    db.session.commit()
    print('超级管理员用户创建成功！') 