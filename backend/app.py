from flask import Flask, send_from_directory, jsonify, request
import os
from werkzeug.utils import secure_filename
import json
from urllib.parse import urljoin
from unicodedata import normalize
import re
# 加载.env文件中的环境变量
from dotenv import load_dotenv
load_dotenv()  # 从.env文件加载环境变量
# 从 models 导入 db 和 migrate 实例
from models import db, migrate 
# 导入 JWT 扩展
from flask_jwt_extended import JWTManager
import secrets # 用于生成安全的密钥
from flask_cors import CORS # 导入 CORS

# 创建 Flask 应用实例
app = Flask(__name__, static_folder='../', static_url_path='')

# --- 配置 CORS ---
# 最简单的配置：允许所有来源访问所有路由
# 在生产中应指定具体的 origins
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}}) # 应用 CORS 配置，允许 /api/* 下的所有路由跨域，并允许携带凭证
# --- CORS 配置结束 ---

# --- JWT 配置 ---
# 从环境变量或默认生成密钥
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
jwt = JWTManager(app)
# --- JWT 配置结束 ---

# --- 数据库配置 ---
basedir = os.path.abspath(os.path.dirname(__file__))
# 设置数据库 URI，这里使用 SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
# 关闭 SQLAlchemy 的事件通知系统，如果不使用可以节省资源
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy 和 Migrate，关联 app
db.init_app(app)
migrate.init_app(app, db)
# --- 数据库配置结束 ---

# --- 注册蓝图 ---
# 导入认证蓝图
from auth_routes import auth_bp
app.register_blueprint(auth_bp)
# 导入资讯蓝图
from news_routes import news_bp
app.register_blueprint(news_bp)
# 导入用户管理蓝图
from user_routes import user_bp
app.register_blueprint(user_bp)
# --- 蓝图注册结束 ---

# 路径设置
BASE_DIR = os.path.abspath(app.static_folder)  # 项目根目录
IMG_DIR = os.path.join(BASE_DIR, 'img', 'products')
JSON_PATH = os.path.join(BASE_DIR, 'products.json')

os.makedirs(IMG_DIR, exist_ok=True)

# 加载产品数据
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, 'r', encoding='utf-8') as fp:
        PRODUCTS = json.load(fp)
else:
    PRODUCTS = []

# --- 现有 PRODUCTS 示例保留如为空时可添加 ---
if not PRODUCTS:
    PRODUCTS.extend([
        {
            "id": 1,
            "name": "天山黑蜂原蜜 500g",
            "description": "源自新疆伊犁天山北麓黑蜂采集的高原原蜜。",
            "price": 128.0,
            "images": ["/api_static/img/products/honey500.png"],
            "category": "蜂蜜"
        }
    ])

def _slugify(text: str) -> str:
    """生成安全的 slug，用于文件前缀"""
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_').lower()
    return text or 'product'

# 将重复的保存逻辑封装

def _save_uploaded_images(files, product_name: str):
    saved_paths = []
    slug = _slugify(product_name)
    for idx, file in enumerate(files, start=1):
        if not file.filename:
            continue
        ext = os.path.splitext(secure_filename(file.filename))[1]
        filename = f"{slug}_{idx}{ext}"
        save_path = os.path.join(IMG_DIR, filename)
        # 避免冲突追加递增号
        dup = 1
        while os.path.exists(save_path):
            filename = f"{slug}_{idx}_{dup}{ext}"
            save_path = os.path.join(IMG_DIR, filename)
            dup += 1
        file.save(save_path)
        saved_paths.append(f"/img/products/{filename}")
    return saved_paths

