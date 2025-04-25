<!-- 管理员用户管理界面 -->
<template>
  <div class="admin-page container">
    <div v-if="loading" class="loading-container">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchUsers" class="retry-button">重试</button>
    </div>
    
    <div v-else>
      <!-- 搜索和筛选工具栏 -->
      <div class="toolbar">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索用户名或邮箱..." 
            @input="debounceSearch"
            class="search-input"
          />
          <button class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
        
        <div class="filter-container">
          <select v-model="adminFilter" @change="fetchUsers" class="filter-select">
            <option value="">全部用户</option>
            <option value="true">管理员</option>
            <option value="false">非管理员</option>
          </select>
          
          <div class="date-range">
            <input 
              type="date" 
              v-model="createdFrom" 
              placeholder="开始日期" 
              class="date-input"
              @change="fetchUsers"
            />
            <span class="date-separator">至</span>
            <input 
              type="date" 
              v-model="createdTo" 
              placeholder="结束日期" 
              class="date-input"
              @change="fetchUsers"
            />
          </div>
        </div>
      </div>
      
      <!-- 批量操作工具栏 -->
      <div class="batch-actions" v-if="selectedUsers.length > 0">
        <span class="selection-info">已选择 {{ selectedUsers.length }} 个用户</span>
        <button 
          @click="batchAction('make_admin')" 
          class="batch-button make-admin-button"
          :disabled="!canMakeAdmin"
        >
          批量设为管理员
        </button>
        <button 
          @click="batchAction('remove_admin')" 
          class="batch-button remove-admin-button"
          :disabled="!canRemoveAdmin"
        >
          批量取消管理员
        </button>
        <button @click="clearSelection" class="batch-button clear-button">
          清除选择
        </button>
      </div>
      
      <div class="user-count">
        共 {{ totalItems }} 个用户
      </div>
      
      <div class="user-table">
        <table>
          <thead>
            <tr>
              <th class="checkbox-cell">
                <input 
                  type="checkbox" 
                  :checked="isAllSelected"
                  :indeterminate="isIndeterminate"
                  @change="toggleAllSelection"
                  class="select-checkbox"
                  :disabled="users.length === 0"
                />
              </th>
              <th>ID</th>
              <th>用户名</th>
              <th>手机号码</th>
              <th>邮箱</th>
              <th>注册时间</th>
              <th>管理员</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="user in users" 
              :key="user.id" 
              :class="{ 'admin-user': user.is_admin, 'selected-row': isSelected(user) }"
            >
              <td class="checkbox-cell">
                <input 
                  type="checkbox" 
                  :checked="isSelected(user)"
                  @change="toggleSelection(user)"
                  class="select-checkbox"
                  :disabled="isCurrentUser(user)"
                />
              </td>
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.phone || '-' }}</td>
              <td>{{ user.email || '-' }}</td>
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
      
      <!-- 分页控件 -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          class="pagination-button" 
          @click="goToPage(1)" 
          :disabled="currentPage === 1"
        >
          首页
        </button>
        <button 
          class="pagination-button" 
          @click="goToPage(currentPage - 1)" 
          :disabled="currentPage === 1"
        >
          上一页
        </button>
        
        <button 
          v-for="page in displayedPages" 
          :key="page" 
          class="pagination-button" 
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        
        <button 
          class="pagination-button" 
          @click="goToPage(currentPage + 1)" 
          :disabled="currentPage === totalPages"
        >
          下一页
        </button>
        <button 
          class="pagination-button" 
          @click="goToPage(totalPages)" 
          :disabled="currentPage === totalPages"
        >
          末页
        </button>
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
            <p><strong>手机号码:</strong> {{ selectedUser.phone || '未设置' }}</p>
            <p><strong>邮箱:</strong> {{ selectedUser.email || '未设置' }}</p>
            <p><strong>真实姓名:</strong> {{ selectedUser.real_name || '未设置' }}</p>
            <p><strong>性别:</strong> {{ selectedUser.gender || '未设置' }}</p>
            <p><strong>生日:</strong> {{ selectedUser.birthday ? formatDate(selectedUser.birthday) : '未设置' }}</p>
            <p><strong>注册时间:</strong> {{ formatDate(selectedUser.created_at) }}</p>
            <p><strong>管理员权限:</strong> {{ selectedUser.is_admin ? '是' : '否' }}</p>
          </div>
        </div>
      </div>
      
      <!-- 批量操作确认弹窗 -->
      <div v-if="batchConfirmation.show" class="batch-confirmation-modal">
        <div class="modal-content">
          <div class="modal-header">
            <h2>操作确认</h2>
            <button @click="batchConfirmation.show = false" class="close-button">&times;</button>
          </div>
          <div class="modal-body">
            <p>{{ batchConfirmation.message }}</p>
            <p class="warning">此操作无法撤销，请确认。</p>
          </div>
          <div class="modal-footer">
            <button @click="batchConfirmation.show = false" class="cancel-button">取消</button>
            <button @click="confirmBatchAction" class="confirm-button">确认</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from '../../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const users = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedUser = ref(null);
