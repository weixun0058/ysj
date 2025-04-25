from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import Product, StockRecord, db

stock_bp = Blueprint('stock', __name__)

# 库存变更类型常量
CHANGE_TYPE_ORDER_CREATE = 1  # 订单创建
CHANGE_TYPE_ORDER_CANCEL = 2  # 订单取消
CHANGE_TYPE_ORDER_PAID = 3    # 订单支付
CHANGE_TYPE_ADMIN_ADJUST = 4  # 后台调整
CHANGE_TYPE_INITIALIZE = 5    # 初始化

@stock_bp.route('/products/<int:product_id>/stock-logs', methods=['GET'])
def get_product_stock_logs(product_id):
    """获取指定产品的库存变动记录"""
    try:
        # 检查产品是否存在
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'success': False,
                'message': f'ID为{product_id}的产品不存在'
            }), 404
        
        # 查询库存记录
        stock_logs = StockRecord.query.filter_by(product_id=product_id).order_by(
            StockRecord.created_time.desc()
        ).all()
        
        # 转换为JSON格式
        logs_data = []
        for log in stock_logs:
            logs_data.append({
                'id': log.id,
                'product_id': log.product_id,
                'change_type': log.change_type,
                'change_amount': log.change_amount,
                'before_total': log.before_total,
                'before_available': log.before_available,
                'before_prelock': log.before_prelock,
                'remark': log.remark,
                'created_time': log.created_time.isoformat() if log.created_time else None,
                'created_by': log.created_by
            })
        
        return jsonify({
            'success': True,
            'logs': logs_data
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'获取库存记录失败: {str(e)}'
        }), 500

@stock_bp.route('/products/initialize-stock', methods=['POST'])
def initialize_product_stock():
    """初始化产品库存（批量）"""
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({
                'success': False,
                'message': '无效的数据格式，请提供产品库存列表'
            }), 400
        
        results = []
        for item in data:
            product_id = item.get('product_id')
            total_stock = item.get('total_stock', 0)
            
            if not product_id:
                results.append({
                    'success': False,
                    'product_id': None,
                    'message': '缺少产品ID'
                })
                continue
            
            # 检查产品是否存在
            product = Product.query.get(product_id)
            if not product:
                results.append({
                    'success': False,
                    'product_id': product_id,
                    'message': f'ID为{product_id}的产品不存在'
                })
                continue
            
            # 检查是否已有库存记录
            if hasattr(product, 'stock') and product.stock:
                # 已有库存记录，更新库存
                before_total = product.stock.total_stock
                before_available = product.stock.available_stock
                before_prelock = product.stock.prelock_stock
                
                # 计算变化量
                change_amount = total_stock - before_total
                
                # 更新库存
                product.stock.total_stock = total_stock
                product.stock.available_stock = total_stock - before_prelock
                
                # 记录库存变动
                stock_record = StockRecord(
                    product_id=product_id,
                    change_type=CHANGE_TYPE_INITIALIZE,
                    change_amount=change_amount,
                    before_total=before_total,
                    before_available=before_available,
                    before_prelock=before_prelock,
                    remark=item.get('remark', '系统批量初始化库存'),
                    created_time=datetime.now(),
                    created_by=request.headers.get('X-User-ID', 'system')
                )
                db.session.add(stock_record)
            else:
                # 初始化库存记录
                product.initialize_stock(
                    total_stock=total_stock,
                    available_stock=total_stock,
                    prelock_stock=0
                )
                
                # 记录库存变动
                stock_record = StockRecord(
                    product_id=product_id,
                    change_type=CHANGE_TYPE_INITIALIZE,
                    change_amount=total_stock,
                    before_total=0,
                    before_available=0,
                    before_prelock=0,
                    remark=item.get('remark', '系统初始化库存'),
                    created_time=datetime.now(),
                    created_by=request.headers.get('X-User-ID', 'system')
                )
                db.session.add(stock_record)
            
            results.append({
                'success': True,
                'product_id': product_id,
                'current_stock': {
                    'total': product.stock.total_stock,
                    'available': product.stock.available_stock,
                    'prelock': product.stock.prelock_stock
                }
            })
        
        db.session.commit()
        return jsonify({
            'success': True,
            'results': results
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'初始化库存失败: {str(e)}'
        }), 500

