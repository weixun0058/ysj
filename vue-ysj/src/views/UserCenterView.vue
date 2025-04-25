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
            <p><strong>手机号码:</strong> {{ currentUser.phone || '未设置' }}</p>
            <p><strong>邮箱:</strong> {{ currentUser.email || '未设置' }}</p>
            <p><strong>注册时间:</strong> {{ formatDateTime(currentUser.created_at) }}</p>
          </div>
          <div class="info-section">
            <h4>个人资料</h4>
            <p><strong>真实姓名:</strong> {{ currentUser.real_name || '未设置' }}</p>
            <p><strong>性别:</strong> {{ currentUser.gender || '未设置' }}</p>
            <p><strong>生日:</strong> {{ currentUser.birthday ? formatDate(currentUser.birthday) : '未设置' }}</p>
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
                 <label for="update-phone">手机号码:</label>
                 <input type="tel" id="update-phone" v-model="updateData.phone" required pattern="^1[3-9]\d{9}$">
                 <small>请输入有效的11位手机号码</small>
               </div>
               <div class="form-group">
                 <label for="update-email">邮箱:</label>
                 <input type="email" id="update-email" v-model="updateData.email">
               </div>
               <div class="form-group">
                 <label for="update-real-name">真实姓名:</label>
                 <input type="text" id="update-real-name" v-model="updateData.real_name">
               </div>
               <div class="form-group">
                 <label for="update-gender">性别:</label>
                 <select id="update-gender" v-model="updateData.gender">
                   <option value="">请选择</option>
                   <option value="男">男</option>
                   <option value="女">女</option>
                   <option value="保密">保密</option>
                 </select>
               </div>
               <div class="form-group">
                 <label for="update-birthday">生日:</label>
                 <input type="date" id="update-birthday" v-model="updateData.birthday">
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

          <!-- 会员积分卡片 -->
          <div class="member-points-card">
              <h3>会员积分</h3>
              <div v-if="memberLoading" class="loading-message">正在加载会员信息...</div>
              <div v-else-if="memberError" class="error-message">加载会员信息失败: {{ memberError }}</div>
              <div v-else>
                  <!-- 会员等级与积分展示 -->
                  <div class="member-level-section">
                      <div class="level-badge" :class="{ 'vip-badge': isVipMember }">
                          <span class="level-name">{{ currentUser.member_level ? currentUser.member_level.name : '普通会员' }}</span>
                      </div>
                      <div class="points-display">
                          <div class="current-points">
                              <span class="points-number">{{ currentUser.points || 0 }}</span>
                              <span class="points-label">当前积分</span>
                          </div>
                          <div v-if="memberLevels.length > 0 && nextLevel" class="next-level-progress">
                              <div class="progress-text">
                                  <span>距离 {{ nextLevel.name }} 还需 {{ nextLevelGap }} 积分</span>
                              </div>
                              <div class="progress-bar-container">
                                  <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
                              </div>
                          </div>
                      </div>
                  </div>

                  <!-- 会员权益说明 -->
                  <div class="member-benefits-section">
                      <h4>会员权益</h4>
                      <div class="benefits-grid">
                          <div class="benefit-item">
                              <div class="benefit-icon">💰</div>
                              <div class="benefit-desc">
                                  {{ isVipMember ? '消费1元=1.5积分' : '消费1元=1积分' }}
                              </div>
                          </div>
                          <div class="benefit-item">
                              <div class="benefit-icon">🏆</div>
                              <div class="benefit-desc">累计消费满2000元自动升级为VIP会员</div>
                          </div>
                          <div class="benefit-item">
                              <div class="benefit-icon">🎁</div>
                              <div class="benefit-desc">积分可兑换专属优惠券</div>
                          </div>
                      </div>
                  </div>

                  <!-- 积分明细和优惠券 -->
                  <div class="points-coupons-tabs">
                      <div class="tabs-header">
                          <div 
                              @click="activeTab = 'points'"
                              class="tab-item" 
                              :class="{ 'active-tab': activeTab === 'points' }"
                          >积分明细</div>
                          <div 
                              @click="activeTab = 'coupons'"
                              class="tab-item" 
                              :class="{ 'active-tab': activeTab === 'coupons' }"
                          >我的优惠券</div>
                      </div>
                      
                      <div class="tab-content">
                          <!-- 积分明细标签页 -->
                          <div v-if="activeTab === 'points'" class="points-records-container">
                              <div v-if="pointsLoading" class="loading-message">正在加载积分记录...</div>
                              <div v-else-if="pointsError" class="error-message">{{ pointsError }}</div>
                              <div v-else-if="pointsRecords.length === 0" class="no-data-message">
                                  暂无积分记录
                              </div>
                              <div v-else class="points-records-list">
                                  <div v-for="record in pointsRecords" :key="record.id" class="points-record-item">
                                      <div class="record-info">
                                          <div class="record-description">{{ record.description }}</div>
                                          <div class="record-date">{{ formatDate(record.created_at) }}</div>
                                      </div>
                                      <div class="record-points" :class="{ 'positive': record.points > 0, 'negative': record.points < 0 }">
                                          {{ record.points > 0 ? '+' : '' }}{{ record.points }}
                                      </div>
                                  </div>
                                  
                                  <!-- 分页控件 -->
                                  <div v-if="pointsPagination.total > 0" class="pagination-controls">
                                      <SfButton 
                                          @click="loadPointsRecords(pointsPagination.page - 1)"
                                          :disabled="!pointsPagination.has_prev"
                                          size="sm"
                                          variant="tertiary"
                                      >上一页</SfButton>
                                      <span class="page-info">{{ pointsPagination.page }}/{{ pointsPagination.pages }}</span>
                                      <SfButton 
                                          @click="loadPointsRecords(pointsPagination.page + 1)"
                                          :disabled="!pointsPagination.has_next"
                                          size="sm"
                                          variant="tertiary"
                                      >下一页</SfButton>
                                  </div>
                              </div>
                          </div>
                          
                          <!-- 优惠券标签页 -->
                          <div v-if="activeTab === 'coupons'" class="coupons-container">
                              <div v-if="couponsLoading" class="loading-message">正在加载优惠券...</div>
                              <div v-else-if="couponsError" class="error-message">{{ couponsError }}</div>
                              <div v-else-if="userCoupons.length === 0" class="no-data-message">
                                  暂无可用优惠券
                                  <div class="coupon-actions">
                                      <SfButton @click="openExchangeCoupons" variant="secondary" size="sm">积分兑换优惠券</SfButton>
                                  </div>
                              </div>
                              <div v-else>
                                  <div class="coupon-status-tabs">
                                      <span 
                                          @click="couponStatusFilter = 'valid'"
                                          :class="{ active: couponStatusFilter === 'valid' }"
                                      >可用</span>
                                      <span 
                                          @click="couponStatusFilter = 'used'"
                                          :class="{ active: couponStatusFilter === 'used' }"
                                      >已使用</span>
                                      <span 
                                          @click="couponStatusFilter = 'all'"
                                          :class="{ active: couponStatusFilter === 'all' }"
                                      >全部</span>
                                  </div>
                                  
                                  <div class="coupons-list">
                                      <div v-for="coupon in userCoupons" :key="coupon.id" class="coupon-item" :class="{ 'used-coupon': coupon.is_used }">
                                          <div class="coupon-value">
                                              <span v-if="coupon.coupon.type === 'percent'">{{ (coupon.coupon.discount_value * 10).toFixed(0) }}折</span>
                                              <span v-else-if="coupon.coupon.type === 'amount'">¥{{ coupon.coupon.discount_value }}</span>
                                              <span v-else>{{ coupon.coupon.discount_value }}</span>
                                          </div>
                                          <div class="coupon-details">
                                              <div class="coupon-name">{{ coupon.coupon.name }}</div>
                                              <div class="coupon-rule" v-if="coupon.coupon.min_purchase > 0">
                                                  满{{ coupon.coupon.min_purchase }}元可用
                                              </div>
                                              <div class="coupon-validity">
                                                  {{ formatDate(coupon.coupon.start_date) }} 至 {{ formatDate(coupon.coupon.end_date) }}
                                              </div>
                                          </div>
                                          <div class="coupon-status" v-if="coupon.is_used">
                                              已使用
                                          </div>
                                      </div>
                                  </div>
                                  
                                  <div class="coupon-actions">
                                      <SfButton @click="openExchangeCoupons" variant="secondary" size="sm">积分兑换优惠券</SfButton>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
                  
                  <!-- 兑换优惠券弹窗 -->
                  <div v-if="showExchangeForm" class="exchange-coupon-modal">
                      <div class="modal-content">
                          <header class="modal-header">
                              <h4>积分兑换优惠券</h4>
                              <SfButton @click="showExchangeForm = false" variant="tertiary" square>X</SfButton>
                          </header>
                          <div class="modal-body">
                              <div class="available-points">
                                  <span>可用积分：<strong>{{ currentUser.points || 0 }}</strong></span>
                              </div>
                              
                              <div class="exchange-options">
                                  <div 
                                      v-for="option in exchangeOptions" 
                                      :key="option.points"
                                      class="exchange-option"
                                      :class="{ 'unavailable': currentUser.points < option.points }"
                                      @click="selectExchangeOption(option)"
                                  >
                                      <div class="option-value">{{ option.name }}</div>
                                      <div class="option-points">{{ option.points }}积分</div>
                                      <div v-if="currentUser.points < option.points" class="option-insufficient">
                                          积分不足
                                      </div>
                                  </div>
                              </div>
                          </div>
                          <footer class="modal-footer">
                              <SfButton @click="showExchangeForm = false" variant="secondary">取消</SfButton>
                              <SfButton 
                                  @click="exchangeCoupon"
                                  :disabled="!selectedExchangeOption || currentUser.points < (selectedExchangeOption?.points || 0) || exchangeLoading"
                              >
                                  <span v-if="exchangeLoading">兑换中...</span>
                                  <span v-else>确认兑换</span>
                              </SfButton>
                          </footer>
                      </div>
                  </div>
              </div>
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
import { ref, onMounted, computed, watch } from 'vue';
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
const updateData = ref({ 
  email: '', 
  phone: '',
  real_name: '',
  gender: '',
  birthday: '' 
});
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

