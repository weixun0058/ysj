<template>
  <div class="success-message">
    <div class="success-icon">
      <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
    </div>
    
    <h2 class="success-title">提交成功！</h2>
    
    <div class="success-text">
      <p>感谢您对壹世健品牌联名合作的兴趣。</p>
      <p>我们的专业团队将在1-3个工作日内与您联系，讨论更多合作细节。</p>
    </div>
    
    <div class="action-buttons">
      <button class="btn primary" @click="handleViewProducts">
        了解我们的产品
      </button>
      <button class="btn secondary" @click="handleBackToHome">
        返回首页
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['back-to-home', 'view-products']);

const handleBackToHome = () => {
  emit('back-to-home');
};

const handleViewProducts = () => {
  emit('view-products');
};
</script>

<style scoped>
.success-message {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.success-icon {
  margin-bottom: 24px;
  color: #4CAF50;
  animation: scale-in 0.5s ease-out;
}

@keyframes scale-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  70% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.success-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.success-text {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 32px;
}

.success-text p {
  margin-bottom: 8px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn {
  padding: 12px 20px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn.primary {
  background-color: #7D5F46;
  color: white;
}

.btn.primary:hover {
  background-color: #8D6F56;
}

.btn.secondary {
  background-color: #E8E8E8;
  color: #333;
}

.btn.secondary:hover {
  background-color: #D8D8D8;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    gap: 12px;
  }
  
  .success-message {
    padding: 30px 15px;
  }
}
</style> 