<template>
  <div class="user-center-page container">
    <h2>用户中心</h2>

    <div v-if="loading" class="loading-message">正在加载用户信息...</div>
    <div v-else-if="error" class="error-message">加载用户信息失败: {{ error }}</div>

    <div v-else-if="currentUser" class="user-info-wrapper">
        <!-- 用户信息卡片 -->
        <div class="user-info-card">
          <h3>欢迎您, {{ currentUser.username }}!</h3>
          <div class="info-section">
            <h4>账户信息</h4>
            <p><strong>用户名:</strong> {{ currentUser.username }}</p>
            <p><strong>邮箱:</strong> {{ currentUser.email }}</p>
            <p><strong>注册时间:</strong> {{ formatDateTime(currentUser.created_at) }}</p>
          </div>
          <div class="actions-section">
            <h4>操作</h4>
            <SfButton @click="openEditProfileForm" variant="secondary" class="action-button">修改信息</SfButton>
            <SfButton @click="openPasswordForm" variant="secondary" class="action-button">修改密码</SfButton>
          </div>

          <!-- 修改信息表单 -->
          <div v-if="showUpdateForm" class="update-form-card embedded-form">
             <h4>修改用户信息</h4>
             <form @submit.prevent="handleUpdateProfile">
               <div class="form-group">
                 <label for="update-email">邮箱:</label>
                 <input type="email" id="update-email" v-model="updateData.email" required>
               </div>
                <div class="form-actions">
                   <SfButton type="submit" :disabled="updateLoading" class="action-button">
                     <span v-if="updateLoading">更新中...</span>
                     <span v-else>确认更新</span>
                   </SfButton>
                   <SfButton type="button" @click="showUpdateForm = false" variant="secondary" class="action-button cancel-button">取消</SfButton>
               </div>
               <p v-if="updateError" class="error-message">{{ updateError }}</p>
               <p v-if="updateSuccess" class="success-message">用户信息更新成功!</p>
             </form>
          </div>

          <!-- 修改密码表单 -->
          <div v-if="showPasswordForm" class="update-form-card embedded-form">
            <h4>修改密码</h4>
            <form @submit.prevent="handleChangePassword">
              <div class="form-group">
                <label for="current-password">当前密码:</label>
                <input type="password" id="current-password" v-model="passwordData.currentPassword" required>
              </div>
               <div class="form-group">
                <label for="new-password">新密码:</label>
                <input type="password" id="new-password" v-model="passwordData.newPassword" required>
                <small v-if="passwordData.newPassword && passwordData.newPassword.length < 6" class="error-message inline-error">密码长度至少需要6位</small>
              </div>
               <div class="form-group">
                <label for="confirm-new-password">确认新密码:</label>
                <input type="password" id="confirm-new-password" v-model="passwordData.confirmNewPassword" required>
                <small v-if="passwordData.newPassword && passwordData.confirmNewPassword && passwordData.newPassword !== passwordData.confirmNewPassword" class="error-message inline-error">两次输入的新密码不一致</small>
              </div>
               <div class="form-actions">
                  <SfButton type="submit" :disabled="passwordLoading || !isPasswordFormValid" class="action-button">
                    <span v-if="passwordLoading">修改中...</span>
                    <span v-else>确认修改密码</span>
                  </SfButton>
                  <SfButton type="button" @click="showPasswordForm = false; resetPasswordForm()" variant="secondary" class="action-button cancel-button">取消</SfButton>
              </div>
               <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
               <p v-if="passwordSuccess" class="success-message">密码修改成功!</p>
            </form>
          </div>
        </div>

        <!-- 地址管理卡片 -->
        <div class="address-management-card">
            <h3>收货地址管理</h3>
            <div v-if="addressLoading" class="loading-message">正在加载地址...</div>
            <div v-else-if="addressError" class="error-message">加载地址失败: {{ addressError }}</div>
            <div v-else>
                <div v-if="addresses.length === 0 && !showAddressForm" class="no-address-message text-center py-5 text-gray-500">
                    <p>您还没有添加收货地址。</p>
                </div>
                <!-- 地址列表 -->
                <div class="address-list grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div v-for="address in addresses" :key="address.id"
                         class="address-item border rounded-md p-4 flex flex-col justify-between"
                         :class="{ 'border-primary-700 ring-2 ring-primary-200': address.is_default }">
                        <div class="address-info mb-4">
                            <p class="font-medium">
                                {{ address.recipient_name }}
                                <span v-if="address.is_default" class="ml-2 text-xs font-semibold text-primary-700 bg-primary-100 px-2 py-0.5 rounded">默认</span>
                            </p>
                            <p class="text-sm text-gray-600">{{ address.phone_number }}</p>
                            <p class="text-sm text-gray-600">{{ address.province }} {{ address.city }} {{ address.district }}</p>
                            <p class="text-sm text-gray-600">{{ address.detailed_address }}</p>
                        </div>
                        <div class="address-actions flex gap-2 justify-end">
                            <SfButton @click="openEditAddressForm(address)" size="sm" variant="tertiary">编辑</SfButton>
                            <SfButton @click="handleDeleteAddress(address.id)" size="sm" variant="tertiary" class="text-negative-700 hover:bg-negative-100">删除</SfButton>
                            <SfButton v-if="!address.is_default" @click="setDefaultAddress(address.id)" size="sm" variant="tertiary">设为默认</SfButton>
                        </div>
                    </div>
                </div>

                <!-- 添加按钮 -->
                <div class="mt-6 text-center">
                  <SfButton @click="openAddAddressForm" variant="primary">
                     + 添加新地址
                  </SfButton>
                </div>

                <!-- 添加/编辑地址模态框 -->
                <div v-if="showAddressForm">
                   <header class="mb-4">
                      <SfButton square variant="tertiary" class="absolute right-2 top-2" @click="closeAddressForm">
                         X
                      </SfButton>
                      <h3 class="font-bold text-lg" id="address-modal-title">
                         {{ editingAddress ? '编辑地址' : '添加新地址' }}
                      </h3>
                   </header>
                   <form @submit.prevent="handleSaveAddress">
                       <input v-model="addressFormData.recipient_name" placeholder="收件人姓名" required class="mb-4"/>
                       <input v-model="addressFormData.phone_number" placeholder="手机号码" type="tel" required pattern="^1[3-9]\d{9}$" title="请输入有效的11位手机号码" class="mb-4"/>
                       <div class="grid grid-cols-3 gap-4 mb-4">
                         <input v-model="addressFormData.province" placeholder="省份" required />
                         <input v-model="addressFormData.city" placeholder="城市" required />
                         <input v-model="addressFormData.district" placeholder="区/县" required />
                       </div>
                       <textarea v-model="addressFormData.detailed_address" placeholder="详细地址" required class="mb-4"></textarea>
                       <div class="mb-6">
                           <input type="checkbox" v-model="addressFormData.is_default" id="is_default_temp"/>
                           <label for="is_default_temp">设为默认地址</label>
                       </div>
                       <p v-if="addressFormError" class="error-message">{{ addressFormError }}</p>

                       <footer class="flex justify-end gap-4">
                           <SfButton type="button" @click="closeAddressForm" variant="secondary">取消</SfButton>
                           <SfButton type="submit" :disabled="addressFormLoading">
                               <span v-if="addressFormLoading">处理中...</span>
                               <span v-else>{{ editingAddress ? '确认更新' : '确认添加' }}</span>
                           </SfButton>
                       </footer>
                   </form>
                 </div>
            </div>
        </div>
    </div>
    <div v-else class="text-center py-10">
       <p>无法加载用户信息，请尝试<router-link to="/login" class="text-primary-600 hover:underline">重新登录</router-link>。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { storeToRefs } from 'pinia';
