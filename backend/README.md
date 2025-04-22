# 后端开发指南

## 环境设置

### Linux/macOS 环境

1. 设置虚拟环境（首次使用或需要重建环境时）：
   ```bash
   ./setup_venv.sh
   ```

2. 激活虚拟环境：
   ```bash
   source venv/bin/activate
   ```

3. 启动Flask服务器：
   ```bash
   ./start_flask.sh
   ```
   
   如需同时更新依赖：
   ```bash
   ./start_flask.sh update
   ```

### Windows 环境

1. 设置虚拟环境（首次使用或需要重建环境时）：
   ```
   setup_venv.bat
   ```

2. 激活虚拟环境：
   ```
   venv\Scripts\activate.bat
   ```

3. 启动Flask服务器：
   ```
   start_flask.bat
   ```
   
   如需同时更新依赖：
   ```
   start_flask.bat update
   ```

## 项目结构

- `app.py`: 应用程序的入口点
- `models.py`: 数据库模型定义
- `auth_routes.py`: 认证相关的API路由
- `news_routes.py`: 新闻资讯相关的API路由
- `user_routes.py`: 用户管理相关的API路由
- `migrations/`: 数据库迁移文件
- `venv/`: Python虚拟环境（由setup_venv脚本创建）
- `requirements.txt`: Python依赖包列表

## 开发工作流

1. 修改模型后，创建新的数据库迁移：
   ```bash
   flask db migrate -m "描述你的更改"
   ```

2. 应用数据库迁移：
   ```bash
   flask db upgrade
   ```

3. API访问：
   - 所有API路由都以`/api`开头
   - 认证路由：`/api/auth/*`
   - 用户管理路由：`/api/user/*`
   - 新闻资讯路由：`/api/news/*`

4. 测试API：
   ```bash
   python test_api.py
   ``` 