// --- 会员积分相关状态 ---
const memberLoading = ref(false);
const memberError = ref(null);
const memberLevels = ref([]);
const activeTab = ref('points');
const couponStatusFilter = ref('valid');

// 积分记录相关
const pointsLoading = ref(false);
const pointsError = ref(null);
const pointsRecords = ref([]);
const pointsPagination = ref({
    total: 0,
    pages: 1,
    page: 1,
    per_page: 10,
    has_next: false,
    has_prev: false
});

// 优惠券相关
const couponsLoading = ref(false);
const couponsError = ref(null);
const userCoupons = ref([]);
const showExchangeForm = ref(false);
const exchangeLoading = ref(false);
const exchangeError = ref(null);
const selectedExchangeOption = ref(null);

// 预定义的兑换选项
const exchangeOptions = [
    { points: 300, name: '95折优惠券', couponType: 'percent', value: 0.95 },
    { points: 500, name: '9折优惠券', couponType: 'percent', value: 0.9 },
    { points: 800, name: '85折优惠券', couponType: 'percent', value: 0.85 }
];

// --- 计算属性 ---
const isVipMember = computed(() => {
    return currentUser.value?.member_level?.name === 'VIP会员';
});

const nextLevel = computed(() => {
    if (!memberLevels.value.length || !currentUser.value) return null;
    
    // 找到当前等级在会员等级列表中的索引
    const currentLevelId = currentUser.value.member_level?.id || memberLevels.value[0].id;
    const currentIndex = memberLevels.value.findIndex(level => level.id === currentLevelId);
    
    // 如果有下一级，返回下一级别
    if (currentIndex >= 0 && currentIndex < memberLevels.value.length - 1) {
        return memberLevels.value[currentIndex + 1];
    }
    
    return null;
});

