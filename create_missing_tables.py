import sqlite3
import os

# 数据库位于后端目录
db_path = 'backend/app.db'

# 确保数据库文件存在
if not os.path.exists(db_path):
    print(f"数据库文件 {db_path} 不存在")
    exit(1)

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 开始事务
conn.execute('BEGIN TRANSACTION')

try:
    # 创建 user_custom_field 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_custom_field (
        id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        field_key VARCHAR(50) NOT NULL, 
        field_value TEXT, 
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user (id),
        UNIQUE (user_id, field_key)
    )
    ''')
    
    # 创建 member_level 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS member_level (
        id INTEGER NOT NULL, 
        name VARCHAR(50) NOT NULL,
        description TEXT,
        points_threshold INTEGER,
        discount_rate FLOAT,
        icon VARCHAR(255),
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id)
    )
    ''')
    
    # 创建 address 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS address (
        id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        recipient_name VARCHAR(100) NOT NULL, 
        phone_number VARCHAR(20) NOT NULL, 
        province VARCHAR(50) NOT NULL, 
        city VARCHAR(50) NOT NULL, 
        district VARCHAR(50) NOT NULL, 
        detail_address TEXT NOT NULL,
        is_default BOOLEAN,
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id)
    )
    ''')
    
    # 创建 user_field_definition 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_field_definition (
        id INTEGER NOT NULL, 
        field_key VARCHAR(50) NOT NULL, 
        field_name VARCHAR(100) NOT NULL, 
        field_type VARCHAR(20) NOT NULL, 
        is_required BOOLEAN DEFAULT 0, 
        is_visible BOOLEAN DEFAULT 1, 
        display_order INTEGER DEFAULT 0, 
        options TEXT, 
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id),
        UNIQUE (field_key)
    )
    ''')
    
    # 创建 coupon 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coupon (
        id INTEGER NOT NULL, 
        code VARCHAR(50) NOT NULL,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        discount_type VARCHAR(20) NOT NULL,
        discount_value FLOAT NOT NULL,
        min_purchase FLOAT,
        max_discount FLOAT,
        start_date DATETIME,
        end_date DATETIME,
        is_active BOOLEAN DEFAULT 1,
        usage_limit INTEGER,
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id),
        UNIQUE (code)
    )
    ''')
    
    # 创建 user_coupon 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_coupon (
        id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        coupon_id INTEGER NOT NULL, 
        is_used BOOLEAN DEFAULT 0, 
        used_at DATETIME, 
        order_id INTEGER, 
        acquired_at DATETIME, 
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id),
        FOREIGN KEY(coupon_id) REFERENCES coupon (id)
    )
    ''')
    
    # 提交事务
    conn.execute('COMMIT')
    print("成功创建所有缺少的表")
    
except Exception as e:
    # 如果有错误，回滚事务
    conn.execute('ROLLBACK')
    print(f"创建表失败: {e}")
    
finally:
    # 关闭连接
    conn.close() 