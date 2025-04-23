#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品路由模块 - 简化版
"""

import os
import json
from flask import Blueprint, jsonify, request, current_app

# 创建产品蓝图，使用新的名称空间避免冲突
product_bp = Blueprint('product_api', __name__, url_prefix='/api/products_v1')

# 产品数据存储
PRODUCTS = []
JSON_PATH = None 
IMG_DIR = None

def init_product_routes(app):
    """初始化产品路由及相关配置"""
    global JSON_PATH, IMG_DIR, PRODUCTS
    
    # 注册蓝图
    app.register_blueprint(product_bp)
    
    # 设置文件路径
    BASE_DIR = os.path.abspath(app.static_folder)
    IMG_DIR = os.path.join(BASE_DIR, 'img', 'products')
    JSON_PATH = os.path.join(BASE_DIR, 'products.json')
    
    # 确保产品图片目录存在
    os.makedirs(IMG_DIR, exist_ok=True)
    
    # 加载产品数据
    load_products()

def load_products():
    """从JSON文件加载产品数据"""
    global PRODUCTS
    
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as fp:
            PRODUCTS = json.load(fp)
    else:
        # 默认示例产品
        PRODUCTS = [{
            "id": 1,
            "name": "天山黑蜂原蜜 500g",
            "description": "源自新疆伊犁天山北麓黑蜂采集的高原原蜜。",
            "price": 128.0,
            "images": ["/api_static/img/products/honey500.png"],
            "category": "蜂蜜",
            "stock": 100,
            "specifications": "500g/瓶",
            "is_featured": True
        }]
        save_products()

def save_products():
    """将产品数据保存到JSON文件"""
    with open(JSON_PATH, 'w', encoding='utf-8') as fp:
        json.dump(PRODUCTS, fp, ensure_ascii=False, indent=2)

# 简化API路由定义 - 仅包含基本的获取产品列表功能，无需认证

@product_bp.route('', methods=['GET'])
def get_products():
    """获取产品列表，支持分类筛选和推荐标记筛选"""
    category = request.args.get('category')
    featured = request.args.get('featured')
    
    result = PRODUCTS
    
    # 根据分类筛选
    if category:
        result = [p for p in result if p.get('category') == category]
    
    # 根据推荐标记筛选
    if featured and featured.lower() == 'true':
        result = [p for p in result if p.get('is_featured')]
    
    return jsonify({"products": result})

@product_bp.route('/<int:pid>', methods=['GET'])
def get_product_detail(pid: int):
    """获取单个产品详情"""
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        return jsonify({"error": "产品不存在"}), 404
    return jsonify({"product": product})

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有产品分类"""
    categories = sorted(set(p.get('category') for p in PRODUCTS if p.get('category')))
    return jsonify({"categories": categories}) 