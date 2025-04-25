from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, BrandCollaboration, CollaborationProject, CollaborationProduct, CollaborationActivity
from backend.utils.admin_auth import admin_required
from sqlalchemy import desc
import json
import datetime

# 创建品牌联名合作蓝图
collaboration_bp = Blueprint('collaboration', __name__, url_prefix='/api/collaboration')

# 允许的状态值列表
ALLOWED_STATUS = ['pending', 'processing', 'approved', 'rejected', 'completed']

# 提交联名合作申请
@collaboration_bp.route('/submit', methods=['POST'])
def submit_collaboration():
    """提交品牌联名合作申请"""
    data = request.json
    
    # 验证必填字段
    required_fields = ['company_name', 'industry', 'contact_name', 'email', 'phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'status': 'error', 'message': f'缺少必填字段: {field}'}), 400
    
    # 处理产品类型，将列表转为JSON字符串存储
    product_types = data.get('product_types', [])
    if isinstance(product_types, list):
        product_types = json.dumps(product_types)
    
    # 创建申请记录
    new_collaboration = BrandCollaboration(
        company_name=data.get('company_name'),
        industry=data.get('industry'),
        contact_name=data.get('contact_name'),
        position=data.get('position'),
        email=data.get('email'),
        phone=data.get('phone'),
        product_types=product_types,
        cooperation_type=data.get('cooperation_type'),
        expected_volume=data.get('expected_volume'),
        expected_start_date=data.get('expected_start_date'),
        details=data.get('details')
    )
    
    try:
        db.session.add(new_collaboration)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '合作申请提交成功',
            'id': new_collaboration.id
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"提交合作申请失败: {str(e)}")
        return jsonify({'status': 'error', 'message': '提交失败，请稍后再试'}), 500

# 获取所有合作申请（管理员）
@collaboration_bp.route('/all', methods=['GET'])
@jwt_required()
@admin_required
def get_all_collaborations():
    """获取所有联名合作申请（管理员用）"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    query = BrandCollaboration.query
    
    # 按状态筛选
    if status and status in ALLOWED_STATUS:
        query = query.filter_by(status=status)
    
    # 按提交时间倒序排列
    query = query.order_by(desc(BrandCollaboration.created_at))
    
    # 分页
    paginated = query.paginate(page=page, per_page=per_page)
    
    collaborations = []
    for collab in paginated.items:
        # 处理产品类型，将JSON字符串转为列表
        product_types = []
        if collab.product_types:
            try:
                product_types = json.loads(collab.product_types)
            except:
                product_types = []
                
        collaborations.append({
            'id': collab.id,
            'company_name': collab.company_name,
            'industry': collab.industry,
            'contact_name': collab.contact_name,
            'email': collab.email,
            'phone': collab.phone,
            'product_types': product_types,
            'cooperation_type': collab.cooperation_type,
            'expected_volume': collab.expected_volume,
            'expected_start_date': collab.expected_start_date,
            'status': collab.status,
            'is_priority': collab.is_priority,
            'created_at': collab.created_at.strftime('%Y-%m-%d %H:%M:%S') if collab.created_at else None,
            'updated_at': collab.updated_at.strftime('%Y-%m-%d %H:%M:%S') if collab.updated_at else None
        })
    
    return jsonify({
        'status': 'success',
        'data': {
            'collaborations': collaborations,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }
    })

# 获取单个合作申请详情（管理员）
@collaboration_bp.route('/<int:collab_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_collaboration(collab_id):
    """获取指定合作申请详情"""
    collab = BrandCollaboration.query.get_or_404(collab_id)
    
    # 处理产品类型，将JSON字符串转为列表
    product_types = []
    if collab.product_types:
        try:
            product_types = json.loads(collab.product_types)
        except:
            product_types = []
    
    # 获取关联的项目
    projects = []
    for project in collab.projects:
        projects.append({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'status': project.status,
            'created_at': project.created_at.strftime('%Y-%m-%d %H:%M:%S') if project.created_at else None
        })
    
    # 构建响应数据
    collaboration_data = {
        'id': collab.id,
        'company_name': collab.company_name,
        'industry': collab.industry,
        'contact_name': collab.contact_name,
        'position': collab.position,
        'email': collab.email,
        'phone': collab.phone,
        'product_types': product_types,
        'cooperation_type': collab.cooperation_type,
        'expected_volume': collab.expected_volume,
        'expected_start_date': collab.expected_start_date,
        'details': collab.details,
        'status': collab.status,
        'is_priority': collab.is_priority,
        'admin_notes': collab.admin_notes,
        'created_at': collab.created_at.strftime('%Y-%m-%d %H:%M:%S') if collab.created_at else None,
        'updated_at': collab.updated_at.strftime('%Y-%m-%d %H:%M:%S') if collab.updated_at else None,
        'projects': projects
    }
    
    return jsonify({
        'status': 'success',
        'data': collaboration_data
    })

# 更新合作申请状态（管理员）
@collaboration_bp.route('/<int:collab_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_collaboration_status(collab_id):
    """更新合作申请状态"""
    collab = BrandCollaboration.query.get_or_404(collab_id)
    data = request.json
    
    # 验证状态值
    new_status = data.get('status')
    if not new_status or new_status not in ALLOWED_STATUS:
        return jsonify({'status': 'error', 'message': f'无效的状态值，允许的值为: {", ".join(ALLOWED_STATUS)}'}), 400
    
    # 更新状态
    collab.status = new_status
    
    # 更新管理员备注（如果提供）
    if 'admin_notes' in data:
        collab.admin_notes = data.get('admin_notes')
    
    # 更新优先级（如果提供）
    if 'is_priority' in data:
        collab.is_priority = bool(data.get('is_priority'))
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '状态更新成功',
            'current_status': collab.status
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新合作申请状态失败: {str(e)}")
        return jsonify({'status': 'error', 'message': '更新失败，请稍后再试'}), 500

# 创建合作项目（管理员）
@collaboration_bp.route('/<int:collab_id>/projects', methods=['POST'])
@jwt_required()
@admin_required
def create_project(collab_id):
    """为合作申请创建项目"""
    collab = BrandCollaboration.query.get_or_404(collab_id)
    data = request.json
    
    # 验证必填字段
    if not data.get('name'):
        return jsonify({'status': 'error', 'message': '项目名称不能为空'}), 400
    
    # 创建项目
    project = CollaborationProject(
        collaboration_id=collab_id,
        name=data.get('name'),
        description=data.get('description'),
        start_date=datetime.datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None,
        end_date=datetime.datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
        budget=data.get('budget'),
        profit_share_model=data.get('profit_share_model'),
        profit_share_percentage=data.get('profit_share_percentage'),
        status=data.get('status', 'planning')
    )
    
    try:
        db.session.add(project)
        
        # 如果这是第一个项目，将合作申请状态更新为"处理中"
        if collab.status == 'pending':
            collab.status = 'processing'
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '项目创建成功',
            'project_id': project.id
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建项目失败: {str(e)}")
        return jsonify({'status': 'error', 'message': '创建失败，请稍后再试'}), 500

# 其他项目管理路由省略...
# 可根据需要继续添加项目详情、编辑、产品管理、活动管理等相关接口 