const nextLevelGap = computed(() => {
    if (!nextLevel.value || !currentUser.value) return 0;
    const gap = nextLevel.value.min_points - (currentUser.value.points || 0);
    return gap > 0 ? gap : 0;
});

const progressPercentage = computed(() => {
    if (!nextLevel.value || !currentUser.value || !currentUser.value.member_level) return 0;
    
    const currentLevel = memberLevels.value.find(level => level.id === currentUser.value.member_level.id);
    if (!currentLevel) return 0;
    
    const currentPoints = currentUser.value.points || 0;
    const levelStart = currentLevel.min_points;
    const levelEnd = nextLevel.value.min_points;
    
    const totalRange = levelEnd - levelStart;
    const currentProgress = currentPoints - levelStart;
    
    if (totalRange <= 0) return 100;
    
    const percentage = (currentProgress / totalRange) * 100;
    return Math.min(Math.max(percentage, 0), 100);
});

// 获取用户信息 ---
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
  if (currentUser.value) { 
    updateData.value.email = currentUser.value.email || '';
    updateData.value.phone = currentUser.value.phone || '';
    updateData.value.real_name = currentUser.value.real_name || '';
    updateData.value.gender = currentUser.value.gender || '';
    updateData.value.birthday = currentUser.value.birthday || '';
  }
};