const selectedUsers = ref([]);

// 分页状态
const currentPage = ref(1);
const perPage = ref(10);
const totalPages = ref(0);
const totalItems = ref(0);

// 搜索和筛选状态
const searchQuery = ref('');
const searchTimeout = ref(null);
const adminFilter = ref('');
const createdFrom = ref('');
const createdTo = ref('');

// 批量操作确认
const batchConfirmation = ref({
  show: false,
  action: '',
  message: '',
});

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

// 获取显示的页码范围
const displayedPages = computed(() => {
  const range = 2; // 当前页前后显示的页数
  const pages = [];
  
  // 确保不超出范围
  let start = Math.max(1, currentPage.value - range);
  let end = Math.min(totalPages.value, currentPage.value + range);
  
  // 添加前面的页码
  if (start > 1) {
    pages.push(1);
    if (start > 2) pages.push('...');
  }
  
  // 添加中间的页码
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  
  // 添加后面的页码
  if (end < totalPages.value) {
    if (end < totalPages.value - 1) pages.push('...');
    pages.push(totalPages.value);
  }
  
  return pages;
});

// 全选状态
const isAllSelected = computed(() => {
  return users.value.length > 0 && 
         users.value.every(user => isSelected(user) || isCurrentUser(user));
});

// 部分选中状态
const isIndeterminate = computed(() => {
  const selectedCount = users.value.filter(user => isSelected(user)).length;
  return selectedCount > 0 && selectedCount < users.value.length;
});

// 是否可以批量设为管理员
const canMakeAdmin = computed(() => {
  return selectedUsers.value.some(user => !user.is_admin);
});

// 是否可以批量取消管理员
const canRemoveAdmin = computed(() => {
  return selectedUsers.value.some(user => user.is_admin);
});

// 检查用户是否被选中
const isSelected = (user) => {
  return selectedUsers.value.some(selectedUser => selectedUser.id === user.id);
};

// 切换用户选择状态
const toggleSelection = (user) => {
  if (isCurrentUser(user)) return;
  
  if (isSelected(user)) {
    selectedUsers.value = selectedUsers.value.filter(selectedUser => selectedUser.id !== user.id);
  } else {
    selectedUsers.value.push(user);
  }
};

// 全选/取消全选
const toggleAllSelection = () => {
  if (isAllSelected.value) {
    selectedUsers.value = [];
  } else {
    selectedUsers.value = users.value.filter(user => !isCurrentUser(user));
  }
};

// 清除选择
const clearSelection = () => {
  selectedUsers.value = [];
};

// 切换页码
const goToPage = (page) => {
  if (page === '...') return;
  currentPage.value = page;
  fetchUsers();
  clearSelection(); // 切换页面时清除选中
};

// 防抖搜索函数
const debounceSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1; // 搜索时重置页码
    fetchUsers();
    clearSelection(); // 搜索时清除选中
  }, 500);
};

