<template>
  <div class="collaboration-form-container">
    <!-- 成功提交后显示成功消息 -->
    <CollaborationSuccessMessage
      v-if="showSuccessMessage"
      @back-to-home="handleBackToHome"
      @view-products="handleViewProducts"
    />
    
    <!-- 提交成功信息 -->
    <div v-if="showSuccessMessage" class="form-success-message">
      <div class="success-icon">✓</div>
      <h3>您的合作意向已成功提交</h3>
      <p>感谢您对壹世健品牌联名合作的兴趣。我们的业务团队将在1-3个工作日内与您联系。</p>
    </div>
    
    <!-- 表单内容 -->
    <form v-else @submit.prevent="handleSubmit" class="collaboration-form">
      <!-- 基本信息 -->
      <div class="form-section">
        <h3>基本信息</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="company-name">公司/品牌名称<span class="required">*</span></label>
            <input 
              type="text" 
              id="company-name" 
              v-model="formData.companyName" 
              required 
              placeholder="请输入您的公司或品牌名称"
              :class="{ error: errors.companyName }"
            >
            <span v-if="errors.companyName" class="error-message">{{ errors.companyName }}</span>
          </div>
          
          <div class="form-group">
            <label for="industry">所属行业<span class="required">*</span></label>
            <select 
              id="industry" 
              v-model="formData.industry" 
              required
              :class="{ error: errors.industry }"
            >
              <option value="">请选择行业</option>
              <option v-for="option in industryOptions" :value="option.value">{{ option.label }}</option>
            </select>
            <span v-if="errors.industry" class="error-message">{{ errors.industry }}</span>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="contact-name">联系人姓名<span class="required">*</span></label>
            <input 
              type="text" 
              id="contact-name" 
              v-model="formData.contactName" 
              required 
              placeholder="请输入联系人姓名"
              :class="{ error: errors.contactName }"
            >
            <span v-if="errors.contactName" class="error-message">{{ errors.contactName }}</span>
          </div>
          
          <div class="form-group">
            <label for="position">职位</label>
            <input 
              type="text" 
              id="position" 
              v-model="formData.position" 
              placeholder="请输入您的职位"
            >
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="email">邮箱<span class="required">*</span></label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email" 
              required 
              placeholder="请输入您的邮箱"
              :class="{ error: errors.email }"
            >
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>
          
          <div class="form-group">
            <label for="phone">联系电话<span class="required">*</span></label>
            <input 
              type="tel" 
              id="phone" 
              v-model="formData.phone" 
              required 
              placeholder="请输入您的联系电话"
              :class="{ error: errors.phone }"
            >
            <span v-if="errors.phone" class="error-message">{{ errors.phone }}</span>
          </div>
        </div>
      </div>
      
      <!-- 合作意向 -->
      <div class="form-section">
        <h3>合作意向</h3>
        
        <div class="form-group">
          <label>合作品类 (可多选)<span class="required">*</span></label>
          <div class="checkbox-group" :class="{ error: errors.productTypes }">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.productTypes" value="honey"> 蜂蜜产品
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.productTypes" value="gift"> 礼盒套装
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.productTypes" value="beauty"> 蜂蜜美容产品
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.productTypes" value="other"> 其他
            </label>
          </div>
          <span v-if="errors.productTypes" class="error-message">{{ errors.productTypes }}</span>
        </div>
        
        <div class="form-group">
          <label for="cooperation-type">合作方式<span class="required">*</span></label>
          <select 
            id="cooperation-type" 
            v-model="formData.cooperationType" 
            required
            :class="{ error: errors.cooperationType }"
          >
            <option value="">请选择合作方式</option>
            <option v-for="option in cooperationTypeOptions" :value="option.value">{{ option.label }}</option>
          </select>
          <span v-if="errors.cooperationType" class="error-message">{{ errors.cooperationType }}</span>
        </div>
        
        <div class="form-group">
          <label for="expected-quantity">预计年度合作量</label>
          <select id="expected-quantity" v-model="formData.annualVolume">
            <option value="">请选择预计年度合作量</option>
            <option v-for="option in volumeOptions" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="expected-start-date">预计启动时间</label>
          <select id="expected-start-date" v-model="formData.expectedStartDate">
            <option value="">请选择预计启动时间</option>
            <option v-for="option in timeframeOptions" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="cooperation-details">合作需求描述<span class="required">*</span></label>
          <textarea 
            id="cooperation-details" 
            v-model="formData.cooperationDetails" 
            rows="5" 
            required 
            placeholder="请详细描述您的合作需求、期望或有任何特殊要求，我们的团队将根据您的需求提供个性化的合作方案。"
            :class="{ error: errors.cooperationDetails }"
          ></textarea>
          <span v-if="errors.cooperationDetails" class="error-message">{{ errors.cooperationDetails }}</span>
        </div>
      </div>
      
      <div class="form-group checkbox-consent">
        <label class="checkbox-label">
          <input 
            type="checkbox" 
            v-model="formData.agreePrivacy" 
            required
            :class="{ error: errors.agreePrivacy }"
          > 
          我同意贵公司根据<a href="#" @click.prevent="togglePrivacyPolicy">隐私政策</a>处理我的个人信息
        </label>
        <span v-if="errors.agreePrivacy" class="error-message">{{ errors.agreePrivacy }}</span>
      </div>
      
      <div class="form-actions">
        <button 
          type="submit" 
          class="submit-btn" 
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? '提交中...' : '提交合作意向' }}
        </button>
        <p v-if="apiError" class="error-message global-error">{{ apiError }}</p>
      </div>
    </form>
    
    <!-- 隐私政策弹窗 -->
    <div v-if="showPrivacyPolicy" class="modal-overlay">
      <div class="modal-content privacy-policy">
        <div class="modal-header">
          <h3>隐私政策</h3>
          <button class="close-btn" @click="togglePrivacyPolicy">&times;</button>
        </div>
        <div class="modal-body">
          <p>本隐私政策介绍了我们收集、使用和披露您的个人信息的方式。</p>
          <h4>1. 我们收集的信息</h4>
          <p>当您通过我们的联名合作表单提交信息时，我们会收集以下信息：</p>
          <ul>
            <li>公司/品牌名称</li>
            <li>联系人姓名和职位</li>
            <li>电子邮件地址和电话号码</li>
            <li>您的合作意向和需求描述</li>
          </ul>
          
          <h4>2. 我们如何使用这些信息</h4>
          <p>我们使用这些信息：</p>
          <ul>
            <li>联系您讨论合作详情</li>
            <li>制定和提供适合您需求的合作方案</li>
            <li>管理我们与您的业务关系</li>
          </ul>
          
          <h4>3. 信息保护</h4>
          <p>我们承诺：</p>
          <ul>
            <li>不会将您的信息出售给第三方</li>
            <li>采取适当的技术和组织措施保护您的数据</li>
            <li>仅在必要的时间内保留您的信息</li>
          </ul>
          
          <h4>4. 联系我们</h4>
          <p>如果您对我们的隐私政策有任何疑问，请联系：privacy@ysj.com</p>
        </div>
        <div class="modal-footer">
          <button @click="togglePrivacyPolicy" class="primary-btn">我已阅读并理解</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { submitCollaborationRequest, getIndustryTypes, getCollaborationTypes } from '@/api/collaborationApi';
