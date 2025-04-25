BEGIN TRANSACTION;
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
);
INSERT INTO user_new SELECT * FROM user;
DROP TABLE user;
ALTER TABLE user_new RENAME TO user;
CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE UNIQUE INDEX ix_user_username ON user (username);
CREATE UNIQUE INDEX ix_user_phone ON user (phone);
COMMIT; 