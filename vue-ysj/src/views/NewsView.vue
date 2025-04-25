<!-- vue-ysj/src/views/NewsView.vue -->
<template>
  <div class="view-container news-list-page">
    <h1>最新动态资讯</h1>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="articles.length > 0">
      <ul class="news-list">
        <li v-for="article in articles" :key="article.id" class="news-item">
          <router-link :to="{ name: 'NewsDetail', params: { slug: article.slug } }" class="news-link">
            <h2>{{ article.title }}</h2>
            <p class="publish-date">发布于: {{ formatDate(article.publish_date) }}</p>
            <!-- <p class="excerpt">{{ article.excerpt }}</p> --> <!-- 如果 API 返回摘要 -->
          </router-link>
        </li>
      </ul>

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

    <div v-else>
      <p>暂无资讯发布。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 
import { getNewsList } from '../api/newsApi'; // 导入新的API服务

const articles = ref([]);
const loading = ref(true);
const error = ref('');
const currentPage = ref(1);
const totalPages = ref(1);
const router = useRouter();
const route = useRoute(); 

const fetchNews = async (page = 1) => {
  loading.value = true;
  error.value = '';
  try {
    // 从路由查询参数获取页码，如果存在的话
    const pageFromQuery = parseInt(route.query.page) || page;
    currentPage.value = pageFromQuery;

    // 使用API服务获取新闻列表
    const data = await getNewsList(currentPage.value, 10); // 每页显示10条
    articles.value = data.news;
    totalPages.value = data.total_pages;
    currentPage.value = data.current_page; 
    document.title = `最新动态资讯 (第 ${currentPage.value} 页) - 壹世健`;
  } catch (err) {
    console.error('获取新闻列表失败:', err);
    error.value = err.message || '无法加载资讯列表，请稍后重试。';
    document.title = '最新动态资讯 - 壹世健';
  } finally {
    loading.value = false;
  }
};

// 格式化日期函数 (简单示例)
const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
}

// 切换页面函数
const changePage = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        // 更新路由查询参数以反映当前页码
        router.push({ query: { page: newPage } });
        // fetchNews 会从 route.query.page 读取新页码
        fetchNews(newPage);
    }
}

// 组件挂载时获取第一页数据
onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.news-list-page {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
   color: var(--text-color-light);
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--text-color-medium);
}
.error {
    color: #e74c3c;
}

.news-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.news-item {
  background-color: var(--card-background);
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}
.news-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}


.news-link {
    display: block;
    padding: 1.5rem 2rem;
    text-decoration: none;
    color: inherit; /* 继承父元素颜色 */
}

.news-item h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: var(--primary-color);
  transition: color 0.3s ease;
}
.news-link:hover h2 {
    color: var(--primary-color-dark);
}


.publish-date {
  font-size: 0.9rem;
  color: var(--text-color-medium);
  margin-bottom: 0.5rem;
}

/* .excerpt {
  color: var(--text-color-light);
  opacity: 0.8;
  line-height: 1.6;
} */

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 3rem;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: var(--primary-color-light);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.pagination button:hover:not(:disabled) {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination span {
  color: var(--text-color-medium);
}
</style> 