// --- 获取会员等级 ---
const fetchMemberLevels = async () => {
    memberLoading.value = true;
    memberError.value = null;
    
    try {
        const response = await axios.get('/api/member-levels');
        memberLevels.value = response.data.member_levels || [];
    } catch (err) {
        console.error("获取会员等级失败:", err);
        memberError.value = err.response?.data?.error || '加载会员等级失败';
    } finally {
        memberLoading.value = false;
    }
};

// --- 加载积分记录 ---
const loadPointsRecords = async (page = 1) => {
    if (!isAuthenticated.value) return;
    
    pointsLoading.value = true;
    pointsError.value = null;
    
    try {
        const response = await axios.get(`/api/me/points?page=${page}`, {
            headers: { 'Authorization': `Bearer ${token.value}` }
        });
        
        pointsRecords.value = response.data.points_records || [];
        pointsPagination.value = response.data.pagination || {
            total: 0,
            pages: 1,
            page: 1,
            per_page: 10,
            has_next: false,
            has_prev: false
        };
    } catch (err) {
        console.error("加载积分记录失败:", err);
        pointsError.value = err.response?.data?.error || '加载积分记录失败';
    } finally {
        pointsLoading.value = false;
    }
};

// --- 加载用户优惠券 ---
const loadUserCoupons = async () => {
    if (!isAuthenticated.value) return;
    
    couponsLoading.value = true;
    couponsError.value = null;
    
    try {
        const response = await axios.get(`/api/me/coupons?status=${couponStatusFilter.value}`, {
            headers: { 'Authorization': `Bearer ${token.value}` }
        });
        
        userCoupons.value = response.data.coupons || [];
    } catch (err) {
        console.error("加载优惠券失败:", err);
        couponsError.value = err.response?.data?.error || '加载优惠券失败';
    } finally {
        couponsLoading.value = false;
    }
};

// --- 兑换优惠券相关 ---
const openExchangeCoupons = () => {
    selectedExchangeOption.value = null;
    exchangeError.value = null;
    showExchangeForm.value = true;
};

const selectExchangeOption = (option) => {
    if (currentUser.value.points >= option.points) {
        selectedExchangeOption.value = option;
    }
};

const exchangeCoupon = async () => {
    if (!selectedExchangeOption.value || !isAuthenticated.value) return;
    
    exchangeLoading.value = true;
    exchangeError.value = null;
    
    try {
        // 假设后端提供了兑换优惠券的API
        await axios.post('/api/me/exchange-coupon', {
            points: selectedExchangeOption.value.points,
            coupon_type: selectedExchangeOption.value.couponType,
            coupon_value: selectedExchangeOption.value.value
        }, {
            headers: { 'Authorization': `Bearer ${token.value}` }
        });
        
        // 成功后关闭弹窗
        showExchangeForm.value = false;
        
        // 刷新数据
        await authStore.fetchUser(); // 重新获取用户信息以更新积分
        loadUserCoupons();
        loadPointsRecords();
        
    } catch (err) {
        console.error("兑换优惠券失败:", err);
        exchangeError.value = err.response?.data?.error || '兑换优惠券失败';
    } finally {
        exchangeLoading.value = false;
    }
};

