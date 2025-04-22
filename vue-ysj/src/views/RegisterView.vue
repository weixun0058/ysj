<!-- src/views/RegisterView.vue -->
<template>
  <div class="auth-page">
    <h2>注册新账户</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="userData.username" required>
        <!-- 可以添加用户名规则提示 -->
      </div>
      <div class="form-group">
        <label for="email">邮箱:</label>
        <input type="email" id="email" v-model="userData.email" required>
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="userData.password" required>
        <!-- 可以添加密码强度提示 -->
      </div>
      <div class="form-group">
        <label for="confirmPassword">确认密码:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required>
      </div>
      <div class="form-actions">
          <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
       <p class="switch-link">已有账户? <router-link to="/login">立即登录</router-link></p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const userData = ref({
  username: '',
  email: '',
  password: ''
});
const confirmPassword = ref('');
const loading = ref(false);
const error = ref(null);

const handleRegister = async () => {
  if (userData.value.password !== confirmPassword.value) {
    error.value = '两次输入的密码不一致';
    return;
  }
  // 可在此处添加更多前端校验，如用户名、邮箱格式、密码强度等

  loading.value = true;
  error.value = null;
  try {
    const success = await authStore.register(userData.value);
    if (success) {
      // 注册并自动登录成功，跳转到首页或用户中心
      router.push('/');
    }
  } catch (err) {
    error.value = err.response?.data?.error || '注册失败，请检查输入或稍后重试。';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 复用 LoginView 的样式 */
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