#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品路由模块 - 基于数据库和库存管理
"""

import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import re
from unicodedata import normalize
from datetime import datetime

from models import db, Product, ProductStock, StockLog, ProductCategory

# 创建产品蓝图
product_bp = Blueprint('product_api', __name__, url_prefix='/api/products')

# --- Helper Functions --- 

def _slugify(text: str) -> str:
    """生成安全的 slug，用于文件前缀"""
    if not text:
        return 'product'
    text = normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9_\-]+', '_', text).strip('_ ').lower()
    return text or 'product'

def _save_uploaded_images(files, product_name: str):
    """保存上传的图片文件"""
    saved_paths = []
    upload_dir = current_app.config['PRODUCT_IMG_DIR']
    slug = _slugify(product_name)
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

    for idx, file in enumerate(files, start=1):
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext not in allowed_extensions:
                current_app.logger.warning(f"Skipping file with disallowed extension: {filename}")
                continue
            
            # 生成安全且唯一的文件名
            unique_filename = f"{slug}_{idx}{ext}"
            save_path = os.path.join(upload_dir, unique_filename)
            
            # 处理潜在的文件名冲突
            counter = 1
            while os.path.exists(save_path):
                unique_filename = f"{slug}_{idx}_{counter}{ext}"
                save_path = os.path.join(upload_dir, unique_filename)
                counter += 1
                
            try:
                file.save(save_path)
                # 返回相对于 UPLOADS_DIR 的路径，供前端访问
                relative_path = os.path.join('uploads', 'products', unique_filename).replace('\\', '/') # 保证斜杠方向
                saved_paths.append(f"/{relative_path}")
            except Exception as e:
                current_app.logger.error(f"Error saving file {unique_filename}: {e}")
                # 可以选择抛出异常或跳过此文件
    return saved_paths

def _log_stock_change(product_id, change_type, change_amount, order_id=None, admin_id=None, remark=None):
    """记录库存变动日志"""
    try:
        log_entry = StockLog(
            product_id=product_id,
            change_type=change_type,
            change_amount=change_amount,
            order_id=order_id,
            admin_id=admin_id,
            remark=remark
        )
        db.session.add(log_entry)
        # 注意：这里不 commit，由调用者负责事务提交
    except Exception as e:
        current_app.logger.error(f"Failed to log stock change for product {product_id}: {e}")
        # 考虑是否需要回滚或发出警报

# --- 库存操作核心逻辑 (内部函数, 后续集成到订单流程) ---

def _prelock_stock(product_id, quantity, order_id=None):
    """下单预扣库存 (悲观锁模拟)
    注意：SQLite 的并发锁机制有限，这里的 for_update 效果不如 MySQL/PostgreSQL。
    在高并发场景下，需要更健壮的机制或切换数据库。
    """
    if quantity <= 0:
        return False, "数量必须为正数"

    try:
        stock = ProductStock.query.with_for_update().filter_by(product_id=product_id).first()
        
        if not stock:
            return False, "库存记录不存在"
            
        if stock.available_stock < quantity:
            return False, "可用库存不足"
            
        stock.available_stock -= quantity
        stock.prelock_stock += quantity
        
        _log_stock_change(product_id, 1, -quantity, order_id=order_id, remark=f"订单 {order_id} 预扣")
        
        # 由调用者 commit
        return True, "预扣成功"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Prelock stock failed for product {product_id}: {e}")
        return False, "库存操作失败，请重试"

def _confirm_stock_deduction(product_id, quantity, order_id=None):
    """支付成功，确认扣减库存"""
    if quantity <= 0:
        return False, "数量必须为正数"

    try:
        stock = ProductStock.query.with_for_update().filter_by(product_id=product_id).first()
        
        if not stock:
            return False, "库存记录不存在"
            
        if stock.prelock_stock < quantity:
            # 预扣库存不足，可能流程有问题或数据不一致
            current_app.logger.warning(f"Confirm stock deduction issue: prelock stock {stock.prelock_stock} < requested {quantity} for product {product_id}")
            # 尝试直接扣减总库存和可用库存作为补偿？或者报错？ - 暂时报错
            return False, "预扣库存异常"
            
        stock.prelock_stock -= quantity
        stock.total_stock -= quantity
        
        _log_stock_change(product_id, 2, -quantity, order_id=order_id, remark=f"订单 {order_id} 支付确认")
        
        # 由调用者 commit
        return True, "确认扣减成功"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Confirm stock deduction failed for product {product_id}: {e}")
        return False, "库存操作失败，请重试"

def _release_stock(product_id, quantity, order_id=None, remark="释放库存"):
    """订单取消/超时/退款，释放预扣库存"""
    if quantity <= 0:
        return False, "数量必须为正数"

    try:
        stock = ProductStock.query.with_for_update().filter_by(product_id=product_id).first()
        
        if not stock:
            return False, "库存记录不存在"
            
        if stock.prelock_stock < quantity:
             current_app.logger.warning(f"Release stock issue: prelock stock {stock.prelock_stock} < requested {quantity} for product {product_id}")
             # 预扣量不足，可能重复释放或流程错误，只释放存在的预扣量
             actual_release_quantity = stock.prelock_stock
        else:
                        actual_release_quantity = quantity

        if actual_release_quantity > 0:
            stock.prelock_stock -= actual_release_quantity
            stock.available_stock += actual_release_quantity
        
            _log_stock_change(product_id, 3, actual_release_quantity, order_id=order_id, remark=remark)
        
        # 由调用者 commit
        return True, "释放成功"
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Release stock failed for product {product_id}: {e}")
        return False, "库存操作失败，请重试"

# --- API Routes --- 

@product_bp.route('', methods=['GET'])
def get_products():
    """获取产品列表，包含库存信息，支持筛选"""
    category = request.args.get('category')
    featured = request.args.get('featured')
    # 可以添加分页参数 page, per_page
    
    query = Product.query.options(joinedload(Product.stock))
    
    if category:
        query = query.filter(Product.category == category)
    if featured and featured.lower() == 'true':
        query = query.filter(Product.is_featured == True)
        
    # 添加排序，例如按创建时间降序
    query = query.order_by(Product.created_at.desc())
    
    # 执行查询
    products_db = query.all()
    
    # 格式化输出
    products_list = []
    for p in products_db:
        stock_info = p.stock
        products_list.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category_id": p.category_id,
            "category_name": p.category.name if p.category else None,
            "images": p.images or [],
            "is_featured": p.is_featured,
            "warning_stock": p.warning_stock,
            "total_stock": stock_info.total_stock if stock_info else 0,
            "available_stock": stock_info.available_stock if stock_info else 0,
            "prelock_stock": stock_info.prelock_stock if stock_info else 0,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None
        })
        
    return jsonify({"products": products_list})

@product_bp.route('/<int:pid>', methods=['GET'])
def get_product_detail(pid: int):
    """获取单个产品详情，包含库存信息"""
    product = Product.query.options(joinedload(Product.stock)).get(pid)
    
    if not product:
        return jsonify({"error": "产品不存在"}), 404
        
    stock_info = product.stock
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "images": product.images or [],
        "is_featured": product.is_featured,
        "warning_stock": product.warning_stock,
        "total_stock": stock_info.total_stock if stock_info else 0,
        "available_stock": stock_info.available_stock if stock_info else 0,
        "prelock_stock": stock_info.prelock_stock if stock_info else 0,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None
    }
    return jsonify({"product": product_data})

@product_bp.route('', methods=['POST'])
def add_product():
    """添加新产品 (含初始库存)"""
    # 检查请求方法和内容类型
    if not request.form:
        return jsonify({"error": "表单数据不能为空"}), 400
    
    try:
        # 获取基本信息
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_str = request.form.get('price', '0.0')
        category_id_str = request.form.get('category_id') # 获取分类ID，而不是直接用category
        warning_stock_str = request.form.get('warning_stock', '10') # 默认预警库存为10
        is_featured = request.form.get('is_featured', 'false').lower() == 'true'
        total_stock_str = request.form.get('total_stock', '0')
        
        # --- 数据校验 ---
        if not name:
            return jsonify({"error": "产品名称不能为空"}), 400
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("价格不能为负数")
        except (ValueError, TypeError):
            return jsonify({"error": "价格必须是有效的数字"}), 400
            
        # 转换分类ID
        category_id = None
        if category_id_str:
            try:
                category_id = int(category_id_str)
                # 可以检查分类是否存在
                category = ProductCategory.query.get(category_id)
                if not category:
                    return jsonify({"error": "指定的产品分类不存在"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "分类ID必须是有效的整数"}), 400
                
        try:
            warning_stock = int(warning_stock_str)
            if warning_stock < 0:
                raise ValueError("预警库存不能为负数")
        except (ValueError, TypeError):
            return jsonify({"error": "预警库存必须是有效的整数"}), 400
            
        try:
            total_stock = int(total_stock_str)
            if total_stock < 0:
                 raise ValueError("总库存不能为负数")
        except (ValueError, TypeError):
            return jsonify({"error": "总库存必须是有效的整数"}), 400
        # --- 校验结束 ---

        # 处理图片上传
        image_paths = []
        if 'images' in request.files:
            image_files = request.files.getlist('images')
            if image_files and any(f.filename for f in image_files):
                image_paths = _save_uploaded_images(image_files, name)

        # 创建产品实例
        new_product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id, # 使用category_id而不是category对象
            images=image_paths if image_paths else None,
            is_featured=is_featured,
            warning_stock=warning_stock
        )
        
        # 创建库存实例 (可用库存等于总库存，预扣为0)
        new_stock = ProductStock(
            total_stock=total_stock,
            available_stock=total_stock, # 初始可用库存等于总库存
            prelock_stock=0
        )
        new_product.stock = new_stock # 关联库存
        
        # 添加到数据库会话
        db.session.add(new_product)
        # 注意：ProductStock 会通过 cascade 自动添加
        
        # 提交事务
        db.session.commit()
        
        # 记录初始库存日志 (可选)
        _log_stock_change(new_product.id, 4, total_stock, remark="产品创建，初始化库存")
        db.session.commit() # 提交日志
        
        # 返回成功信息和新产品数据
        stock_info = new_product.stock
        product_data = {
            "id": new_product.id,
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "category_id": new_product.category_id,
            "category_name": new_product.category.name if new_product.category else None,
            "images": new_product.images or [],
            "is_featured": new_product.is_featured,
            "warning_stock": new_product.warning_stock,
            "total_stock": stock_info.total_stock if stock_info else 0,
            "available_stock": stock_info.available_stock if stock_info else 0,
            "prelock_stock": stock_info.prelock_stock if stock_info else 0,
            "created_at": new_product.created_at.isoformat() if new_product.created_at else None,
            "updated_at": new_product.updated_at.isoformat() if new_product.updated_at else None
        }
        return jsonify({"message": "产品添加成功", "product": product_data}), 201
        
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f"Database integrity error on add product: {e}")
        return jsonify({"error": "添加产品时数据库出错，可能存在唯一约束冲突"}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding product: {e}", exc_info=True)
        return jsonify({"error": f"添加产品失败: {str(e)}"}), 500

@product_bp.route('/<int:pid>', methods=['POST', 'PUT']) # 支持 POST 或 PUT 更新
def update_product(pid):
    """更新现有产品及其库存信息"""
    product = Product.query.options(joinedload(Product.stock)).get(pid)
    if not product:
        return jsonify({"error": "产品不存在"}), 404
    
    if not request.form:
        return jsonify({"error": "表单数据不能为空"}), 400

    try:
        # 获取数据 (提供默认值，从现有产品取)
        name = request.form.get('name', product.name).strip()
        description = request.form.get('description', product.description).strip()
        price_str = request.form.get('price', str(product.price))
        category_id_str = request.form.get('category_id', str(product.category_id or ''))
        warning_stock_str = request.form.get('warning_stock', str(product.warning_stock))
        is_featured = request.form.get('is_featured', str(product.is_featured)).lower() == 'true'
        
        # 库存相关字段 (谨慎更新，可能需要更复杂的逻辑)
        total_stock_str = request.form.get('total_stock') # 如果提供了 total_stock，则尝试更新
        
        # --- 数据校验 ---
        if not name:
            return jsonify({"error": "产品名称不能为空"}), 400
        try:
            price = float(price_str)
            if price < 0: raise ValueError("价格不能为负数")
        except (ValueError, TypeError): return jsonify({"error": "价格必须是有效的数字"}), 400
        try:
            warning_stock = int(warning_stock_str)
            if warning_stock < 0: raise ValueError("预警库存不能为负数")
        except (ValueError, TypeError): return jsonify({"error": "预警库存必须是有效的整数"}), 400
        
        new_total_stock = None
        diff_total_stock = 0 # 总库存变动量
        if total_stock_str is not None:
            try:
                new_total_stock = int(total_stock_str)
                if new_total_stock < 0: raise ValueError("总库存不能为负数")
                if product.stock:
                     # 计算总库存变动量，用于调整可用库存
                    if new_total_stock < product.stock.prelock_stock:
                         return jsonify({"error": f"总库存 ({new_total_stock}) 不能小于当前的预扣库存 ({product.stock.prelock_stock})"}), 400
                    diff_total_stock = new_total_stock - product.stock.total_stock
                else:
                    # 如果之前没有库存记录，相当于初始化
                    diff_total_stock = new_total_stock
            except (ValueError, TypeError): return jsonify({"error": "总库存必须是有效的整数"}), 400
        # --- 校验结束 ---

        # 更新产品基础信息
        product.name = name
        product.description = description
        product.price = price
        
        # 处理分类ID
        category_id = None
        if category_id_str:
            try:
                category_id = int(category_id_str)
                # 可以检查分类是否存在
                category = ProductCategory.query.get(category_id)
                if not category:
                    return jsonify({"error": "指定的产品分类不存在"}), 400
                product.category_id = category_id
            except (ValueError, TypeError):
                return jsonify({"error": "分类ID必须是有效的整数"}), 400
        
        product.warning_stock = warning_stock
        product.is_featured = is_featured

        # 处理图片上传 (追加)
        if 'images' in request.files:
            image_files = request.files.getlist('images')
            if image_files and any(f.filename for f in image_files):
                new_image_paths = _save_uploaded_images(image_files, name)
                if not product.images:
                    product.images = []
                # 合并并去重 (如果需要)
                product.images = list(dict.fromkeys(product.images + new_image_paths)) # 简单去重
        
        # 更新库存信息
        stock_changed = False
        if new_total_stock is not None:
            stock = product.stock
            if not stock:
                # 如果没有库存记录，则创建
                stock = ProductStock(product_id=pid, total_stock=new_total_stock, available_stock=new_total_stock, prelock_stock=0)
                product.stock = stock
                db.session.add(stock) # 需要显式添加，因为它不是通过 product cascade 创建的
            else:
                stock.total_stock = new_total_stock
                # 调整可用库存：可用库存增加量 = 总库存增加量
                # 需确保 available_stock 不会变成负数
                stock.available_stock = max(0, stock.available_stock + diff_total_stock)
            stock_changed = True
            
        # 提交事务
        db.session.commit()
        
        # 记录库存变动日志 (如果后台修改了库存)
        if stock_changed and diff_total_stock != 0:
            # 假设由管理员操作，需要获取管理员ID
            # admin_id = get_current_user().id # 示例
            _log_stock_change(pid, 4, diff_total_stock, admin_id=None, remark="后台修改总库存")
            db.session.commit() # 提交日志

        # 返回更新后的产品数据
        stock_info = product.stock
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "category_name": product.category.name if product.category else None,
            "images": product.images or [],
            "is_featured": product.is_featured,
            "warning_stock": product.warning_stock,
            "total_stock": stock_info.total_stock if stock_info else 0,
            "available_stock": stock_info.available_stock if stock_info else 0,
            "prelock_stock": stock_info.prelock_stock if stock_info else 0,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None
        }
        return jsonify({"message": "产品更新成功", "product": product_data})
        
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f"Database integrity error on update product {pid}: {e}")
        return jsonify({"error": "更新产品时数据库出错"}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating product {pid}: {e}", exc_info=True)
        return jsonify({"error": f"更新产品失败: {str(e)}"}), 500

@product_bp.route('/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    """删除产品 (及其关联的库存记录)"""
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "产品不存在"}), 404
    
    try:
        # ProductStock 会通过 cascade="all, delete-orphan" 自动删除
        # StockLog 是否需要删除？通常建议保留日志，或者可以添加一个 is_deleted 标记
        # 如果需要删除日志：
        # StockLog.query.filter_by(product_id=pid).delete()
        
        db.session.delete(product)
        db.session.commit()
        
        # 删除关联的图片文件 (可选，但建议做)
        if product.images:
            upload_dir = current_app.config['UPLOADS_DIR']
            for img_path in product.images:
                try:
                    # 移除开头的斜杠，并构建绝对路径
                    relative_path = img_path.lstrip('/') 
                    abs_path = os.path.join(upload_dir, os.path.dirname(relative_path) ,os.path.basename(relative_path))
                    if os.path.exists(abs_path):
                        os.remove(abs_path)
                        current_app.logger.info(f"Deleted image file: {abs_path}")
                except Exception as e:
                    current_app.logger.error(f"Error deleting image file {img_path}: {e}")
        
        return jsonify({"message": "产品已删除"})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting product {pid}: {e}", exc_info=True)
        return jsonify({"error": f"删除产品失败: {str(e)}"}), 500

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有产品分类 (从数据库获取)"""
    try:
        # 直接查询ProductCategory表，而不是通过Product表
        categories = ProductCategory.query.filter(ProductCategory.is_active == True).order_by(ProductCategory.display_order, ProductCategory.name).all()
        
        # 格式化返回数据
        category_list = [
            {
                "id": c.id,
                "name": c.name,
                "slug": c.slug,
                "description": c.description,
                "parent_id": c.parent_id
            }
            for c in categories
        ]
        return jsonify({"categories": category_list})
    except Exception as e:
        current_app.logger.error(f"Error fetching categories: {e}")
        return jsonify({"error": "获取分类失败"}), 500

