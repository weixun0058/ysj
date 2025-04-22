<!-- 测试视图，用于验证API连接 -->
<template>
  <div class="test-container">
    <h1>API 连接测试</h1>
    
    <div class="card">
      <h2>验证信息</h2>
      <p><strong>认证状态：</strong> {{ authStore.isAuthenticated ? '已登录' : '未登录' }}</p>
      <p><strong>用户类型：</strong> {{ authStore.currentUser?.is_admin ? '管理员' : '普通用户' }}</p>
      <p><strong>用户名：</strong> {{ authStore.currentUser?.username || '未登录' }}</p>
      <p><strong>Token 状态：</strong> {{ authStore.token ? '已存在' : '不存在' }}</p>
      <p v-if="authStore.token"><strong>Token 片段：</strong> {{ tokenPreview }}</p>
    </div>
    
    <div class="card">
      <h2>API 测试</h2>
      <div class="button-group">
        <button @click="testApiUsers" :disabled="testingUsers">
          <span v-if="testingUsers">测试中...</span>
          <span v-else>测试用户列表接口</span>
        </button>
        <button @click="testApiNews" :disabled="testingNews">
          <span v-if="testingNews">测试中...</span>
          <span v-else>测试文章列表接口</span>
        </button>
      </div>
      
      <div v-if="testResult" :class="['test-result', testSuccess ? 'success' : 'error']">
        <h3>{{ testSuccess ? '测试成功' : '测试失败' }}</h3>
        <pre>{{ testResult }}</pre>
      </div>
    </div>
    
    <div class="card">
      <h2>Axios 默认配置</h2>
      <p><strong>是否设置默认授权头：</strong> {{ !!axiosAuthHeader }}</p>
      <p v-if="axiosAuthHeader"><strong>默认头值：</strong> {{ axiosAuthHeader }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const testResult = ref('');
const testSuccess = ref(false);
const testingUsers = ref(false);
const testingNews = ref(false);
const axiosAuthHeader = ref('');

// 显示token的前10位加...
const tokenPreview = computed(() => {
  if (!authStore.token) return '';
  const token = authStore.token;
  if (token.length <= 10) return token;
  return token.substring(0, 10) + '...';
});

// 测试用户列表API
const testApiUsers = async () => {
  testingUsers.value = true;
  testResult.value = '';
  testSuccess.value = false;
  
  try {
    // 设置请求头并记录
    const headers = { 'Authorization': `Bearer ${authStore.token}` };
    
    // 发送请求
    const response = await axios.get('/api/users', { headers });
    
    // 显示结果
    testSuccess.value = true;
    testResult.value = JSON.stringify(response.data, null, 2);
  } catch (error) {
    testSuccess.value = false;
    testResult.value = `错误: ${error.message}\n\n`;
    if (error.response) {
      testResult.value += `状态码: ${error.response.status}\n`;
      testResult.value += `响应数据: ${JSON.stringify(error.response.data, null, 2)}`;
    }
  } finally {
    testingUsers.value = false;
  }
};

// 测试文章列表API
const testApiNews = async () => {
  testingNews.value = true;
  testResult.value = '';
  testSuccess.value = false;
  
  try {
    // 设置请求头并记录
    const headers = { 'Authorization': `Bearer ${authStore.token}` };
    
    // 发送请求
    const response = await axios.get('/api/admin/news', { headers });
    
    // 显示结果
    testSuccess.value = true;
    testResult.value = JSON.stringify(response.data, null, 2);
  } catch (error) {
    testSuccess.value = false;
    testResult.value = `错误: ${error.message}\n\n`;
    if (error.response) {
      testResult.value += `状态码: ${error.response.status}\n`;
      testResult.value += `响应数据: ${JSON.stringify(error.response.data, null, 2)}`;
    }
  } finally {
    testingNews.value = false;
  }
};

// 组件挂载时检查axios默认设置
onMounted(() => {
  // 检查axios是否设置了默认的授权头
  if (axios.defaults.headers.common['Authorization']) {
    axiosAuthHeader.value = axios.defaults.headers.common['Authorization'];
  }
});
</script>

<style scoped>
.test-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-color);
}

h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button:hover:not(:disabled) {
  background-color: #e08743;
}

button:disabled {
  background-color: #7f8c8d;
  cursor: not-allowed;
}

.test-result {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 4px;
}

.test-result.success {
  background-color: rgba(46, 204, 113, 0.1);
  border: 1px solid #2ecc71;
}

.test-result.error {
  background-color: rgba(231, 76, 60, 0.1);
  border: 1px solid #e74c3c;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
  background-color: var(--card-background);
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  max-height: 400px;
  overflow-y: auto;
}
</style> 