// 监听标签页变化
const watchTabChanges = () => {
    // 当切换到优惠券标签页时加载优惠券数据
    if (activeTab.value === 'coupons') {
        loadUserCoupons();
    }
    // 当切换到积分标签页时加载积分记录
    else if (activeTab.value === 'points') {
        loadPointsRecords();
    }
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
    fetchMemberLevels();
    loadPointsRecords();
    
    // 监听标签页变化
    watchTabChanges();
});

// 监听tab的变化
watch(activeTab, () => {
    watchTabChanges();
});

// 监听优惠券状态过滤器变化
watch(couponStatusFilter, () => {
    loadUserCoupons();
});

// --- 修改邮箱逻辑 ---
const openEditProfileForm = () => {
    if (currentUser.value) {
      updateData.value.email = currentUser.value.email || '';
      updateData.value.phone = currentUser.value.phone || '';
      updateData.value.real_name = currentUser.value.real_name || '';
      updateData.value.gender = currentUser.value.gender || '';
      updateData.value.birthday = currentUser.value.birthday || '';
    }
    updateError.value = null; 
    updateSuccess.value = false;
    showPasswordForm.value = false;
    showUpdateForm.value = true;
}
const handleUpdateProfile = async () => {
  updateLoading.value = true; 
  updateError.value = null; 
  updateSuccess.value = false;
  
  // 验证手机号
  if (updateData.value.phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    if (!phoneRegex.test(updateData.value.phone)) {
      updateError.value = '请输入有效的11位手机号码';
      updateLoading.value = false;
      return;
    }
  }
  
  try {
    const profileDataToUpdate = {};
    
    // 检查每个字段是否有变化
    if (updateData.value.email !== currentUser.value.email) { 
      profileDataToUpdate.email = updateData.value.email; 
    }
    if (updateData.value.phone !== currentUser.value.phone) { 
      profileDataToUpdate.phone = updateData.value.phone; 
    }
    if (updateData.value.real_name !== currentUser.value.real_name) { 
      profileDataToUpdate.real_name = updateData.value.real_name; 
    }
    if (updateData.value.gender !== currentUser.value.gender) { 
      profileDataToUpdate.gender = updateData.value.gender; 
    }
    if (updateData.value.birthday !== currentUser.value.birthday) { 
      profileDataToUpdate.birthday = updateData.value.birthday; 
    }

    if (Object.keys(profileDataToUpdate).length > 0) {
      await authStore.updateUserProfile(profileDataToUpdate);
      updateSuccess.value = true;
      setTimeout(() => { 
        showUpdateForm.value = false; 
        updateSuccess.value = false; 
      }, 2000);
    } else { 
      updateError.value = '未检测到信息更改'; 
    }
  } catch (err) { 
    updateError.value = err.response?.data?.error || err.message || '更新失败，请稍后重试。'; 
  } finally { 
    updateLoading.value = false; 
  }
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

// 辅助函数：格式化日期
const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
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

.user-info-card, .address-management-card, .member-points-card {
  background-color: var(--card-background);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.user-info-card h3, .address-management-card h3, .member-points-card h3 {
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

/* 会员积分样式 */
.member-points-card {
    overflow: hidden;
}

.member-level-section {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
    gap: 1rem;
}

.level-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #c62828;
    border: 2px solid #fa964b;
}

.vip-badge {
    background-color: #fcf2e6;
    border-color: #f6ba67;
    color: #e6a23c;
}

.level-name {
    font-weight: bold;
    font-size: 1rem;
}

.points-display {
    flex: 1;
}

.current-points {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.5rem;
}

.points-number {
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--primary-color);
}

.points-label {
    font-size: 0.9rem;
    color: var(--text-color-light);
}

.next-level-progress {
    margin-top: 0.5rem;
}

.progress-text {
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
    color: var(--text-color-light);
}

.progress-bar-container {
    height: 6px;
    background-color: #e9e9e9;
    border-radius: 3px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    background-color: var(--primary-color);
    border-radius: 3px;
}

.member-benefits-section {
    margin: 1.5rem 0;
    padding: 1rem;
    background-color: #666;
    border-radius: 8px;
}

.member-benefits-section h4 {
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
}

.benefit-item {
    display: flex;
    align-items: center;
    padding: 0.8rem;
    background-color: #555;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.benefit-icon {
    font-size: 1.5rem;
    margin-right: 0.8rem;
}

.benefit-desc {
    font-size: 0.9rem;
}

.points-coupons-tabs {
    margin-top: 1.5rem;
}

.tabs-header {
    display: flex;
    border-bottom: 1px solid var(--border-color-light);
    margin-bottom: 1rem;
}

.tab-item {
    padding: 0.8rem 1.2rem;
    cursor: pointer;
    font-weight: 500;
    color: var(--text-color-light);
    position: relative;
}

.active-tab {
    color: var(--primary-color);
}

.active-tab::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--primary-color);
}