import { SfButton } from '@storefront-ui/vue';

const authStore = useAuthStore();
const { currentUser, isAuthenticated, token } = storeToRefs(authStore);

const loading = ref(false);
const error = ref(null);
const showUpdateForm = ref(false);
const showPasswordForm = ref(false);

// --- 修改邮箱相关状态 ---
const updateData = ref({ email: '' });
const updateLoading = ref(false);
const updateError = ref(null);
const updateSuccess = ref(false);

// --- 修改密码相关状态 ---
const passwordData = ref({ currentPassword: '', newPassword: '', confirmNewPassword: '' });
const passwordLoading = ref(false);
const passwordError = ref(null);
const passwordSuccess = ref(false);

// --- 地址管理相关状态 ---
const addresses = ref([]);
const addressLoading = ref(false);
const addressError = ref(null);
const showAddressForm = ref(false);
const editingAddress = ref(null);
const addressFormData = ref({
    id: null,
    recipient_name: '',
    phone_number: '',
    province: '',
    city: '',
    district: '',
    detailed_address: '',
    is_default: false
});
const addressFormLoading = ref(false);
const addressFormError = ref(null);

// --- 获取用户信息 ---
const fetchUserData = async () => {
  if (!isAuthenticated.value) { error.value = '用户未登录'; return; }
  if (!currentUser.value) {
      loading.value = true; error.value = null;
      try {
          await authStore.fetchUser();
          if (!authStore.currentUser) {
              throw new Error('无法从服务器获取用户信息');
          }
      } catch (err) { error.value = err.message || '获取用户信息时出错'; }
      finally { loading.value = false; }
  }
  if (currentUser.value) { updateData.value.email = currentUser.value.email; }
};

