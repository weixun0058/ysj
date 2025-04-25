<!-- src/views/RegisterView.vue -->
<template>
  <div class="auth-page">
    <h2>注册新账户</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" v-model="userData.username" required>
        <small>用户名长度至少3个字符</small>
      </div>
      <div class="form-group">
        <label for="phone">手机号码:</label>
        <input type="tel" id="phone" v-model="userData.phone" required pattern="^1[3-9]\d{9}$">
        <small>请输入11位手机号码</small>
      </div>
      <div class="form-group">
        <label for="email">邮箱 (选填):</label>
        <input type="email" id="email" v-model="userData.email">
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="userData.password" required minlength="6">
        <small>密码长度至少6位</small>
      </div>
      <div class="form-group">
        <label for="confirmPassword">确认密码:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required>
        <small v-if="confirmPassword && userData.password !== confirmPassword" class="error-text">两次输入的密码不一致</small>
      </div>
      
      <!-- 额外信息部分 -->
      <details>
        <summary>填写更多信息</summary>
        <div class="additional-info">
          <div class="form-group">
            <label for="realName">真实姓名 (选填):</label>
            <input type="text" id="realName" v-model="userData.real_name">
          </div>
          <div class="form-group">
            <label for="gender">性别 (选填):</label>
            <select id="gender" v-model="userData.gender">
              <option value="">请选择</option>
              <option value="男">男</option>
              <option value="女">女</option>
              <option value="保密">保密</option>
            </select>
          </div>
          <div class="form-group">
            <label for="birthday">生日 (选填):</label>
            <input type="date" id="birthday" v-model="userData.birthday">
          </div>
        </div>
      </details>

      <div class="form-actions">
          <button type="submit" :disabled="loading || !isFormValid">{{ loading ? '注册中...' : '注册' }}</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
       <p class="switch-link">已有账户? <router-link to="/login">立即登录</router-link></p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const userData = ref({
  username: '',
  phone: '',
  email: '',
  password: '',
  real_name: '',
  gender: '',
  birthday: ''
});
const confirmPassword = ref('');
const loading = ref(false);
const error = ref(null);

const validatePhone = (phone) => {
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(phone);
};

const isFormValid = computed(() => {
  return userData.value.username && 
         userData.value.username.length >= 3 &&
         userData.value.phone && 
         validatePhone(userData.value.phone) &&
         userData.value.password && 
         userData.value.password.length >= 6 &&
         userData.value.password === confirmPassword.value;
});

const handleRegister = async () => {
  if (userData.value.password !== confirmPassword.value) {
    error.value = '两次输入的密码不一致';
    return;
  }

  if (!validatePhone(userData.value.phone)) {
    error.value = '请输入有效的11位手机号码';
    return;
  }
  
  if (userData.value.username.length < 3) {
    error.value = '用户名长度至少需要3个字符';
    return;
  }
  
  if (userData.value.password.length < 6) {
    error.value = '密码长度至少需要6位';
    return;
  }

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
input[type="password"],
input[type="tel"],
input[type="date"],
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--background-color);
  color: var(--text-color-light);
}
small {
  display: block;
  margin-top: 0.25rem;
  color: var(--text-color-muted);
  font-size: 0.8em;
}
small.error-text {
  color: #e74c3c; /* 红色 */
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
details {
  margin: 1.5rem 0;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0.5rem;
}
summary {
  cursor: pointer;
  padding: 0.5rem;
  font-weight: bold;
}
.additional-info {
  padding: 0.5rem;
}
</style> 