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
    # 创建新表
    cursor.execute('''
    CREATE TABLE user_new (
        id INTEGER NOT NULL, 
        username VARCHAR(64) NOT NULL, 
        email VARCHAR(120), 
        password_hash VARCHAR(256), 
        created_at DATETIME, 
        is_admin BOOLEAN NOT NULL, 
        phone VARCHAR(20) DEFAULT NULL, 
        gender VARCHAR(10) DEFAULT NULL, 
        birthday DATE DEFAULT NULL, 
        real_name VARCHAR(50) DEFAULT NULL, 
        member_level_id INTEGER DEFAULT NULL, 
        points INTEGER DEFAULT 0, 
        total_spend FLOAT DEFAULT 0.0, 
        last_login DATETIME DEFAULT NULL, 
        PRIMARY KEY (id)
    )
    ''')
    
    # 复制数据
    cursor.execute('INSERT INTO user_new SELECT * FROM user')
    
    # 删除旧表
    cursor.execute('DROP TABLE user')
    
    # 重命名新表
    cursor.execute('ALTER TABLE user_new RENAME TO user')
    
    # 创建索引
    cursor.execute('CREATE UNIQUE INDEX ix_user_email ON user (email)')
    cursor.execute('CREATE UNIQUE INDEX ix_user_username ON user (username)')
    cursor.execute('CREATE UNIQUE INDEX ix_user_phone ON user (phone)')
    
    # 提交事务
    conn.execute('COMMIT')
    print("用户表已成功更新，email字段现在是可选的")
    
except Exception as e:
    # 如果有错误，回滚事务
    conn.execute('ROLLBACK')
    print(f"更新失败: {e}")
    
finally:
    # 关闭连接
    conn.close() 