def _save_products():
    """将 PRODUCTS 列表写入 JSON 文件"""
    with open(JSON_PATH, 'w', encoding='utf-8') as fp:
        json.dump(PRODUCTS, fp, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """
    定义根路由，用于提供 index.html 文件。
    它会从项目根目录（即 backend 目录的上一级）查找 index.html。
    """
    # 使用 send_from_directory 从项目根目录提供 index.html
    # os.path.abspath(os.path.join(app.static_folder)) 获取项目根目录的绝对路径
    return send_from_directory(os.path.abspath(app.static_folder), 'index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({"products": PRODUCTS})

@app.route('/api/products', methods=['POST'])
def add_product():
    """接收表单和图片，新增产品"""
    # 数据字段
    name = (request.form.get('name') or '').strip()
    description = (request.form.get('description') or '').strip()
    price = float(request.form.get('price') or 0)
    category = (request.form.get('category') or '').strip()

    if not name or price <= 0:
        return jsonify({"error": "名称和价格必填且价格>0"}), 400

    # 保存图片
    images = _save_uploaded_images(request.files.getlist('images'), name)

    new_id = max((p['id'] for p in PRODUCTS), default=0) + 1
    PRODUCTS.append({
        "id": new_id,
        "name": name,
        "description": description,
        "price": price,
        "images": images,
        "category": category
    })
    _save_products()
    return jsonify({"message": "产品已添加", "id": new_id})

@app.route('/api/products/<int:pid>', methods=['GET'])
def get_product_detail(pid: int):
    """根据 ID 返回单个产品详情"""
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return jsonify({"error": "产品不存在"}), 404
    return jsonify({"product": product})

@app.route('/api/products/<int:pid>', methods=['POST'])
def update_product(pid: int):
    """更新已有产品信息，表单同 add_product"""
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return jsonify({"error": "产品不存在"}), 404

    name = (request.form.get('name') or '').strip()
    description = (request.form.get('description') or '').strip()
    price = request.form.get('price')
    category = (request.form.get('category') or '').strip()

    if name:
        product['name'] = name
    if description:
        product['description'] = description
    if price is not None and price != '':
        product['price'] = float(price)
    if category:
        product['category'] = category

    # 新上传的图片追加
    if request.files.getlist('images'):
        product.setdefault('images', []).extend(_save_uploaded_images(request.files.getlist('images'), product.get('name', 'product')))

    _save_products()
    return jsonify({"message": "产品已更新"})

@app.route('/api/products/<int:pid>/delete', methods=['POST'])
def delete_product(pid: int):
    """删除产品"""
    global PRODUCTS
    new_list = [p for p in PRODUCTS if p['id'] != pid]
    if len(new_list) == len(PRODUCTS):
        return jsonify({"error": "产品不存在"}), 404
    PRODUCTS = new_list
    _save_products()
    return jsonify({"message": "产品已删除"})

@app.route('/admin/upload-product')
def upload_product_form():
    """HTML 页面: 新增产品表单 + 现有产品编辑"""
    rows = []
    for p in PRODUCTS:
        rows.append(f"""
        <details style='margin-top:20px;'>
          <summary><strong>编辑: {p['name']} (ID:{p['id']})</strong></summary>
          <form action='/api/products/{p['id']}' method='post' enctype='multipart/form-data' style='margin-top:10px;'>
            名称: <input type='text' name='name' value='{p['name']}' required><br><br>
            描述: <textarea name='description' rows='3' cols='40'>{p['description']}</textarea><br><br>
            价格: <input type='number' step='0.01' name='price' value='{p['price']}' required><br><br>
            分类: <input type='text' name='category' value='{p.get('category','')}'><br><br>
            新增图片: <input type='file' name='images' multiple><br><br>
            <button type='submit'>更新</button>
          </form>
          <form action='/api/products/{p['id']}/delete' method='post' onsubmit="return confirm('确定删除?');" style='margin-top:5px;'>
            <button type='submit' style='color:red;'>删除</button>
          </form>
          <p>已有图片:</p>
          {''.join(f'<img src="{img}" alt="img" style="height:80px;margin-right:10px;">' for img in p.get('images', []))}
        </details>
        """)

    html = f"""
    <!DOCTYPE html>
    <html lang='zh-CN'>
    <head><meta charset='utf-8'><title>产品管理</title></head>
    <body>
      <h1>上传新产品</h1>
      <form action='/api/products' method='post' enctype='multipart/form-data'>
        名称: <input type='text' name='name' required><br><br>
        描述: <textarea name='description' rows='4' cols='40'></textarea><br><br>
        价格: <input type='number' step='0.01' name='price' required><br><br>
        分类: <input type='text' name='category'><br><br>
        图片: <input type='file' name='images' multiple><br><br>
        <button type='submit'>提交</button>
      </form>
      <hr>
      <h2>编辑已有产品</h2>
      {''.join(rows)}
    </body></html>"""
    return html

if __name__ == '__main__':
    # 启动 Flask 开发服务器
    # host='0.0.0.0' 使服务器可以从本地网络访问
    # debug=True 开启调试模式，方便开发
    app.run(host='0.0.0.0', port=5000, debug=True) 