import CollaborationSuccessMessage from './CollaborationSuccessMessage.vue';

const emit = defineEmits(['form-submitted']);

const formData = reactive({
  companyName: '',
  industry: '',
  contactName: '',
  position: '',
  email: '',
  phone: '',
  productTypes: [],
  cooperationType: '',
  annualVolume: '',
  expectedStartDate: '',
  cooperationDetails: '',
  agreePrivacy: false
});

const errors = reactive({
  companyName: '',
  industry: '',
  contactName: '',
  email: '',
  phone: '',
  productTypes: '',
  cooperationType: '',
  agreePrivacy: ''
});

const isSubmitting = ref(false);
const showSuccessMessage = ref(false);
const showPrivacyPolicy = ref(false);
const apiError = ref('');

// 模拟的选项数据（实际项目中可从API获取）
const industryOptions = ref([
  { value: '健康食品', label: '健康食品' },
  { value: '美容护肤', label: '美容护肤' },
  { value: '高端礼品', label: '高端礼品' },
  { value: '文化旅游', label: '文化旅游' },
  { value: '其他', label: '其他' }
]);

const cooperationTypeOptions = ref([
  { value: '产品定制', label: '产品定制' },
  { value: '品牌联名', label: '品牌联名' },
  { value: '礼盒定制', label: '礼盒定制' },
  { value: '全案合作', label: '全案合作' }
]);

const volumeOptions = ref([
  { value: '10万-50万', label: '10万-50万' },
  { value: '50万-100万', label: '50万-100万' },
  { value: '100万-500万', label: '100万-500万' },
  { value: '500万以上', label: '500万以上' },
  { value: '待定', label: '待定' }
]);

const timeframeOptions = ref([
  { value: '1个月内', label: '1个月内' },
  { value: '1-3个月', label: '1-3个月' },
  { value: '3-6个月', label: '3-6个月' },
  { value: '半年以上', label: '半年以上' },
  { value: '待定', label: '待定' }
]);

// 尝试从API获取选项数据
const fetchOptions = async () => {
  try {
    const [industriesResponse, typesResponse] = await Promise.all([
      getIndustryTypes(),
      getCollaborationTypes()
    ]);
    
    if (industriesResponse && industriesResponse.data) {
      industryOptions.value = industriesResponse.data;
    }
    
    if (typesResponse && typesResponse.data) {
      cooperationTypeOptions.value = typesResponse.data;
    }
  } catch (error) {
    console.error('获取选项数据失败，使用默认值', error);
    // 使用默认值，已经在上面定义了
  }
};

