<!-- 管理员用户管理界面 -->
<template>
  <div class="admin-page container">
    <h1>用户管理</h1>
    
    <div v-if="loading" class="loading-container">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchUsers" class="retry-button">重试</button>
    </div>
    
    <div v-else>
      <div class="user-count">
        共 {{ users.length }} 个用户
      </div>
      
      <div class="user-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>注册时间</th>
              <th>管理员</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" :class="{ 'admin-user': user.is_admin }">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>
                <span v-if="user.is_admin" class="admin-badge">是</span>
                <span v-else>否</span>
              </td>
              <td class="action-buttons">
                <button @click="showUserDetails(user)" class="action-button details-button">
                  详情
                </button>
                <button 
                  @click="toggleAdminStatus(user)" 
                  class="action-button"
                  :class="user.is_admin ? 'remove-admin-button' : 'make-admin-button'"
                  :disabled="isCurrentUser(user)"
                >
                  {{ user.is_admin ? '取消管理员' : '设为管理员' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 用户详情弹窗 -->
      <div v-if="selectedUser" class="user-details-modal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>用户详情</h2>
            <button @click="selectedUser = null" class="close-button">&times;</button>
          </div>
          <div class="modal-body">
            <p><strong>ID:</strong> {{ selectedUser.id }}</p>
            <p><strong>用户名:</strong> {{ selectedUser.username }}</p>
            <p><strong>邮箱:</strong> {{ selectedUser.email }}</p>
            <p><strong>注册时间:</strong> {{ formatDate(selectedUser.created_at) }}</p>
            <p><strong>管理员权限:</strong> {{ selectedUser.is_admin ? '是' : '否' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const users = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedUser = ref(null);

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 判断是否为当前登录用户
const isCurrentUser = (user) => {
  return authStore.currentUser && user.id === authStore.currentUser.id;
};

// 获取所有用户
const fetchUsers = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get('/api/users', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    users.value = response.data.users || [];
    
    // 获取每个用户的详细信息
    for (const user of users.value) {
      await fetchUserDetails(user);
    }
  } catch (err) {
    console.error('获取用户列表出错:', err);
    error.value = err.response?.data?.error || err.message || '获取用户列表失败';
  } finally {
    loading.value = false;
  }
};

// 获取单个用户的详细信息
const fetchUserDetails = async (user) => {
  try {
    const response = await axios.get(`/api/users/${user.id}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    if (response.status === 200) {
      // 更新用户对象的其他属性
      Object.assign(user, response.data);
    }
  } catch (err) {
    console.error(`获取用户 ${user.id} 详情出错:`, err);
  }
};

// 显示用户详情
const showUserDetails = (user) => {
  selectedUser.value = user;
};

// 切换用户管理员状态
const toggleAdminStatus = async (user) => {
  if (isCurrentUser(user)) {
    return; // 不允许修改自己的管理员状态
  }
  
  try {
    const response = await axios.put(`/api/users/${user.id}/admin`, {
      is_admin: !user.is_admin
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    // 更新本地状态
    user.is_admin = !user.is_admin;
  } catch (err) {
    console.error('更新用户权限出错:', err);
    alert(`操作失败: ${err.response?.data?.error || err.message}`);
  }
};

// 组件挂载时获取用户列表
onMounted(() => {
  document.title = '用户管理 - 壹世健';
  fetchUsers();
});
</script>

<style scoped>
.admin-page {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-color-light);
}

.loading-container, .error-container {
  text-align: center;
  margin: 3rem 0;
  padding: 2rem;
  background-color: var(--card-background);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.error-container {
  color: var(--error-color, #e53935);
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.user-count {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: var(--text-color-light);
  opacity: 0.8;
}

.user-table {
  width: 100%;
  overflow-x: auto;
  background-color: var(--card-background);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

th {
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.1);
}

tr:last-child td {
  border-bottom: none;
}

.admin-user {
  background-color: rgba(var(--primary-color-rgb, 255, 200, 0), 0.1);
}

.admin-badge {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.3rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s;
}

.details-button {
  background-color: var(--card-background);
  color: var(--text-color-light);
  border: 1px solid var(--border-color);
}

.details-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.make-admin-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
}

.make-admin-button:hover {
  background-color: rgba(var(--primary-color-rgb, 255, 200, 0), 0.8);
}

.remove-admin-button {
  background-color: #e53935;
  color: white;
}

.remove-admin-button:hover {
  background-color: #c62828;
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 用户详情弹窗 */
.user-details-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 500px;
  background-color: var(--card-background);
  border-radius: 8px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-color-light);
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin: 0.8rem 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
  
  th, td {
    padding: 0.8rem 0.5rem;
    font-size: 0.9rem;
  }
}
</style> 