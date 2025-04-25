# 塞外本草 / 壹世健 官方网站 - 项目概览

## 1. 项目简介

本项目旨在为"塞外本草"及其旗下高端蜂蜜品牌"壹世健"打造一个集品牌展示、产品销售、会员认养及溯源功能于一体的官方网站。

网站将重点突出产品的核心优势：新疆伊犁的地理标志保护产区、珍稀新疆黑蜂、纯净天山蜜源、原蜜直出无添加工艺，以及独特的蜜蜂认养会员体系。

## 2. 技术栈

* **后端:** Python 3.10+, Flask 3.x, SQLAlchemy, Flask-Migrate, SQLite
* **前端:** Node.js 18+/20+, Vue.js 3.x, Vite, Vue Router 4.x, Pinia, Axios
* **数据库:** SQLite, Redis (缓存/消息队列)
* **基础设施 (生产):** 阿里云 Ubuntu Server, Nginx, Docker (推荐), Gunicorn/uWSGI
* **开发环境:** Windows / Linux / macOS
* **版本控制:** Git (GitHub/GitLab/Gitee)

详细技术栈请参考 `技术栈概览.md`。

## 3. 环境配置与启动

### 3.1 后端 (Flask - `flask-app` 目录)

1. **创建虚拟环境:**

    ```bash
    cd flask-app
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    # source venv/bin/activate
    ```

2. **安装依赖:**

    ```bash
    pip install -r requirements.txt
    ```

3. **配置环境变量:**
    * 复制 `.env.example` 为 `.env`。
    * 修改 `.env` 文件中的配置，特别是数据库连接字符串 (`DATABASE_URL`) 和 `SECRET_KEY`。
4. **数据库初始化/迁移:**

    ```bash
    flask db init # 首次需要
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **启动开发服务器:**

    ```bash
    flask run
    ```

    默认访问: `http://127.0.0.1:5000`

### 3.2 前端 (Vue.js - `vue-app` 目录)

1. **安装依赖:**

    ```bash
    cd vue-app
    npm install # 或者 yarn install / pnpm install
    ```

2. **启动开发服务器:**

    ```bash
    npm run dev # 或者 yarn dev / pnpm dev
    ```

    默认访问: `http://127.0.0.1:5173` (Vite 默认端口，可能不同)

## 4. 项目结构

请参考 `前后端技术规范.md` 中关于项目结构的说明。

## 5. 关键功能模块

* **首页:** 品牌形象展示、核心优势、产品推荐、入口引导。
* **品牌故事:** 图文并茂介绍品牌历史、理念、产地、认证。
* **产品中心:** 商品列表、详情、搜索、购物车、下单支付流程。
* **蜜蜂认养·会员中心:** 认养计划介绍、会员管理、认养信息展示、溯源追踪。
* **动态资讯:** 发布公司新闻、行业知识等。
* **联系我们:** 联系方式、留言表单、地图。
* **后台管理:** 内容、产品、订单、会员、溯源数据管理等。

详细功能需求请参考 `产品需求文档（PRD）.md`。

## 6. 开发规范

请严格遵守 `前后端技术规范.md` 中定义的各项规范，包括版本控制、编码风格、API 设计、测试、文档等。

## 7. 部署说明

(后续补充生产环境部署细节)

## 8. 当前可用的管理入口 (待完善)

以下后端功能已实现基础接口，但目前**缺乏权限控制**，并且没有对应的前端管理界面。可以通过 API 工具或手动访问特定 URL 来进行操作，主要用于开发和测试阶段添加初始数据。

* **创建资讯文章:**
  * **API 端点:** `POST /api/news`
  * **请求体 (JSON):** `{ "title": "文章标题", "content": "文章内容" }`
  * **前端临时入口:** 可通过浏览器直接访问 `http://localhost:5678/admin/news/create` (端口号可能不同) 来使用简单的表单进行创建。

* **管理产品 (增/改/删):**
  * **前端临时管理页面:** 可通过浏览器直接访问 `/admin/upload-product` (基于 Flask 后端直接渲染的简单 HTML 页面) 来进行产品的增删改操作。
  * **涉及 API 端点:**
    * `POST /api/products` (添加产品)
    * `POST /api/products/<int:pid>` (更新产品)
    * `POST /api/products/<int:pid>/delete` (删除产品)

**警告:** 这些入口目前没有安全防护，请勿在生产环境或公开网络中使用。后续需要实现完整的后台管理系统和权限控制。