// 组件挂载时获取选项数据
fetchOptions();

const validateForm = () => {
  let isValid = true;
  // 重置所有错误
  Object.keys(errors).forEach(key => {
    errors[key] = '';
  });

  // 验证必填字段
  if (!formData.companyName.trim()) {
    errors.companyName = '请输入公司/品牌名称';
    isValid = false;
  }

  if (!formData.industry) {
    errors.industry = '请选择所属行业';
    isValid = false;
  }

  if (!formData.contactName.trim()) {
    errors.contactName = '请输入联系人姓名';
    isValid = false;
  }

  if (!formData.email.trim()) {
    errors.email = '请输入电子邮箱';
    isValid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = '请输入有效的电子邮箱';
    isValid = false;
  }

  if (!formData.phone.trim()) {
    errors.phone = '请输入联系电话';
    isValid = false;
  } else if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
    errors.phone = '请输入有效的手机号码';
    isValid = false;
  }

  if (formData.productTypes.length === 0) {
    errors.productTypes = '请至少选择一种合作产品类型';
    isValid = false;
  }

  if (!formData.cooperationType) {
    errors.cooperationType = '请选择合作类型';
    isValid = false;
  }

  if (!formData.agreePrivacy) {
    errors.agreePrivacy = '请阅读并同意隐私政策';
    isValid = false;
  }

  return isValid;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    // 滚动到第一个错误
    const firstError = document.querySelector('.error-message');
    if (firstError) {
      firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return;
  }

  isSubmitting.value = true;
  apiError.value = '';
  
  try {
    // 准备提交的数据
    const submissionData = {
      company_name: formData.companyName,
      industry: formData.industry,
      contact_name: formData.contactName,
      position: formData.position,
      email: formData.email,
      phone: formData.phone,
      product_types: formData.productTypes,
      cooperation_type: formData.cooperationType,
      expected_volume: formData.annualVolume,
      expected_start_date: formData.expectedStartDate,
      details: formData.cooperationDetails
    };
    
    await submitCollaborationRequest(submissionData);
    
    // 重置表单
    Object.keys(formData).forEach(key => {
      if (key === 'productTypes') {
        formData[key] = [];
      } else if (key === 'agreePrivacy') {
        formData[key] = false;
      } else {
        formData[key] = '';
      }
    });
    
    showSuccessMessage.value = true;
    setTimeout(() => {
      showSuccessMessage.value = false;
    }, 5000); // 5秒后隐藏成功消息
  } catch (error) {
    console.error('表单提交失败:', error);
    apiError.value = error.response?.data?.message || '提交失败，请稍后重试或联系客服';
  } finally {
    isSubmitting.value = false;
  }
};

const handleBackToHome = () => {
  window.location.href = '/';
};

const handleViewProducts = () => {
  window.location.href = '/products';
};

const togglePrivacyPolicy = () => {
  showPrivacyPolicy.value = !showPrivacyPolicy.value;
};
</script>

<style scoped>
.collaboration-form {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.form-section h3 {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  color: var(--text-color-light);
  position: relative;
}

.form-section h3::after {
  content: "";
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 40px;
  height: 2px;
  background-color: var(--primary-color);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color-light);
}

.required {
  color: #e74c3c;
  margin-left: 3px;
}

input[type="text"],
input[type="email"],
input[type="tel"],
select,
textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--input-background);
  color: var(--text-color-light);
  font-size: 1rem;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: var(--text-color-medium);
}

.checkbox-label input[type="checkbox"] {
  margin-right: 0.5rem;
  cursor: pointer;
}

.checkbox-consent {
  margin-top: 1rem;
  margin-bottom: 2rem;
}

.checkbox-consent a {
  color: var(--primary-color);
  text-decoration: underline;
}

.form-actions {
  text-align: center;
}

.submit-btn {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 0.9rem 2.5rem;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: var(--primary-color-dark);
}

.submit-btn:disabled {
  background-color: var(--primary-color-light);
  cursor: not-allowed;
}

/* 错误样式 */
.error {
  border-color: #e74c3c !important;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.3rem;
}

/* 隐私政策弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--card-background);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  font-size: 1.5rem;
  margin: 0;
  color: var(--text-color-light);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-color-medium);
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
  color: var(--text-color-medium);
  line-height: 1.6;
}

.modal-body h4 {
  color: var(--text-color-light);
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.modal-body ul {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.modal-body li {
  margin-bottom: 0.3rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  text-align: right;
}

.primary-btn {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 0.7rem 1.5rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .checkbox-group {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style> 