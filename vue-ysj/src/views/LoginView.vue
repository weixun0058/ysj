<!-- src/views/LoginView.vue -->
<template>
  <div class="auth-page">
    <h2>{{ isAdminLogin ? '管理员登录' : '用户登录' }}</h2>
    
    <!-- 权限提示信息 -->
    <div v-if="accessDenied" class="access-denied-message">
      您没有管理员权限，请使用管理员账号登录。
    </div>
    
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
          <button type="submit" :disabled="loading">{{ loading ? '登录中...' : isAdminLogin ? '管理员登录' : '登录' }}</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      
      <!-- 仅在普通登录时显示注册链接 -->
      <p v-if="!isAdminLogin" class="switch-link">
        还没有账户? <router-link to="/register">立即注册</router-link>
      </p>
      
      <!-- 返回网站链接 (适用于从管理页面跳转过来的情况) -->
      <p v-if="isAdminLogin" class="back-link">
        <router-link to="/">返回网站首页</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// 获取查询参数
const redirect = computed(() => route.query.redirect || '/');
const requireAdmin = computed(() => route.query.requireAdmin === 'true');
const accessDenied = computed(() => route.query.accessDenied === 'true');

// 判断是否是管理员登录流程
const isAdminLogin = computed(() => requireAdmin.value || accessDenied.value);

const credentials = ref({
  username: '',
  password: ''
});
const loading = ref(false);
const error = ref(null);

// 设置页面标题
onMounted(() => {
  document.title = isAdminLogin.value ? '管理员登录 - 壹世健' : '用户登录 - 壹世健';
});

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
      // 检查是否为管理员登录流程
      if (isAdminLogin.value) {
        // 检查是否具有管理员权限
        if (authStore.currentUser?.is_admin) {
          // 是管理员，重定向到指定页面或管理后台
          router.push(redirect.value || '/admin/dashboard');
        } else {
          // 不是管理员，显示错误信息
          error.value = '您没有管理员权限';
          await authStore.logout(); // 登出非管理员用户
        }
      } else {
        // 普通用户登录，重定向到指定页面或首页
        router.push(redirect.value || '/');
      }
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
.access-denied-message {
  color: #e74c3c; /* 红色 */
  margin-bottom: 1.5rem;
  text-align: center;
  padding: 0.75rem;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 4px;
  border: 1px solid rgba(231, 76, 60, 0.3);
}
.switch-link, .back-link {
    margin-top: 1.5rem;
    text-align: center;
    font-size: 0.9em;
}
.switch-link a, .back-link a {
    color: var(--primary-color);
    text-decoration: underline;
}
</style> 