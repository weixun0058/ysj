<!-- Placeholder for src/views/ContactView.vue -->
<template>
  <div class="contact-view">
    <app-header
      title="联系我们"
      subtitle="我们期待听到您的声音，随时为您提供专业服务"
    />
    
    <div class="contact-container">
      <!-- 联系信息卡片 -->
      <div class="contact-info">
        <h2>联系方式</h2>
        <div class="address-card">
          <div class="card-icon">
            <i class="fas fa-map-marker-alt"></i>
          </div>
          <div class="card-content">
            <h3>公司地址</h3>
            <p>新疆维吾尔自治区伊犁哈萨克自治州尼勒克县</p>
            <p>塞外本草科技发展有限公司</p>
          </div>
        </div>
        
        <div class="contact-card">
          <div class="card-icon">
            <i class="fas fa-phone-alt"></i>
          </div>
          <div class="card-content">
            <h3>联系电话</h3>
            <p>客服热线: <a href="tel:+8600000000000">000-0000-0000</a></p>
            <p>商务合作: <a href="tel:+8600000000000">000-0000-0000</a></p>
          </div>
        </div>
        
        <div class="email-card">
          <div class="card-icon">
            <i class="fas fa-envelope"></i>
          </div>
          <div class="card-content">
            <h3>电子邮箱</h3>
            <p>客户服务: <a href="mailto:service@ysj.com">service@ysj.com</a></p>
            <p>商务合作: <a href="mailto:business@ysj.com">business@ysj.com</a></p>
          </div>
        </div>
        
        <div class="hours-card">
          <div class="card-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="card-content">
            <h3>服务时间</h3>
            <p>周一至周五: 09:00 - 18:00</p>
            <p>周六至周日: 10:00 - 16:00</p>
          </div>
        </div>
      </div>
      
      <!-- 联系表单部分 -->
      <div class="form-section">
        <h2>留言咨询</h2>
        <p class="form-intro">如有任何问题或建议，请填写以下表单，我们将尽快回复您。</p>
        
        <contact-form @form-submitted="handleFormSubmitted" />
        
        <!-- 表单提交成功提示 -->
        <div v-if="showSuccessMessage" class="success-message">
          <i class="fas fa-check-circle"></i>
          <h3>留言提交成功！</h3>
          <p>感谢您的留言，我们会尽快与您联系。</p>
          <button @click="showSuccessMessage = false" class="close-success">关闭</button>
        </div>
      </div>
    </div>
    
    <!-- 地图部分 -->
    <div class="map-section">
      <h2>公司位置</h2>
      <div class="map-container">
        <l-map 
          ref="map" 
          :zoom="mapZoom" 
          :center="mapCenter" 
          style="height: 100%; width: 100%"
          :use-global-leaflet="false" 
        >
          <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer-type="base"
            name="OpenStreetMap"
            attribution="&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"
          ></l-tile-layer>
          <l-marker :lat-lng="mapCenter">
            <l-popup>
              <b>塞外本草科技发展有限公司</b><br>
              新疆伊犁哈萨克自治州尼勒克县绿农产业园D6号
            </l-popup>
          </l-marker>
        </l-map>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// import AppHeader from '@/components/AppHeader.vue';
import ContactForm from '@/components/contact/ContactForm.vue';

// 引入 vue-leaflet 组件
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

// 表单提交成功消息控制
const showSuccessMessage = ref(false);

// 处理表单提交成功
function handleFormSubmitted() {
  showSuccessMessage.value = true;
  
  // 5秒后自动关闭成功消息
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 5000);
}

// 地图配置
const mapZoom = ref(10); // 初始缩放级别
const mapCenter = ref([43.765, 82.60]); // 尼勒克县的大致经纬度 [latitude, longitude]

</script>

<style scoped>
.contact-view {
  padding-bottom: 4rem;
}

.contact-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 3rem;
  max-width: 1200px;
  margin: 3rem auto;
  padding: 0 1.5rem;
}

.contact-container h2 {
  font-size: 1.8rem;
  color: var(--text-color-dark);
  margin-bottom: 1rem;
}

/* 联系信息卡片样式 */
.contact-info {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  align-content: start;
}

.address-card,
.contact-card,
.email-card,
.hours-card {
  display: flex;
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.address-card:hover,
.contact-card:hover,
.email-card:hover,
.hours-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.card-icon {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}

.card-icon i {
  font-size: 1.4rem;
  color: var(--primary-color);
}

.card-content h3 {
  font-size: 1.1rem;
  color: var(--text-color-dark);
  margin: 0 0 0.8rem 0;
}

.card-content p {
  margin: 0.4rem 0;
  color: var(--text-color-medium);
  font-size: 0.95rem;
}

.card-content a {
  color: var(--primary-color);
  text-decoration: none;
  transition: color 0.2s ease;
}

.card-content a:hover {
  color: var(--primary-color-dark);
  text-decoration: underline;
}

/* 表单部分样式 */
.form-section {
  position: relative;
}

.form-section h2 {
  font-size: 1.8rem;
  color: var(--text-color-dark);
  margin-bottom: 1rem;
}

.form-intro {
  color: var(--text-color-medium);
  margin-bottom: 2rem;
}

/* 成功消息样式 */
.success-message {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 400px;
  width: 90%;
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translate(-50%, -60%); }
  to { opacity: 1; transform: translate(-50%, -50%); }
}

.success-message i {
  font-size: 3rem;
  color: #4CAF50;
  margin-bottom: 1rem;
}

.success-message h3 {
  font-size: 1.4rem;
  color: var(--text-color-dark);
  margin-bottom: 0.8rem;
}

.success-message p {
  color: var(--text-color-medium);
  margin-bottom: 1.5rem;
}

.close-success {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.6rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-success:hover {
  background-color: var(--primary-color-dark);
}

/* 地图部分样式 */
.map-section {
  max-width: 1200px;
  margin: 4rem auto 2rem;
  padding: 0 1.5rem;
}

.map-section h2 {
  font-size: 1.8rem;
  color: var(--text-color-dark);
  margin-bottom: 1.5rem;
}

.map-container {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  /* 确保 Leaflet 地图容器有明确的高度 */
  background-color: #eee; /* 临时背景色，防止地图加载时空白 */
}

/* 移除图片占位符相关的样式 */
/*
.placeholder-map {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 1.2rem;
  text-align: center;
  padding: 1rem;
}
*/

/* 响应式调整 */
@media (max-width: 992px) {
  .contact-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .contact-info {
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    order: 2;
  }
  
  .form-section {
    order: 1;
  }
}

@media (max-width: 768px) {
  .contact-info {
    grid-template-columns: 1fr;
  }
  
  .map-container {
    height: 300px;
  }
}
</style> 