// --- 获取地址列表 ---
const fetchAddresses = async () => {
    if (!isAuthenticated.value) return;
    addressLoading.value = true;
    addressError.value = null;
    addresses.value = [];
    try {
        const response = await axios.get('/api/me/addresses', {
            headers: { 'Authorization': `Bearer ${token.value}` }
        });
        addresses.value = response.data.addresses;
    } catch (err) {
        addressError.value = err.response?.data?.error || '加载地址列表失败';
        console.error("Fetch addresses error:", err);
    } finally {
        addressLoading.value = false;
    }
};

// --- 地址表单操作 ---
const resetAddressForm = () => {
    editingAddress.value = null;
    addressFormData.value = {
        id: null,
        recipient_name: '',
        phone_number: '',
        province: '',
        city: '',
        district: '',
        detailed_address: '',
        is_default: false
    };
    addressFormError.value = null;
};

const openAddAddressForm = () => {
    resetAddressForm();
    showAddressForm.value = true;
};

const openEditAddressForm = (address) => {
    resetAddressForm();
    editingAddress.value = address;
    addressFormData.value = { ...address };
    showAddressForm.value = true;
};

const closeAddressForm = () => {
    showAddressForm.value = false;
    setTimeout(resetAddressForm, 300);
};

// --- 保存地址 (添加或更新) ---
const handleSaveAddress = async () => {
    if (!isAuthenticated.value) return;
    addressFormLoading.value = true;
    addressFormError.value = null;
    const apiUrl = editingAddress.value
        ? `/api/me/addresses/${editingAddress.value.id}`
        : '/api/me/addresses';
    const method = editingAddress.value ? 'put' : 'post';

    try {
        await axios({
            method: method,
            url: apiUrl,
            headers: { 'Authorization': `Bearer ${token.value}` },
            data: addressFormData.value
        });
        closeAddressForm();
        await fetchAddresses();
    } catch (err) {
        addressFormError.value = err.response?.data?.error || (editingAddress.value ? '更新地址失败' : '添加地址失败');
        console.error("Save address error:", err);
    } finally {
        addressFormLoading.value = false;
    }
};

// --- 删除地址 ---
const handleDeleteAddress = async (addressId) => {
    if (!isAuthenticated.value || !confirm('确定要删除这个地址吗？')) return;

    try {
        await axios.delete(`/api/me/addresses/${addressId}`, {
            headers: { 'Authorization': `Bearer ${token.value}` }
        });
        await fetchAddresses();
    } catch (err) {
        console.error("Delete address error:", err);
        addressError.value = err.response?.data?.error || '删除地址失败';
        setTimeout(() => addressError.value = null, 3000);
    }
};

// --- 设为默认地址 ---
const setDefaultAddress = async (addressId) => {
     if (!isAuthenticated.value) return;
     try {
         const addressToUpdate = addresses.value.find(addr => addr.id === addressId);
         if (addressToUpdate) {
             await axios.put(`/api/me/addresses/${addressId}`,
                 { ...addressToUpdate, is_default: true },
                 { headers: { 'Authorization': `Bearer ${token.value}` } }
             );
             await fetchAddresses();
         }
     } catch (err) {
         console.error("Set default address error:", err);
          addressError.value = err.response?.data?.error || '设置默认地址失败';
         setTimeout(() => addressError.value = null, 3000);
     }
};

onMounted(() => {
  fetchUserData();
  fetchAddresses();
});

// --- 修改邮箱逻辑 ---
const openEditProfileForm = () => {
    updateData.value.email = currentUser.value.email;
    updateError.value = null; updateSuccess.value = false;
    showPasswordForm.value = false;
    showUpdateForm.value = true;
}
const handleUpdateProfile = async () => {
  updateLoading.value = true; updateError.value = null; updateSuccess.value = false;
  try {
    const profileDataToUpdate = {};
    if (updateData.value.email !== currentUser.value.email) { profileDataToUpdate.email = updateData.value.email; }

    if (Object.keys(profileDataToUpdate).length > 0) {
      await authStore.updateUserProfile(profileDataToUpdate);
      updateSuccess.value = true;
      setTimeout(() => { showUpdateForm.value = false; updateSuccess.value = false; }, 2000);
    } else { updateError.value = '未检测到信息更改'; }
  } catch (err) { updateError.value = err.response?.data?.error || err.message || '更新失败，请稍后重试。'; }
  finally { updateLoading.value = false; }
};

