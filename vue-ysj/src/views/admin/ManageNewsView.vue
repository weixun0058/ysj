<!-- vue-ysj/src/views/admin/ManageNewsView.vue -->
<template>
  <div class="view-container manage-news-page">
    <h1>文章管理</h1>
    
    <div class="actions-bar">
      <router-link to="/admin/news/create" class="create-btn">
        <i class="fas fa-plus-circle"></i> 发布新文章
      </router-link>
      
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索文章标题..." 
          @input="debounceSearch"
        />
        <i class="fas fa-search"></i>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="articles.length > 0">
      <table class="articles-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>标题</th>
            <th>发布日期</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td>{{ article.id }}</td>
            <td>
              <router-link :to="{ name: 'NewsDetail', params: { slug: article.slug } }" target="_blank">
                {{ article.title }}
              </router-link>
            </td>
            <td>{{ formatDate(article.publish_date) }}</td>
            <td>
              <span :class="['status-badge', article.is_published ? 'published' : 'draft']">
                {{ article.is_published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editArticle(article)" class="edit-btn">
                <i class="fas fa-edit"></i> 编辑
              </button>
              <button @click="togglePublishStatus(article)" :class="['toggle-btn', article.is_published ? 'unpublish' : 'publish']">
                <i :class="article.is_published ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                {{ article.is_published ? '取消发布' : '发布' }}
              </button>
              <button @click="confirmDelete(article)" class="delete-btn">
                <i class="fas fa-trash-alt"></i> 删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页控制 -->
      <div class="pagination" v-if="totalPages > 1">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage <= 1">
          上一页
        </button>
        <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">
          下一页
        </button>
      </div>
    </div>

    <div v-else class="no-articles">
      <p>暂无文章。</p>
      <router-link to="/admin/news/create" class="create-btn">
        发布第一篇文章
      </router-link>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal-dialog">
        <h3>确认删除</h3>
        <p>您确定要删除文章 "{{ articleToDelete?.title }}" 吗？此操作不可恢复。</p>
        <div class="modal-actions">
          <button @click="cancelDelete" class="cancel-btn">取消</button>
          <button @click="deleteArticle" class="confirm-delete-btn">确认删除</button>
        </div>
      </div>
    </div>

    <!-- 成功/错误提示 -->
    <div v-if="actionMessage" :class="['action-message', actionSuccess ? 'success' : 'error']">
      {{ actionMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth'; 
import { getAdminNewsList, toggleNewsPublishStatus, deleteNews } from '../../api/newsApi'; // 导入新API服务

const authStore = useAuthStore(); 
const articles = ref([]);
const loading = ref(true);
const error = ref('');
const currentPage = ref(1);
const totalPages = ref(1);
const searchQuery = ref('');
const searchTimeout = ref(null);
const router = useRouter();
const route = useRoute();

// 删除确认相关
const showDeleteConfirm = ref(false);
const articleToDelete = ref(null);

// 操作反馈
const actionMessage = ref('');
const actionSuccess = ref(true);

// 格式化日期函数
const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 搜索防抖
const debounceSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  searchTimeout.value = setTimeout(() => {
    fetchArticles(1); // 搜索时重置到第一页
  }, 500);
};

// 获取文章列表
const fetchArticles = async (page = 1) => {
  loading.value = true;
  error.value = '';
  try {
    // 使用API服务获取管理员文章列表
    const data = await getAdminNewsList(page, 10, searchQuery.value.trim());
    articles.value = data.articles;
    totalPages.value = data.total_pages;
    currentPage.value = data.current_page;
  } catch (err) {
    console.error('获取文章列表失败:', err);
    error.value = err.response?.data?.error || err.message || '无法加载文章列表，请稍后重试。';
  } finally {
    loading.value = false;
  }
};

// 切换页面
const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    currentPage.value = newPage;
    fetchArticles(newPage);
  }
};

// 编辑文章
const editArticle = (article) => {
  router.push({ name: 'EditNews', params: { id: article.id } });
};

// 切换发布状态
const togglePublishStatus = async (article) => {
  try {
    // 使用API服务切换文章发布状态
    const response = await toggleNewsPublishStatus(article.id);

    // 更新本地文章状态
    const index = articles.value.findIndex(a => a.id === article.id);
    if (index !== -1) {
      articles.value[index].is_published = response.is_published;
    }

    // 显示成功消息
    actionSuccess.value = true;
    actionMessage.value = response.is_published ? '文章已发布' : '文章已设为草稿';
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
  } catch (err) {
    console.error('切换发布状态失败:', err);
    actionSuccess.value = false;
    actionMessage.value = err.response?.data?.error || err.message || '操作失败，请稍后重试';
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
  }
};

// 确认删除
const confirmDelete = (article) => {
  articleToDelete.value = article;
  showDeleteConfirm.value = true;
};

// 取消删除
const cancelDelete = () => {
  showDeleteConfirm.value = false;
  articleToDelete.value = null;
};

// 执行删除
const deleteArticle = async () => {
  try {
    // 使用API服务删除文章
    await deleteNews(articleToDelete.value.id);
    
    // 更新文章列表，删除已删除的文章
    articles.value = articles.value.filter(a => a.id !== articleToDelete.value.id);
    
    // 如果当前页没有文章了，并且不是第一页，则转到上一页
    if (articles.value.length === 0 && currentPage.value > 1) {
      changePage(currentPage.value - 1);
    }
    
    // 关闭确认对话框
    showDeleteConfirm.value = false;
    articleToDelete.value = null;
    
    // 显示成功消息
    actionSuccess.value = true;
    actionMessage.value = '文章已成功删除';
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
  } catch (err) {
    console.error('删除文章失败:', err);
    actionSuccess.value = false;
    actionMessage.value = err.response?.data?.error || err.message || '删除文章失败，请稍后重试';
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
    
    // 关闭确认对话框但保留错误消息
    showDeleteConfirm.value = false;
  }
};

// 组件挂载时获取文章列表
onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>
.manage-news-page {
  padding: 1rem;
}

h1 {
  margin-bottom: 1.5rem;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background-color: var(--primary-color-dark);
}

.search-box {
  position: relative;
}

.search-box input {
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 250px;
  font-size: 1rem;
}

.search-box .fas {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.articles-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.articles-table th,
.articles-table td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.articles-table th {
  font-weight: 600;
  color: #333;
  background-color: #f9f9f9;
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.published {
  background-color: #e6f7e6;
  color: #28a745;
}

.status-badge.draft {
  background-color: #f8f9fa;
  color: #6c757d;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions button {
  padding: 0.4rem 0.7rem;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.edit-btn {
  background-color: #e7f3ff;
  color: #0275d8;
}

.edit-btn:hover {
  background-color: #d0e5ff;
}

.toggle-btn.publish {
  background-color: #e6f7e6;
  color: #28a745;
}

.toggle-btn.publish:hover {
  background-color: #d0f0d0;
}

.toggle-btn.unpublish {
  background-color: #fff9e6;
  color: #ffc107;
}

.toggle-btn.unpublish:hover {
  background-color: #fff0c0;
}

.delete-btn {
  background-color: #ffebee;
  color: #dc3545;
}

.delete-btn:hover {
  background-color: #ffd5da;
}

.no-articles {
  padding: 2rem;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.no-articles p {
  margin-bottom: 1rem;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination button:hover:not(:disabled) {
  background-color: #e9ecef;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 模态对话框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background-color: white;
  border-radius: 6px;
  padding: 1.5rem;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-dialog h3 {
  margin-top: 0;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn {
  background-color: #f8f9fa;
  color: #333;
}

.confirm-delete-btn {
  background-color: #dc3545;
  color: white;
}

.confirm-delete-btn:hover {
  background-color: #c82333;
}

/* 操作反馈消息 */
.action-message {
  position: fixed;
  top: 1rem;
  right: 1rem;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  z-index: 900;
  animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
}

.action-message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.action-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-20px); }
}
</style> 