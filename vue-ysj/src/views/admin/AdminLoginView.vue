<!-- 管理员登录页面 -->
<template>
  <div class="admin-login-page">
    <div class="login-container">
      <div class="login-header">
        <img src="/logo.svg" alt="壹世健后台管理系统" class="logo">
        <h1>后台管理系统</h1>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="请输入管理员用户名"
            required
            :disabled="isLoading"
          >
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              placeholder="请输入密码"
              required
              :disabled="isLoading"
            >
            <button 
              type="button" 
              class="toggle-password" 
              @click="togglePasswordVisibility"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <button 
          type="submit" 
          class="login-button" 
          :disabled="isLoading"
        >
          <span v-if="isLoading">登录中...</span>
          <span v-else>登录管理后台</span>
        </button>
      </form>
      
      <div class="login-footer">
        <router-link to="/" class="back-to-site">返回网站首页</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// 表单数据
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

// 登录处理
const handleLogin = async () => {
  errorMessage.value = '';
  
  if (!username.value || !password.value) {
    errorMessage.value = '请输入用户名和密码';
    return;
  }
  
  isLoading.value = true;
  
  try {
    // 使用公共的登录方法，传递对象格式的参数
    const credentials = {
      username: username.value,
      password: password.value
    };
    const success = await authStore.login(credentials);
    
    if (success) {
      // 检查是否为管理员
      if (authStore.currentUser?.is_admin) {
        // 登录成功且是管理员，跳转到管理后台
        router.push('/admin/dashboard');
      } else {
        // 登录成功但不是管理员，显示错误信息
        errorMessage.value = '您没有管理员权限';
        await authStore.logout(); // 登出普通用户
      }
    } else {
      // 登录失败
      errorMessage.value = '用户名或密码错误';
    }
  } catch (error) {
    console.error('登录失败', error);
    errorMessage.value = error.response?.data?.error || error.message || '登录失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.admin-login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

.login-container {
  width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header .logo {
  height: 60px;
  margin-bottom: 1rem;
}

.login-header h1 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.form-group input:focus {
  border-color: #3498db;
  outline: none;
  background-color: #fff;
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #777;
  cursor: pointer;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  text-align: center;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #1a2530;
}

.login-button:disabled {
  background-color: #7f8c8d;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 1rem;
}

.back-to-site {
  color: #7f8c8d;
  text-decoration: none;
  font-size: 0.875rem;
}

.back-to-site:hover {
  text-decoration: underline;
  color: #3498db;
}

@media (max-width: 480px) {
  .login-container {
    width: 100%;
    max-width: 320px;
    padding: 1.5rem;
  }
}
</style> 