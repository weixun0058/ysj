"""
数据库更新脚本：增强用户模型和添加新的相关表
"""
from app import app
from models import db, User, Address, UserCustomField, UserFieldDefinition, MemberLevel, PointsRecord, UserCoupon, Coupon
import sqlite3
import os

def check_column_exists(table, column):
    """检查表中是否存在特定列"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    conn.close()
    return any(col[1] == column for col in columns)

def check_table_exists(table):
    """检查数据库中是否存在特定表"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)

def add_column_to_user(column, type_with_constraints):
    """向用户表添加新列"""
    if not check_column_exists('user', column):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE user ADD COLUMN {column} {type_with_constraints}")
        conn.commit()
        conn.close()
        print(f"已添加列: user.{column}")
    else:
        print(f"列已存在: user.{column}")

def create_table_if_not_exists(table_name, create_table_sql):
    """如果表不存在，则创建表"""
    if not check_table_exists(table_name):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
        print(f"已创建表: {table_name}")
    else:
        print(f"表已存在: {table_name}")

def update_database():
    """执行数据库更新操作"""
    with app.app_context():
        # 向用户表添加新列
        add_column_to_user('phone', 'VARCHAR(20) DEFAULT NULL')
        add_column_to_user('gender', 'VARCHAR(10) DEFAULT NULL')
        add_column_to_user('birthday', 'DATE DEFAULT NULL')
        add_column_to_user('real_name', 'VARCHAR(50) DEFAULT NULL')
        add_column_to_user('member_level_id', 'INTEGER DEFAULT NULL')
        add_column_to_user('points', 'INTEGER DEFAULT 0')
        add_column_to_user('total_spend', 'FLOAT DEFAULT 0.0')
        add_column_to_user('last_login', 'DATETIME DEFAULT NULL')
        
        # 修改email列为可空
        # SQLite不直接支持修改列约束，需要通过创建新表并复制数据来实现
        # 此操作较复杂，暂不在脚本中实现
        print("注意: 需要手动将email字段设为可空")
        
        # 创建自定义字段表
        create_table_if_not_exists('user_custom_field', '''
            CREATE TABLE user_custom_field (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                field_key VARCHAR(50) NOT NULL,
                field_value TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, field_key),
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        
        # 创建用户字段定义表
        create_table_if_not_exists('user_field_definition', '''
            CREATE TABLE user_field_definition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_key VARCHAR(50) NOT NULL UNIQUE,
                field_name VARCHAR(100) NOT NULL,
                field_type VARCHAR(20) NOT NULL,
                is_required BOOLEAN DEFAULT 0,
                is_visible BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                options TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建会员等级表
        create_table_if_not_exists('member_level', '''
            CREATE TABLE member_level (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                description VARCHAR(255),
                min_points INTEGER DEFAULT 0,
                min_spend FLOAT DEFAULT 0.0,
                discount_rate FLOAT DEFAULT 1.0,
                icon_url VARCHAR(255),
                benefits TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建积分记录表
        create_table_if_not_exists('points_record', '''
            CREATE TABLE points_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points INTEGER NOT NULL,
                balance INTEGER NOT NULL,
                description VARCHAR(255),
                source_type VARCHAR(50),
                source_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        
        # 创建优惠券表
        create_table_if_not_exists('coupon', '''
            CREATE TABLE coupon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(50) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20) NOT NULL,
                discount_value FLOAT NOT NULL,
                min_purchase FLOAT DEFAULT 0.0,
                start_date DATETIME NOT NULL,
                end_date DATETIME NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                max_uses INTEGER DEFAULT 0,
                current_uses INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建用户优惠券关联表
        create_table_if_not_exists('user_coupon', '''
            CREATE TABLE user_coupon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                coupon_id INTEGER NOT NULL,
                is_used BOOLEAN DEFAULT 0,
                used_at DATETIME,
                order_id INTEGER,
                acquired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(coupon_id) REFERENCES coupon(id)
            )
        ''')
        
        # 创建默认会员等级
        if not MemberLevel.query.first():
            default_level = MemberLevel(
                name="普通会员",
                description="基础会员等级",
                min_points=0,
                min_spend=0.0,
                discount_rate=1.0
            )
            
            vip_level = MemberLevel(
                name="VIP会员",
                description="消费满1000元或积分达500自动升级",
                min_points=500,
                min_spend=1000.0,
                discount_rate=0.95
            )
            
            db.session.add(default_level)
            db.session.add(vip_level)
            db.session.commit()
            print("已添加默认会员等级")
        
        # 创建一些默认用户字段定义
        if not UserFieldDefinition.query.first():
            fields = [
                UserFieldDefinition(
                    field_key="profession",
                    field_name="职业",
                    field_type="text",
                    is_required=False,
                    is_visible=True,
                    display_order=1
                ),
                UserFieldDefinition(
                    field_key="interests",
                    field_name="兴趣爱好",
                    field_type="text",
                    is_required=False,
                    is_visible=True,
                    display_order=2
                ),
                UserFieldDefinition(
                    field_key="education",
                    field_name="学历",
                    field_type="select",
                    is_required=False,
                    is_visible=True,
                    display_order=3,
                    options='["高中及以下", "大专", "本科", "硕士", "博士及以上"]'
                )
            ]
            
            for field in fields:
                db.session.add(field)
            
            db.session.commit()
            print("已添加默认用户字段定义")
        
        print("数据库更新完成")

if __name__ == "__main__":
    # 备份数据库
    if os.path.exists('app.db') and not os.path.exists('app.db.backup'):
        import shutil
        shutil.copy2('app.db', 'app.db.backup')
        print("已备份数据库到 app.db.backup")
    
    # 执行更新
    update_database() 