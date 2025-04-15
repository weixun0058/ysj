# 壹世健官方网站项目

本项目旨在为高端蜂蜜品牌"壹世健"构建官方网站。

## 技术栈

* **前端:** HTML, CSS, JavaScript (根据 PRD，未来可能采用 Vue.js)
* **后端:** Python / Flask
* **数据库:** SQLite (根据 PRD)

## 项目结构

``` plaintext
/
|-- backend/                # 后端 Flask 应用
|   |-- app.py              # Flask 应用主文件
|   |-- requirements.txt    # Python 依赖
|-- index.html              # 前端主页
|-- README.md               # 项目说明文件
|-- 文档/                   # 项目相关文档
|   |-- ...
```

## 设置与运行

1. **克隆仓库** (如果需要)

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **设置并激活 Python 虚拟环境** (推荐)

    ```bash
    # 在项目根目录
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **安装后端依赖**

    ```bash
    # 确保你在项目根目录，或者根据需要 cd 到 backend 目录
    # 如果在根目录执行:
    pip install -r backend/requirements.txt
    # 如果在 backend 目录执行:
    # pip install -r requirements.txt
    ```

4. **运行后端 Flask 服务器**

    ```bash
    # 确保你在项目根目录
    python backend/app.py
    # 或者 cd 到 backend 目录后运行:
    # python app.py
    ```

5. **访问网站**
    打开浏览器，访问 `http://127.0.0.1:5000` 或 `http://localhost:5000`。

## 文档

详细的需求、设计和规范请参见 `文档/` 目录下的 Markdown 文件。
