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
import axios from 'axios'; // 添加axios导入
import { useAuthStore } from '../../stores/auth'; // 导入auth store

const authStore = useAuthStore(); // 使用auth store
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
    // 构建查询URL，包含分页参数和可能的搜索条件
    let url = `/api/admin/news`;
    let params = {
      page: page,
      per_page: 10
    };
    
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }

    const response = await axios.get(url, {
      params: params,
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });

    articles.value = response.data.articles;
    totalPages.value = response.data.total_pages;
    currentPage.value = response.data.current_page;
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
    const response = await axios.put(`/api/admin/news/${article.id}/toggle-publish`, {}, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });

    // 更新本地文章状态
    const index = articles.value.findIndex(a => a.id === article.id);
    if (index !== -1) {
      articles.value[index].is_published = response.data.is_published;
    }

    // 显示成功消息
    actionSuccess.value = true;
    actionMessage.value = response.data.is_published ? '文章已发布' : '文章已设为草稿';
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
    const response = await axios.delete(`/api/admin/news/${articleToDelete.value.id}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });

    // 从列表中移除已删除的文章
    articles.value = articles.value.filter(a => a.id !== articleToDelete.value.id);
    
    // 显示成功消息
    actionSuccess.value = true;
    actionMessage.value = '文章已成功删除';
    
    // 关闭确认对话框
    showDeleteConfirm.value = false;
    articleToDelete.value = null;
    
    // 3秒后隐藏消息
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
    
    // 如果删除后没有文章了，检查是否需要更新页数
    if (articles.value.length === 0 && currentPage.value > 1) {
      changePage(currentPage.value - 1);
    }
  } catch (err) {
    console.error('删除文章失败:', err);
    actionSuccess.value = false;
    actionMessage.value = err.response?.data?.error || err.message || '删除失败，请稍后重试';
    
    // 3秒后隐藏消息
    setTimeout(() => {
      actionMessage.value = '';
    }, 3000);
  }
};

// 组件挂载时获取数据
onMounted(() => {
  // 从查询参数获取页码（如果有）
  const pageFromQuery = parseInt(route.query.page) || 1;
  fetchArticles(pageFromQuery);
});

</script>

<style scoped>
.admin-page {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-color-light, #f0f0f0);
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-container {
  display: flex;
  gap: 0.5rem;
  flex: 1;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
}

.search-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.search-button:hover {
  background-color: rgba(var(--primary-color-rgb, 250, 150, 75), 0.8);
}

.create-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.create-button:hover {
  background-color: rgba(var(--primary-color-rgb, 250, 150, 75), 0.8);
}

.create-button svg {
  width: 16px;
  height: 16px;
}

.loading-container, .error-container {
  text-align: center;
  margin: 3rem 0;
  padding: 2rem;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  border: 1px solid var(--border-color, #444);
}

.error-container {
  color: var(--error-color, #e53935);
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.article-count {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.8;
}

.article-table-container {
  overflow-x: auto;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  border: 1px solid var(--border-color, #444);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #444);
  color: var(--text-color-light, #f0f0f0);
}

th {
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.2);
}

tr:last-child td {
  border-bottom: none;
}

tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.article-title {
  font-weight: bold;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-subtitle {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  opacity: 0.7;
}

.article-date {
  font-size: 0.9rem;
}

.article-status {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.published {
  background-color: rgba(46, 125, 50, 0.2);
  color: #81c784;
}

.draft {
  background-color: rgba(255, 152, 0, 0.2);
  color: #ffb74d;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.3rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s;
}

.edit-button {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
}

.edit-button:hover {
  background-color: rgba(var(--primary-color-rgb, 250, 150, 75), 0.8);
}

.view-button {
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
  border: 1px solid var(--border-color, #444);
}

.view-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.delete-button {
  background-color: #e53935;
  color: white;
}

.delete-button:hover {
  background-color: #c62828;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  gap: 0.5rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color, #444);
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
  border-radius: 4px;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button.active {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border-color: var(--primary-color, #fa964b);
}

/* 删除确认弹窗 */
.delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 500px;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color, #444);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-color-light, #f0f0f0);
}

.modal-body {
  padding: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.modal-footer {
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  border-top: 1px solid var(--border-color, #444);
}

.cancel-button {
  padding: 0.5rem 1.5rem;
  background-color: transparent;
  color: var(--text-color-light, #f0f0f0);
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button {
  padding: 0.5rem 1.5rem;
  background-color: #e53935;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-container {
    width: 100%;
  }
  
  .create-button {
    width: 100%;
    justify-content: center;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  th, td {
    padding: 0.8rem 0.5rem;
    font-size: 0.9rem;
  }
  
  .article-title, .article-subtitle {
    max-width: 150px;
  }
}
</style> 