// 获取所有用户（带分页和搜索）
const fetchUsers = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // 构建查询参数
    const params = {
      page: currentPage.value,
      per_page: perPage.value
    };
    
    // 添加搜索和筛选参数
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    
    if (adminFilter.value) {
      params.admin = adminFilter.value;
    }
    
    if (createdFrom.value) {
      params.created_from = new Date(createdFrom.value).toISOString();
    }
    
    if (createdTo.value) {
      // 设置为当天结束时间 23:59:59
      const endDate = new Date(createdTo.value);
      endDate.setHours(23, 59, 59, 999);
      params.created_to = endDate.toISOString();
    }
    
    // 发送请求
    const response = await axios.get('/api/users', {
      params,
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    // 更新列表和分页数据
    users.value = response.data.users || [];
    
    // 更新分页信息
    const pagination = response.data.pagination || {};
    totalPages.value = pagination.total_pages || 1;
    totalItems.value = pagination.total_items || 0;
    
    // 如果当前页面超出了总页数，回到第一页
    if (currentPage.value > totalPages.value && totalPages.value > 0) {
      currentPage.value = 1;
      fetchUsers();
    }
  } catch (err) {
    console.error('获取用户列表出错:', err);
    error.value = err.response?.data?.error || err.message || '获取用户列表失败';
  } finally {
    loading.value = false;
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

// 批量操作
const batchAction = (action) => {
  if (selectedUsers.value.length === 0) return;
  
  let message = '';
  switch (action) {
    case 'make_admin':
      message = `确定将选中的 ${selectedUsers.value.length} 个用户设为管理员吗？`;
      break;
    case 'remove_admin':
      message = `确定取消选中的 ${selectedUsers.value.length} 个用户的管理员权限吗？`;
      break;
    default:
      return;
  }
  
  // 显示确认弹窗
  batchConfirmation.value = {
    show: true,
    action,
    message
  };
};

// 确认批量操作
const confirmBatchAction = async () => {
  const action = batchConfirmation.value.action;
  const userIds = selectedUsers.value.map(user => user.id);
  
  try {
    const response = await axios.post('/api/users/batch', {
      user_ids: userIds,
      action
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    // 隐藏确认弹窗
    batchConfirmation.value.show = false;
    
    // 更新本地状态
    if (action === 'make_admin') {
      selectedUsers.value.forEach(user => {
        user.is_admin = true;
      });
    } else if (action === 'remove_admin') {
      selectedUsers.value.forEach(user => {
        user.is_admin = false;
      });
    }
    
    // 清除选择
    clearSelection();
  } catch (err) {
    console.error('批量操作失败:', err);
    alert(`操作失败: ${err.response?.data?.error || err.message}`);
  }
};

// 监听筛选条件变化
watch([adminFilter], () => {
  currentPage.value = 1; // 切换筛选时重置页码
  fetchUsers();
});

// 组件挂载时获取用户列表
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.admin-page {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

/* 加载和错误状态 */
.loading-container, .error-container {
  text-align: center;
  margin: 3rem 0;
  padding: 2rem;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  border: 1px solid var(--border-color, #444);
}

.error-container {
  color: var(--error-color, #e53935);
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

/* 工具栏 */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-box {
  display: flex;
  align-items: center;
  background-color: var(--input-background, #2a2a2a);
  border-radius: 4px;
  overflow: hidden;
  width: 300px;
}

.search-input {
  flex: 1;
  padding: 0.5rem 1rem;
  border: none;
  background-color: transparent;
  color: var(--text-color-light, #f0f0f0);
  outline: none;
}

.search-button {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.filter-container {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light, #f0f0f0);
  border: 1px solid var(--border-color, #444);
}

.date-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-input {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light, #f0f0f0);
  border: 1px solid var(--border-color, #444);
}

.date-separator {
  color: var(--text-color-light, #f0f0f0);
}

/* 批量操作工具栏 */
.batch-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: var(--highlight-background, #2c2c2c);
  border-radius: 4px;
  border-left: 3px solid var(--primary-color, #fa964b);
}

.selection-info {
  margin-right: auto;
  font-weight: bold;
  color: var(--text-color-light, #f0f0f0);
}

.batch-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.make-admin-button {
  background-color: var(--success-color, #4caf50);
  color: white;
}

.remove-admin-button {
  background-color: var(--warning-color, #ff9800);
  color: white;
}

.clear-button {
  background-color: var(--neutral-color, #757575);
  color: white;
}

/* 用户数量显示 */
.user-count {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.8;
}

/* 用户表格 */
.user-table {
  width: 100%;
  overflow-x: auto;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  border: 1px solid var(--border-color, #444);
  margin-bottom: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #444);
  color: var(--text-color-light, #f0f0f0);
}

th {
  font-weight: bold;
  background-color: var(--table-header-background, #252525);
}

.checkbox-cell {
  width: 40px;
  text-align: center;
}

.select-checkbox {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.admin-user {
  background-color: rgba(250, 150, 75, 0.1);
}

.selected-row {
  background-color: rgba(250, 150, 75, 0.2);
}

.admin-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: bold;
}

.action-buttons {
  white-space: nowrap;
}

.action-button {
  padding: 0.3rem 0.7rem;
  margin-right: 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
}

.details-button {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
}

.make-admin-button {
  background-color: var(--success-color, #4caf50);
  color: white;
}

.remove-admin-button {
  background-color: var(--warning-color, #ff9800);
  color: white;
}

/* 分页控件 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  cursor: pointer;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button.active {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border-color: var(--primary-color, #fa964b);
}

/* 模态框样式 */
.user-details-modal, .batch-confirmation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color, #444);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color, #444);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button {
  padding: 0.5rem 1.5rem;
  background-color: var(--neutral-color, #757575);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button {
  padding: 0.5rem 1.5rem;
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.warning {
  color: var(--warning-color, #ff9800);
  font-weight: bold;
  margin-top: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    width: 100%;
  }
  
  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .date-range {
    flex-direction: column;
  }
  
  .batch-actions {
    flex-wrap: wrap;
  }
  
  .selection-info {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}
</style> 