# 库存调整API
@product_bp.route('/products/<int:product_id>/adjust-stock', methods=['POST'])
def adjust_product_stock(product_id):
    """
    调整产品库存API
    参数:
    - adjust_total: 总库存调整值 (正数增加, 负数减少)
    - remark: 备注说明
    """
    try:
        data = request.get_json()
        adjust_total = data.get('adjust_total', 0)
        remark = data.get('remark', '后台库存调整')
        
        # 校验参数
        if not isinstance(adjust_total, int):
            return jsonify({'success': False, 'message': '库存调整值必须为整数'}), 400
            
        # 查询产品及库存信息
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': '产品不存在'}), 404
            
        # 获取当前库存记录
        stock = ProductStock.query.filter_by(product_id=product_id).first()
        if not stock:
            # 如果不存在库存记录，创建新记录
            stock = ProductStock(product_id=product_id, total_stock=0, available_stock=0, prelock_stock=0)
            db.session.add(stock)
            
        # 记录调整前的库存状态
        before_total = stock.total_stock
        before_available = stock.available_stock
        before_prelock = stock.prelock_stock
        
        # 调整库存 (总库存和可用库存同时调整)
        # 验证调整后库存不能为负数
        if stock.total_stock + adjust_total < 0:
            return jsonify({'success': False, 'message': '库存不足，无法调整至负数'}), 400
            
        # 更新总库存和可用库存
        stock.total_stock += adjust_total
        stock.available_stock += adjust_total
        
        # 添加库存日志
        stock_log = StockLog(
            product_id=product_id,
            change_type=4,  # 4: 后台修改
            change_amount=adjust_total,
            remark=remark,
            operation_type='admin_adjust',
            before_total=before_total,
            before_available=before_available,
            before_prelock=before_prelock
        )
        db.session.add(stock_log)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': '库存调整成功',
            'data': {
                'product_id': product_id,
                'current_stock': {
                    'total': stock.total_stock,
                    'available': stock.available_stock,
                    'prelock': stock.prelock_stock
                },
                'adjustment': adjust_total
            }
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'数据库错误: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'}), 500 