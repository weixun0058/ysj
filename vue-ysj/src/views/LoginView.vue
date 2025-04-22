<!-- src/views/LoginView.vue -->
<template>
  <div class="auth-page">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名或邮箱:</label>
        <input type="text" id="username" v-model="credentials.username" required>
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="credentials.password" required>
      </div>
      <div class="form-actions">
          <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <p class="switch-link">还没有账户? <router-link to="/register">立即注册</router-link></p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const credentials = ref({
  username: '',
  password: ''
});
const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 清理输入值两端的空格
    const cleanedCredentials = {
        username: credentials.value.username.trim(),
        password: credentials.value.password.trim()
    };

    // 使用清理后的凭证进行登录
    const success = await authStore.login(cleanedCredentials);
    if (success) {
      // 登录成功，跳转到首页或用户中心
      router.push(router.currentRoute.value.query.redirect || '/'); // 跳转到来源页或首页
    }
  } catch (err) {
    error.value = err.response?.data?.error || '登录失败，请检查用户名或密码。';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 共享样式可以提取到 style.css 或 auth.css */
.auth-page {
  max-width: 400px;
  margin: 4rem auto;
  padding: 2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--card-background);
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-color);
  color: var(--text-color-light);
}
button {
  width: 100%;
  padding: 0.8rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background-color: #e6b800; /* primary-color 的亮色 */
}
.error-message {
  color: #e74c3c; /* 红色 */
  margin-top: 1rem;
  text-align: center;
}
.switch-link {
    margin-top: 1.5rem;
    text-align: center;
    font-size: 0.9em;
}
.switch-link a {
    color: var(--primary-color);
    text-decoration: underline;
}
</style> 