.tab-content {
    min-height: 200px;
}

.points-records-container, .coupons-container {
    padding: 0.5rem 0;
}

.no-data-message {
    text-align: center;
    padding: 2rem 0;
    color: var(--text-color-light);
}

.points-records-list {
    display: flex;
    flex-direction: column;
}

.points-record-item {
    display: flex;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-color-light);
}

.record-info {
    flex: 1;
}

.record-description {
    font-size: 0.95rem;
    margin-bottom: 0.3rem;
}

.record-date {
    font-size: 0.85rem;
    color: var(--text-color-light);
}

.record-points {
    font-weight: bold;
    font-size: 1.1rem;
}

.record-points.positive {
    color: #4caf50;
}

.record-points.negative {
    color: #f44336;
}

.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 1.5rem;
    gap: 1rem;
}

.page-info {
    font-size: 0.9rem;
    color: var(--text-color-light);
}

.coupon-status-tabs {
    display: flex;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border-color-light);
}

.coupon-status-tabs span {
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 0.9rem;
    color: var(--text-color-light);
}

.coupon-status-tabs span.active {
    color: var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    font-weight: 500;
}

.coupons-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.coupon-item {
    position: relative;
    display: flex;
    background: linear-gradient(to right, var(--primary-color) 30%, #fff 30%);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.coupon-item.used-coupon {
    opacity: 0.7;
    filter: grayscale(30%);
}

.coupon-value {
    width: 30%;
    padding: 1.2rem 0;
    color: #fff;
    font-size: 1.3rem;
    font-weight: bold;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
}

.coupon-details {
    width: 70%;
    padding: 1rem;
}

.coupon-name {
    font-weight: 500;
    margin-bottom: 0.3rem;
}

.coupon-rule {
    font-size: 0.85rem;
    color: var(--text-color-light);
    margin-bottom: 0.3rem;
}

.coupon-validity {
    font-size: 0.8rem;
    color: var(--text-color-light);
}

.coupon-status {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.2rem 0.5rem;
    font-size: 0.8rem;
    background-color: #f5f5f5;
    color: #999;
    border-radius: 4px;
}

.coupon-actions {
    text-align: center;
    margin-top: 1rem;
}

/* 兑换优惠券弹窗 */
.exchange-coupon-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    width: 90%;
    max-width: 500px;
    background-color: #fff;
    border-radius: 8px;
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border-color-light);
}

.modal-header h4 {
    margin: 0;
    font-size: 1.2rem;
}

.modal-body {
    padding: 1.5rem;
}

.available-points {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.exchange-options {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
}

.exchange-option {
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}

.exchange-option:hover:not(.unavailable) {
    border-color: var(--primary-color);
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.option-value {
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.option-points {
    font-size: 0.9rem;
    color: var(--text-color-light);
}

.exchange-option.unavailable {
    opacity: 0.6;
    cursor: not-allowed;
}

.option-insufficient {
    position: absolute;
    top: 0;
    right: 0;
    background-color: #f44336;
    color: white;
    padding: 0.2rem 0.5rem;
    font-size: 0.7rem;
    border-radius: 0 6px 0 6px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color-light);
    gap: 1rem;
}

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
  .user-info-card, .address-management-card, .member-points-card { padding: 1rem 1.2rem; }
  .form-row { flex-direction: column; gap: 1rem; }
  .address-list { grid-template-columns: 1fr; }
  
  .member-level-section { flex-direction: column; }
  .level-badge { margin-bottom: 0.5rem; }
  .benefits-grid { grid-template-columns: 1fr; }
  .coupons-list { grid-template-columns: 1fr; }
  .exchange-options { grid-template-columns: 1fr; }
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