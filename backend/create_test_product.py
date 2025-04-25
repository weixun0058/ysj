from app import app, db
from models import Product, ProductCategory, ProductStock

# 在应用上下文中执行
with app.app_context():
    # 检查现有产品
    existing_products = db.session.query(Product).count()
    print(f"当前产品数量: {existing_products}")
    
    # 创建产品分类（如果不存在）
    category_name = "新疆特产"
    category = db.session.query(ProductCategory).filter_by(name=category_name).first()
    if not category:
        category = ProductCategory(name=category_name, description="新疆特色产品分类")
        db.session.add(category)
        db.session.commit()
        print(f"创建分类: {category_name}")
    
    # 创建测试产品
    product = Product(
        name="天山蜂蜜",
        price=188.00,
        description="纯正天山野生蜂蜜，来自新疆伊犁尼勒克地区。",
        is_featured=True,
        category_id=category.id,
        warning_stock=10,
        images=["honey1.jpg", "honey2.jpg"]
    )
    
    # 添加产品
    db.session.add(product)
    db.session.flush()  # 先保存一下获取ID
    print(f"添加产品: {product.name}, ID: {product.id}")
    
    # 创建并关联库存信息
    stock = ProductStock(
        product_id=product.id,
        total_stock=100,
        available_stock=100,
        prelock_stock=0
    )
    db.session.add(stock)
    
    # 提交事务
    db.session.commit()
    print(f"添加库存信息: 总库存={stock.total_stock}, 可用库存={stock.available_stock}")
    
    # 验证
    new_product = db.session.query(Product).filter_by(name="天山蜂蜜").first()
    if new_product and new_product.stock:
        print("产品添加成功!")
        print(f"产品名称: {new_product.name}")
        print(f"产品价格: {new_product.price}")
        print(f"产品分类: {new_product.category.name}")
        print(f"有效库存: {new_product.effective_stock}")
        print(f"库存状态: {new_product.stock_status}")  # 0=无库存，1=库存警告，2=库存充足
    else:
        print("产品添加失败!") 