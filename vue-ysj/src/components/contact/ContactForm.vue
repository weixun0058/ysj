<template>
  <div class="contact-form">
    <!-- 隐私政策弹窗 -->
    <div v-if="showPrivacyPolicy" class="privacy-policy-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>隐私政策</h3>
          <button @click="showPrivacyPolicy = false" class="close-button">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <h4>信息收集与使用</h4>
          <p>当您使用我们的联系表单时，我们会收集您提供的个人信息，包括姓名、联系电话、电子邮箱等。这些信息仅用于回复您的咨询、处理您的请求或改进我们的服务。</p>
          
          <h4>信息保护</h4>
          <p>我们采取适当的技术和组织措施来保护您的个人信息，防止未经授权的访问、使用或披露。您的个人信息将仅由需要了解这些信息以提供相关服务的员工访问。</p>
          
          <h4>信息共享</h4>
          <p>我们不会将您的个人信息出售、交易或出租给第三方。在某些情况下，我们可能会与受信任的第三方共享您的信息，这些第三方帮助我们经营网站、开展业务或为您提供服务，前提是这些方同意对这些信息保密。</p>
          
          <h4>您的权利</h4>
          <p>根据《中华人民共和国个人信息保护法》，您有权访问、更正、删除您的个人信息，以及限制我们对您信息的处理。如果您希望行使这些权利，请通过我们提供的联系方式与我们联系。</p>
        </div>
        <div class="modal-footer">
          <button @click="showPrivacyPolicy = false" class="confirm-button">我已阅读并理解</button>
        </div>
      </div>
    </div>
  </div>

    <form @submit.prevent="submitForm">
      <div class="form-grid">
        <!-- 姓名 -->
        <div class="form-group">
          <label for="name">姓名 <span class="required">*</span></label>
          <input 
            type="text" 
            id="name" 
            v-model="formData.name" 
            :class="{ 'error': errors.name }"
            placeholder="请输入您的姓名"
          >
          <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
        </div>
        
        <!-- 联系电话 -->
        <div class="form-group">
          <label for="phone">联系电话 <span class="required">*</span></label>
          <input 
            type="tel" 
            id="phone" 
            v-model="formData.phone" 
            :class="{ 'error': errors.phone }"
            placeholder="请输入您的联系电话"
          >
          <span v-if="errors.phone" class="error-message">{{ errors.phone }}</span>
        </div>
        
        <!-- 电子邮箱 -->
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email" 
            :class="{ 'error': errors.email }"
            placeholder="请输入您的电子邮箱"
          >
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
        </div>
        
        <!-- 咨询类型 -->
        <div class="form-group">
          <label for="type">咨询类型 <span class="required">*</span></label>
          <select 
            id="type" 
            v-model="formData.type" 
            :class="{ 'error': errors.type }"
          >
            <option value="" disabled selected>请选择咨询类型</option>
            <option value="product">产品咨询</option>
            <option value="order">订单问题</option>
            <option value="cooperation">商务合作</option>
            <option value="suggestion">意见建议</option>
            <option value="complaint">投诉反馈</option>
            <option value="other">其他</option>
          </select>
          <span v-if="errors.type" class="error-message">{{ errors.type }}</span>
        </div>
      </div>
      
      <!-- 留言内容 -->
      <div class="form-group full-width">
        <label for="message">留言内容 <span class="required">*</span></label>
        <textarea 
          id="message" 
          v-model="formData.message" 
          :class="{ 'error': errors.message }"
          placeholder="请详细描述您的问题或需求，我们将尽快回复您"
          rows="6"
        ></textarea>
        <span v-if="errors.message" class="error-message">{{ errors.message }}</span>
      </div>
      
      <!-- 验证码 - 为简化示例，实际需要后端支持 -->
      <div class="form-group captcha-group">
        <label for="captcha">验证码 <span class="required">*</span></label>
        <div class="captcha-container">
          <input 
            type="text" 
            id="captcha" 
            v-model="formData.captcha" 
            :class="{ 'error': errors.captcha }"
            placeholder="请输入验证码"
          >
          <div class="captcha-image" @click="refreshCaptcha">
            {{ captchaText }}
          </div>
        </div>
        <span v-if="errors.captcha" class="error-message">{{ errors.captcha }}</span>
      </div>
      
      <!-- 隐私政策同意 -->
      <div class="form-group privacy-policy">
        <div class="checkbox-wrapper">
          <input 
            type="checkbox" 
            id="privacy" 
            v-model="formData.privacyAgreed"
            :class="{ 'error': errors.privacyAgreed }"
          >
          <label for="privacy">
            我已阅读并同意<a href="#" @click.prevent="showPrivacyPolicy = true">《隐私政策》</a>
          </label>
        </div>
        <span v-if="errors.privacyAgreed" class="error-message">{{ errors.privacyAgreed }}</span>
      </div>
      
      <!-- 提交按钮 -->
      <div class="form-group submit-group">
        <button 
          type="submit" 
          class="submit-button" 
          :disabled="isSubmitting"
        >
          <span v-if="isSubmitting">
            <i class="fas fa-spinner fa-spin"></i> 提交中...
          </span>
          <span v-else>提交留言</span>
        </button>
      </div>
    </form>
    