@stock_bp.route('/products/batch-adjust-stock', methods=['POST'])
def batch_adjust_product_stock():
    """批量调整产品库存"""
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({
                'success': False,
                'message': '无效的数据格式，请提供产品库存调整列表'
            }), 400
        
        results = []
        for item in data:
            product_id = item.get('product_id')
            adjust_total = item.get('adjust_total', 0)
            
            if not product_id:
                results.append({
                    'success': False,
                    'product_id': None,
                    'message': '缺少产品ID'
                })
                continue
            
            # 检查产品是否存在
            product = Product.query.get(product_id)
            if not product:
                results.append({
                    'success': False,
                    'product_id': product_id,
                    'message': f'ID为{product_id}的产品不存在'
                })
                continue
            
            # 检查是否已有库存记录
            if not hasattr(product, 'stock') or not product.stock:
                # 初始化库存记录
                product.initialize_stock(
                    total_stock=max(0, adjust_total),
                    available_stock=max(0, adjust_total),
                    prelock_stock=0
                )
                
                # 记录库存变动
                stock_record = StockRecord(
                    product_id=product_id,
                    change_type=CHANGE_TYPE_ADMIN_ADJUST,
                    change_amount=max(0, adjust_total),
                    before_total=0,
                    before_available=0,
                    before_prelock=0,
                    remark=item.get('remark', '批量调整库存'),
                    created_time=datetime.now(),
                    created_by=request.headers.get('X-User-ID', 'system')
                )
                db.session.add(stock_record)
                
                results.append({
                    'success': True,
                    'product_id': product_id,
                    'message': '初始化库存成功',
                    'current_stock': {
                        'total': product.stock.total_stock,
                        'available': product.stock.available_stock,
                        'prelock': product.stock.prelock_stock
                    }
                })
                continue
            
            # 已有库存记录，调整库存
            before_total = product.stock.total_stock
            before_available = product.stock.available_stock
            before_prelock = product.stock.prelock_stock
            
            # 检查调整后是否小于0
            if before_total + adjust_total < 0:
                results.append({
                    'success': False,
                    'product_id': product_id,
                    'message': '调整后的库存不能小于0'
                })
                continue
            
            # 更新库存
            product.stock.total_stock = before_total + adjust_total
            # 调整可用库存，确保不会小于0
            new_available = before_available + adjust_total
            product.stock.available_stock = max(0, new_available)
            
            # 记录库存变动
            stock_record = StockRecord(
                product_id=product_id,
                change_type=CHANGE_TYPE_ADMIN_ADJUST,
                change_amount=adjust_total,
                before_total=before_total,
                before_available=before_available,
                before_prelock=before_prelock,
                remark=item.get('remark', '批量调整库存'),
                created_time=datetime.now(),
                created_by=request.headers.get('X-User-ID', 'system')
            )
            db.session.add(stock_record)
            
            results.append({
                'success': True,
                'product_id': product_id,
                'message': '调整库存成功',
                'current_stock': {
                    'total': product.stock.total_stock,
                    'available': product.stock.available_stock,
                    'prelock': product.stock.prelock_stock
                }
            })
        
        db.session.commit()
        return jsonify({
            'success': True,
            'results': results
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'批量调整库存失败: {str(e)}'
        }), 500

# 导出库存变更类型常量
def get_stock_change_types():
    """获取库存变更类型常量"""
    return {
        'ORDER_CREATE': CHANGE_TYPE_ORDER_CREATE,
        'ORDER_CANCEL': CHANGE_TYPE_ORDER_CANCEL,
        'ORDER_PAID': CHANGE_TYPE_ORDER_PAID,
        'ADMIN_ADJUST': CHANGE_TYPE_ADMIN_ADJUST,
        'INITIALIZE': CHANGE_TYPE_INITIALIZE
    } 