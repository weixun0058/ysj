<template>
  <div class="test-auth-page container">
    <h1>认证状态测试页面</h1>
    
    <div class="auth-status">
      <h2>认证状态</h2>
      <p><strong>是否已认证:</strong> {{ isAuthenticated ? '是' : '否' }}</p>
      
      <div v-if="isAuthenticated">
        <h2>用户信息</h2>
        <pre>{{ JSON.stringify(currentUser, null, 2) }}</pre>
      </div>
      
      <div v-else>
        <p>未登录，请先登录。</p>
        <router-link to="/login" class="login-button">前往登录</router-link>
      </div>
    </div>
    
    <h2>路由测试</h2>
    <div class="route-tests">
      <div class="route-test">
        <h3>管理员路由</h3>
        <p>点击测试：</p>
        <router-link to="/admin/users" class="test-button">访问用户管理</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const { isAuthenticated, currentUser } = storeToRefs(authStore);
</script>

<style scoped>
.test-auth-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1, h2, h3 {
  color: var(--text-color-light);
}

.auth-status {
  background-color: var(--card-background);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid var(--border-color);
}

pre {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.route-tests {
  background-color: var(--card-background);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.route-test {
  margin-bottom: 1.5rem;
}

.test-button, .login-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
  margin-top: 0.5rem;
}

.test-button:hover, .login-button:hover {
  opacity: 0.9;
}
</style> 