</template>

<script setup>
import { ref, reactive } from 'vue';

// 表单数据
const formData = reactive({
  name: '',
  phone: '',
  email: '',
  type: '',
  message: '',
  captcha: '',
  privacyAgreed: false
});

// 表单错误信息
const errors = reactive({
  name: '',
  phone: '',
  email: '',
  type: '',
  message: '',
  captcha: '',
  privacyAgreed: ''
});

// 提交状态
const isSubmitting = ref(false);

// 生成简单验证码（实际项目中应从后端获取）
const captchaText = ref(generateCaptcha());
function generateCaptcha() {
  const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let result = '';
  for (let i = 0; i < 4; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// 刷新验证码
function refreshCaptcha() {
  captchaText.value = generateCaptcha();
  formData.captcha = '';
}

// 隐私政策显示控制
const showPrivacyPolicy = ref(false);

// 表单验证
function validateForm() {
  let isValid = true;
  
  // 清除所有错误信息
  Object.keys(errors).forEach(key => {
    errors[key] = '';
  });
  
  // 验证姓名
  if (!formData.name.trim()) {
    errors.name = '请输入您的姓名';
    isValid = false;
  }
  
  // 验证电话
  if (!formData.phone.trim()) {
    errors.phone = '请输入您的联系电话';
    isValid = false;
  } else if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
    errors.phone = '请输入正确的手机号码';
    isValid = false;
  }
  
  // 验证邮箱（如果填写）
  if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = '请输入正确的电子邮箱';
    isValid = false;
  }
  
  // 验证咨询类型
  if (!formData.type) {
    errors.type = '请选择咨询类型';
    isValid = false;
  }
  
  // 验证留言内容
  if (!formData.message.trim()) {
    errors.message = '请输入留言内容';
    isValid = false;
  } else if (formData.message.length < 10) {
    errors.message = '留言内容至少10个字符';
    isValid = false;
  }
  
  // 验证验证码
  if (!formData.captcha.trim()) {
    errors.captcha = '请输入验证码';
    isValid = false;
  } else if (formData.captcha.toUpperCase() !== captchaText.value) {
    errors.captcha = '验证码不正确';
    isValid = false;
  }
  
  // 验证隐私政策
  if (!formData.privacyAgreed) {
    errors.privacyAgreed = '请阅读并同意隐私政策';
    isValid = false;
  }
  
  return isValid;
}

// 表单提交
const emit = defineEmits(['form-submitted']);

async function submitForm() {
  if (!validateForm()) {
    // 滚动到第一个错误
    setTimeout(() => {
      document.querySelector('.error-message').scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    }, 100);
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // 这里应该是实际的API调用，此处模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 清空表单
    Object.keys(formData).forEach(key => {
      if (key !== 'privacyAgreed') {
        formData[key] = '';
      }
    });
    
    // 刷新验证码
    refreshCaptcha();
    
    // 通知父组件提交成功
    emit('form-submitted');
    
  } catch (error) {
    console.error('提交表单时出错：', error);
    alert('提交失败，请稍后重试');
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.contact-form {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color-dark);
}

.required {
  color: #e74c3c;
  margin-left: 2px;
}

input,
select,
textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--input-background);
  color: var(--text-color-dark);
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

input.error,
select.error,
textarea.error {
  border-color: #e74c3c;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}

/* 验证码样式 */
.captcha-container {
  display: flex;
  gap: 1rem;
}

.captcha-image {
  flex-shrink: 0;
  width: 120px;
  height: 44px;
  background: linear-gradient(45deg, #f1f1f1, #e7e7e7);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 1.2rem;
  letter-spacing: 4px;
  cursor: pointer;
  color: #333;
  text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.8);
  user-select: none;
}

/* 隐私政策复选框 */
.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-wrapper input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-wrapper label {
  margin-bottom: 0;
  cursor: pointer;
  font-weight: normal;
  font-size: 0.95rem;
}

.checkbox-wrapper a {
  color: var(--primary-color);
  text-decoration: none;
}

.checkbox-wrapper a:hover {
  text-decoration: underline;
}

/* 提交按钮 */
.submit-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.submit-button:hover {
  background-color: var(--primary-color-dark);
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-button i {
  margin-right: 0.5rem;
}

/* 隐私政策弹窗 */
.privacy-policy-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-content {
  background-color: var(--card-background);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 1.3rem;
  color: var(--text-color-dark);
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--text-color-medium);
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-color-dark);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
  color: var(--text-color-medium);
  line-height: 1.6;
}

.modal-body h4 {
  font-size: 1.1rem;
  color: var(--text-color-dark);
  margin: 1.2rem 0 0.8rem;
}

.modal-body h4:first-child {
  margin-top: 0;
}

.modal-body p {
  margin-bottom: 1rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
  text-align: right;
}

.confirm-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.7rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-button:hover {
  background-color: var(--primary-color-dark);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .contact-form {
    padding: 1.5rem;
  }
}
</style> 