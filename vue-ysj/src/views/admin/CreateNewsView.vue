<!-- vue-ysj/src/views/admin/CreateNewsView.vue -->
<template>
  <div class="view-container create-news-page">
    <h1>撰写新资讯文章</h1>
    <!-- TODO: 添加权限检查，只允许管理员访问此页面 -->

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">文章标题</label>
        <input type="text" id="title" v-model="title" required placeholder="输入文章标题">
      </div>

      <div class="form-group">
        <label for="content">文章内容</label>
        <!-- 简单的 textarea，可以替换为富文本编辑器 -->
        <textarea id="content" v-model="content" rows="15" required placeholder="在此输入文章内容..."></textarea>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
       <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '发布中...' : '发布文章' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const title = ref('');
const content = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);
const router = useRouter();

const handleSubmit = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    // TODO: 在实际应用中，需要从 localStorage 或状态管理获取 JWT token
    // const token = localStorage.getItem('accessToken');
    // if (!token) {
    //   // 处理未登录情况，例如跳转到登录页
    //   router.push('/login');
    //   return;
    // }

    const response = await fetch('/api/news', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${token}` // <-- 发送 JWT token 用于后端验证权限
      },
      body: JSON.stringify({
        title: title.value,
        content: content.value,
        // slug: 可选，让后端自动生成
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }

    // 发布成功
    successMessage.value = `文章 "${data.title}" 发布成功！`;
    console.log('文章发布成功:', data);
    // 清空表单
    title.value = '';
    content.value = '';
    // 可选：跳转到新文章详情页或列表页
    // router.push({ name: 'NewsDetail', params: { slug: data.slug } });
    // 或
    // router.push('/news');

  } catch (error) {
    console.error('文章发布失败:', error);
    errorMessage.value = error.message || '文章发布失败，请稍后重试。';
  } finally {
    isLoading.value = false;
  }
};

</script>

<style scoped>
.create-news-page {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
   background-color: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--text-color-light);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: var(--text-color-medium);
}

.form-group input[type="text"],
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background-color: var(--input-background);
  color: var(--text-color-light);
  line-height: 1.6; /* 优化 textarea 行高 */
}
.form-group input:focus,
.form-group textarea:focus {
   outline: none;
   border-color: var(--primary-color);
   box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

textarea {
    resize: vertical; /* 允许垂直调整大小 */
    min-height: 200px; /* 设置最小高度 */
}


.error-message {
  color: #e74c3c;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: center;
}

.success-message {
  color: #2ecc71;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: center;
}

button {
  display: block; /* 让按钮独占一行 */
  width: auto; /* 宽度自适应内容 */
  min-width: 150px; /* 设置最小宽度 */
  margin: 2rem auto 0 auto; /* 顶部留白并居中 */
  padding: 0.9rem 2rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, opacity 0.3s ease;
}

button:hover {
  background-color: var(--primary-color-dark);
}
button:disabled {
  background-color: var(--primary-color-light);
  opacity: 0.7;
  cursor: not-allowed;
}

</style> 