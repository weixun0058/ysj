# backend/news_routes.py
from flask import Blueprint, jsonify, request, abort
from models import db, NewsArticle
# 导入 User 模型和 JWT 装饰器 (未来用于权限控制)
from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity 
import sys # 导入 sys 用于打印到 stderr

news_bp = Blueprint('news', __name__, url_prefix='/api')

@news_bp.route('/news', methods=['GET'])
def get_news_list():
    # 获取分页参数，默认为第 1 页，每页 10 条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    print(f"[DEBUG] get_news_list called. Requesting page: {page}, per_page: {per_page}", file=sys.stderr)

    # 查询已发布的文章，按发布日期降序排列，并进行分页
    pagination = NewsArticle.query.filter_by(is_published=True)\
                                   .order_by(NewsArticle.publish_date.desc())\
                                   .paginate(page=page, per_page=per_page, error_out=False)

    articles = pagination.items
    # --- 添加调试打印 --- 
    print(f"[DEBUG] Articles retrieved from DB: {articles}", file=sys.stderr)
    # --- 调试打印结束 --- 

    # 准备返回的数据结构
    news_data = [
        {
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            # 考虑是否需要返回简短摘要，而不是完整内容
            # 'excerpt': generate_excerpt(article.content, 150), # 假设有生成摘要的函数
            'publish_date': article.publish_date.isoformat() # 返回 ISO 格式日期字符串
        } for article in articles
    ]

    # --- 添加调试打印 --- 
    print(f"[DEBUG] Serialized news_data to be returned: {news_data}", file=sys.stderr)
    # --- 调试打印结束 --- 

    return jsonify({
        'news': news_data,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'total_items': pagination.total
    })

@news_bp.route('/news/<string:slug>', methods=['GET'])
def get_news_detail(slug):
    # 根据 slug 查询已发布的文章，如果找不到则返回 404
    article = NewsArticle.query.filter_by(slug=slug, is_published=True).first_or_404()

    # 准备返回的详细数据
    article_data = {
        'id': article.id,
        'title': article.title,
        'slug': article.slug,
        'content': article.content, # 返回完整内容
        'publish_date': article.publish_date.isoformat(),
        'updated_at': article.updated_at.isoformat()
        # 'author_name': article.author.username if article.author else 'N/A' # 如果有关联作者
    }
    return jsonify(article_data)

@news_bp.route('/news', methods=['POST'])
# @jwt_required() # <-- TODO: 添加权限控制，只允许管理员操作
def create_news_article():
    # TODO: 检查当前用户是否有创建权限
    # current_user_id = get_jwt_identity()
    # user = User.query.get(current_user_id)
    # if not user or not user.is_admin: # 假设 User 模型有 is_admin 字段
    #     return jsonify({"error": "权限不足"}), 403

    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "标题和内容不能为空"}), 400

    title = data['title']
    content = data['content']
    slug_provided = data.get('slug') # 可选地允许前端提供 slug

    # 创建 NewsArticle 实例，slug 会在 __init__ 中自动生成（如果未提供）
    try:
        new_article = NewsArticle(title=title, content=content, slug=slug_provided)
        db.session.add(new_article)
        db.session.commit()
        # 返回新创建的文章信息，特别是生成的 slug
        return jsonify({
            'message': '文章创建成功',
            'id': new_article.id,
            'title': new_article.title,
            'slug': new_article.slug 
        }), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        # 在实际应用中应该记录错误日志 log.error(f"Error creating news article: {e}")
        # 检查是否因为 slug 重复导致 (虽然模型里有处理，但以防万一)
        if 'UNIQUE constraint failed: news_article.slug' in str(e):
             return jsonify({"error": "生成文章标识(slug)时发生冲突，请尝试修改标题或手动提供一个唯一的标识"}), 409
        return jsonify({"error": "创建文章失败，请稍后重试"}), 500

# 管理员 API 路由 - 获取所有文章（包括草稿）
@news_bp.route('/admin/news', methods=['GET'])
@jwt_required()
def admin_get_all_news():
    # 检查用户权限
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '', type=str)
    
    # 构建基础查询
    query = NewsArticle.query
    
    # 如果有搜索查询，添加过滤条件
    if search_query:
        query = query.filter(NewsArticle.title.ilike(f'%{search_query}%'))
    
    # 按发布日期降序排序并分页
    pagination = query.order_by(NewsArticle.publish_date.desc())\
                      .paginate(page=page, per_page=per_page, error_out=False)
    
    # 准备返回数据
    articles_data = [
        {
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'is_published': article.is_published,
            'publish_date': article.publish_date.isoformat(),
            'updated_at': article.updated_at.isoformat()
        } for article in pagination.items
    ]
    
    return jsonify({
        'articles': articles_data,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    })

# 管理员 API 路由 - 获取单篇文章详情（草稿也可以）
@news_bp.route('/admin/news/<int:article_id>', methods=['GET'])
@jwt_required()
def admin_get_news_detail(article_id):
    # 检查用户权限
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    # 查询文章
    article = NewsArticle.query.get_or_404(article_id)
    
    # 准备返回数据
    article_data = {
        'id': article.id,
        'title': article.title,
        'slug': article.slug,
        'content': article.content,
        'is_published': article.is_published,
        'publish_date': article.publish_date.isoformat(),
        'updated_at': article.updated_at.isoformat()
    }
    
    return jsonify(article_data)

# 管理员 API 路由 - 更新文章
@news_bp.route('/admin/news/<int:article_id>', methods=['PUT'])
@jwt_required()
def admin_update_news(article_id):
    # 检查用户权限
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    # 获取JSON数据
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400
    
    # 查询文章
    article = NewsArticle.query.get_or_404(article_id)
    
    # 更新文章字段
    if 'title' in data:
        article.title = data['title']
    if 'content' in data:
        article.content = data['content']
    if 'slug' in data and data['slug']:
        # 检查新的slug是否已存在
        existing = NewsArticle.query.filter(NewsArticle.slug == data['slug'], 
                                          NewsArticle.id != article_id).first()
        if existing:
            return jsonify({"error": "文章标识(slug)已被使用"}), 409
        article.slug = data['slug']
    if 'is_published' in data:
        article.is_published = bool(data['is_published'])
    
    try:
        db.session.commit()
        # 返回更新后的文章数据
        return jsonify({
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'is_published': article.is_published,
            'updated_at': article.updated_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新文章失败: {str(e)}"}), 500

# 管理员 API 路由 - 删除文章
@news_bp.route('/admin/news/<int:article_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_news(article_id):
    # 检查用户权限
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    # 查询文章
    article = NewsArticle.query.get_or_404(article_id)
    
    try:
        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": "文章已成功删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除文章失败: {str(e)}"}), 500

# 管理员 API 路由 - 切换文章发布状态
@news_bp.route('/admin/news/<int:article_id>/toggle-publish', methods=['PUT'])
@jwt_required()
def admin_toggle_publish_status(article_id):
    # 检查用户权限
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({"error": "权限不足"}), 403
    
    # 查询文章
    article = NewsArticle.query.get_or_404(article_id)
    
    # 切换发布状态
    article.is_published = not article.is_published
    
    try:
        db.session.commit()
        status_msg = "已发布" if article.is_published else "已设为草稿"
        return jsonify({
            "message": f"文章{status_msg}",
            "is_published": article.is_published
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新文章状态失败: {str(e)}"}), 500

# 可选：简单的摘要生成函数 (非常基础)
# def generate_excerpt(content, length=150):
#     if len(content) <= length:
#         return content
#     return content[:length] + '...' 