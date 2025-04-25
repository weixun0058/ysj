from app import app, db
from models import Product
 
with app.app_context():
    print('产品总数:', db.session.query(Product).count()) 