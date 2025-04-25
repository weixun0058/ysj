<!-- vue-ysj/src/views/admin/EditNewsView.vue -->
<template>
  <div class="view-container edit-news-page">
    <h1>编辑文章</h1>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <form v-else @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">文章标题</label>
        <input type="text" id="title" v-model="title" required placeholder="输入文章标题">
      </div>

      <div class="form-group">
        <label for="slug">文章标识 (URL)</label>
        <div class="slug-input-group">
          <input 
            type="text" 
            id="slug" 
            v-model="slug" 
            placeholder="自动生成或手动输入" 
            :class="{ 'is-warning': slugWarning }"
          >
          <div v-if="slugWarning" class="input-warning">
            <i class="fas fa-exclamation-triangle"></i>
            {{ slugWarning }}
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="content">文章内容</label>
        <QuillEditor v-model="content" placeholder="请在此输入文章内容..." height="400px" />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="publish-status">发布状态</label>
          <select id="publish-status" v-model="isPublished">
            <option :value="true">已发布</option>
            <option :value="false">草稿</option>
          </select>
        </div>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div class="form-actions">
        <button type="button" class="cancel-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> 返回
        </button>
        <button type="submit" :disabled="isSubmitting" class="save-btn">
          <i class="fas fa-save"></i> {{ isSubmitting ? '保存中...' : '保存修改' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import { getAdminNewsDetail, updateNews } from '../../api/newsApi'; // 导入API服务
import QuillEditor from '@/components/admin/QuillEditor.vue'; // 导入QuillEditor组件

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const articleId = route.params.id;

// 表单数据
const title = ref('');
const slug = ref('');
const content = ref('');
const isPublished = ref(true);

// 状态
const loading = ref(true);
const error = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isSubmitting = ref(false);
const slugWarning = ref('');
const originalSlug = ref(''); // 保存原始slug，用于检测是否修改

// 加载文章详情
const fetchArticle = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    // 使用API服务获取文章详情
    const article = await getAdminNewsDetail(articleId);
    
    // 填充表单数据
    title.value = article.title;
    slug.value = article.slug;
    originalSlug.value = article.slug; // 记录原始slug
    content.value = article.content;
    isPublished.value = article.is_published;
    
    document.title = `编辑: ${article.title} - 管理系统`;
  } catch (err) {
    console.error('获取文章失败:', err);
    error.value = err.response?.data?.error || err.message || '无法加载文章，请稍后重试。';
  } finally {
    loading.value = false;
  }
};

// 表单提交
const handleSubmit = async () => {
  // 如果已经在提交中，直接返回，避免重复提交
  if (isSubmitting.value) return;
  
  console.log('handleSubmit function called');
  errorMessage.value = '';
  successMessage.value = '';
  isSubmitting.value = true;

  try {
    // 检查内容是否为空
    if (!content.value || content.value === '<p><br></p>') {
      errorMessage.value = '文章内容不能为空';
      isSubmitting.value = false;
      return;
    }
    
    // 使用API服务更新文章
    const data = await updateNews(articleId, {
      title: title.value,
      content: content.value,
      slug: slug.value || undefined, // 如果为空，后端自动生成
      is_published: isPublished.value
    });
    
    // 更新表单数据（以防后端有修改）
    slug.value = data.slug;
    originalSlug.value = data.slug;
    
    // 显示成功消息
    successMessage.value = '文章更新成功！';
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
    
    // 可选：成功后延迟跳转回列表
    setTimeout(() => {
      router.push({ name: 'ManageNews' });
    }, 1000);
  } catch (err) {
    console.error('更新文章失败:', err);
    errorMessage.value = err.response?.data?.error || err.message || '更新失败，请稍后重试。';
  } finally {
    isSubmitting.value = false;
  }
};

// 监听slug变化，提供警告
watch(slug, (newValue) => {
  if (newValue && newValue !== originalSlug.value) {
    slugWarning.value = '修改URL可能会影响已分享的链接。';
  } else {
    slugWarning.value = '';
  }
});

// 返回列表
const goBack = () => {
  console.log('goBack function called');
  // 使用浏览器原生历史返回，如果是从文章管理页来的
  if (window.history.length > 1 && document.referrer.includes('admin/news')) {
    router.back();
  } else {
    // 否则直接导航到文章管理页
    router.push({ name: 'ManageNews' });
  }
};

// 初始化
onMounted(() => {
  fetchArticle();
});
</script>

<style scoped>
.edit-news-page {
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

.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: var(--text-color-medium);
}

.form-group input[type="text"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light);
  line-height: 1.6;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(250, 150, 75, 0.2);
}

.form-group input.is-warning {
  border-color: #f1c40f;
}

.slug-input-group {
  position: relative;
}

.input-warning {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #f1c40f;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.cancel-btn, .save-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn {
  background-color: transparent;
  color: var(--text-color-light);
  border: 1px solid var(--border-color);
}

.cancel-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.save-btn {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
}

.save-btn:hover {
  background-color: var(--primary-color-dark);
}

.save-btn:disabled {
  background-color: rgba(var(--primary-color-rgb, 250, 150, 75), 0.5);
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--text-color-medium);
}

.error {
  text-align: center;
  padding: 1.5rem;
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 4px;
}

.success-message {
  color: #27ae60;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  background-color: rgba(39, 174, 96, 0.1);
  border-radius: 4px;
}
</style> 