// --- 修改密码逻辑 ---
const resetPasswordForm = () => {
   passwordData.value = { currentPassword: '', newPassword: '', confirmNewPassword: '' };
   passwordError.value = null; passwordSuccess.value = false;
}
const openPasswordForm = () => {
    resetPasswordForm();
    showUpdateForm.value = false;
    showPasswordForm.value = true;
}
const isPasswordFormValid = computed(() => {
    return passwordData.value.currentPassword &&
           passwordData.value.newPassword &&
           passwordData.value.newPassword.length >= 6 &&
           passwordData.value.confirmNewPassword &&
           passwordData.value.newPassword === passwordData.value.confirmNewPassword;
});

const handleChangePassword = async () => {
  if (!isPasswordFormValid.value) { passwordError.value = '请检查输入'; return; }
  passwordLoading.value = true; passwordError.value = null; passwordSuccess.value = false;
  try {
    await axios.put('/api/me/password',
        {
            current_password: passwordData.value.currentPassword,
            new_password: passwordData.value.newPassword
        },
        { headers: { 'Authorization': `Bearer ${token.value}` } }
    );
    passwordSuccess.value = true;
    resetPasswordForm();
    setTimeout(() => { showPasswordForm.value = false; passwordSuccess.value = false; }, 2000);
  } catch (err) { passwordError.value = err.response?.data?.error || '修改密码失败，请检查当前密码是否正确。'; }
  finally { passwordLoading.value = false; }
};

// 辅助函数：格式化日期时间
const formatDateTime = (isoString) => {
    if (!isoString) return 'N/A';
    try {
        const date = new Date(isoString);
        return date.toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        return 'Invalid Date';
    }
};

</script>

<style scoped>
.user-center-page {
  padding: 2rem 0;
  max-width: 900px;
}

.user-center-page h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.user-info-wrapper {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.user-info-card, .address-management-card {
  background-color: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.user-info-card h3, .address-management-card h3 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color-light);
    padding-bottom: 0.8rem;
}

.info-section, .actions-section {
    margin-bottom: 1.5rem;
}
.info-section h4, .actions-section h4 {
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
    color: var(--text-color);
}
.info-section p {
    margin-bottom: 0.5rem;
    color: var(--text-color-light);
}
.info-section p strong {
    color: var(--text-color);
    min-width: 80px;
    display: inline-block;
}

.actions-section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
}

.action-button {
    min-width: 120px;
}

.update-form-card.embedded-form {
    background-color: var(--background-color);
    border: 1px solid var(--border-color-light);
    border-radius: 6px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}
.update-form-card h4 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  font-size: 0.9rem;
}
.form-group input[type="email"],
.form-group input[type="password"],
.form-group input[type="text"],
.form-group input[type="tel"],
.form-group textarea {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--card-background);
  color: var(--text-color);
  font-size: 1rem;
}
.form-group textarea {
    resize: vertical;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: flex-end;
}

.cancel-button {
}

.error-message, .success-message {
  margin-top: 1rem;
  font-size: 0.9rem;
}
.error-message { color: var(--error-color); }
.success-message { color: var(--success-color); }
.inline-error { font-size: 0.8rem; display: inline; margin-left: 5px;}

.address-list {
}
.address-item {
}

.add-address-btn {
}

.form-row { display: flex; gap: 1rem; }
.form-group-inline { flex: 1; }
.form-group-checkbox { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem; }
.form-group-checkbox input[type="checkbox"] { width: auto; }
.form-group-checkbox label { margin-bottom: 0; }

@media (max-width: 768px) {
  .user-center-page { padding: 1rem; }
  .user-info-card, .address-management-card { padding: 1rem 1.2rem; }
  .form-row { flex-direction: column; gap: 1rem; }
  .address-list { grid-template-columns: 1fr; }
}

input, textarea {
    border: 1px solid var(--border-color);
    padding: 0.5rem;
    background-color: var(--card-background);
    color: var(--text-color-light);
    border-radius: 4px;
    width: 100%;
}

</style> 