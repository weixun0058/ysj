<!-- vue-ysj/src/views/NewsDetailView.vue -->
<template>
  <div class="view-container news-detail-page">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <article v-else-if="article">
      <h1>{{ article.title }}</h1>
      <div class="article-meta">
        <span>发布于: {{ formatDate(article.publish_date) }}</span>
        <span v-if="article.updated_at !== article.publish_date"> | 更新于: {{ formatDate(article.updated_at) }}</span>
      </div>
      <!-- 使用 v-html 渲染内容，确保后端已对内容进行必要的安全处理 -->
      <div class="article-content" v-html="article.content"></div>
      <router-link to="/news" class="back-link">返回资讯列表</router-link>
    </article>
    <div v-else>
      <p>文章未找到。</p>
      <router-link to="/news" class="back-link">返回资讯列表</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getNewsDetail } from '../api/newsApi'; // 导入新的API服务

const route = useRoute();
const article = ref(null);
const loading = ref(true);
const error = ref('');

const fetchArticle = async (slug) => {
  loading.value = true;
  error.value = '';
  article.value = null; // 重置文章数据
  try {
    // 使用API服务获取文章详情
    const data = await getNewsDetail(slug);
    article.value = data;
    document.title = `${data.title} - 壹世健资讯`; // 更新页面标题
  } catch (err) {
    console.error('获取文章详情失败:', err);
    error.value = err.message || '无法加载文章内容，请稍后重试。';
    document.title = '文章未找到 - 壹世健资讯';
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

// 组件挂载时获取文章
onMounted(() => {
  fetchArticle(route.params.slug);
});

// 监听路由参数变化，以便在同一组件内导航时重新获取数据
watch(() => route.params.slug, (newSlug) => {
  if (newSlug) {
      fetchArticle(newSlug);
  }
});
</script>

<style scoped>
.news-detail-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

h1 {
  margin-bottom: 0.5rem;
  font-size: 2.2rem;
  color: var(--text-color-light);
}

.article-meta {
  font-size: 0.9rem;
  color: var(--text-color-medium);
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.article-content {
  line-height: 1.8;
  color: var(--text-color-light);
  opacity: 0.9;
  /* 考虑为 v-html 内容添加一些基础样式 */
}
.article-content ::v-deep(p) { /* 使用 ::v-deep 或 :deep() */
    margin-bottom: 1rem;
}
.article-content ::v-deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin: 1rem 0;
}
/* ... 可以添加更多 v-html 内容的样式 */

.loading, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--text-color-medium);
}
.error {
    color: #e74c3c;
}

.back-link {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.5rem 1rem;
  background-color: var(--primary-color-light);
  color: var(--primary-color);
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}
.back-link:hover {
    background-color: var(--primary-color);
    color: var(--text-color-dark);
}
</style> 