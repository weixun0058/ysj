<template>
  <div class="view-container brand-collaboration-page">
    <!-- 顶部横幅 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>品牌联名合作计划</h1>
        <h2>携手共赢，打造"甜蜜"生态圈</h2>
        <p class="subtitle">让您的品牌拥有天然健康的附加值，触达千万精准客户</p>
        <button class="cta-button" @click="scrollToForm">立即合作</button>
      </div>
    </section>

    <!-- 我们的优势 -->
    <section class="advantages-section section-padding">
      <h2 class="section-title">我们的优势</h2>
      
      <div class="advantages-grid">
        <div class="advantage-card">
          <div class="icon-container">
            <i class="fas fa-seedling"></i>
          </div>
          <h3>纯净天然，品质保证</h3>
          <p>来自新疆伊犁天山脚下的认证蜂蜜：</p>
          <ul>
            <li><strong>地理标志保护产品</strong>，保证原产地真实性</li>
            <li><strong>严格品控标准</strong>，零添加纯天然</li>
          </ul>
        </div>
        
        <div class="advantage-card">
          <div class="icon-container">
            <i class="fas fa-palette"></i>
          </div>
          <h3>灵活定制，精准触达</h3>
          <p>全链路定制化服务：</p>
          <ul>
            <li><strong>包装设计</strong>：印制品牌LOGO，打造差异化视觉</li>
            <li><strong>产品组合</strong>：定制规格、功能套装，满足多样需求</li>
          </ul>
        </div>
        
        <div class="advantage-card">
          <div class="icon-container">
            <i class="fas fa-sync-alt"></i>
          </div>
          <h3>资源共享，流量裂变</h3>
          <ul>
            <li><strong>渠道互通</strong>：双向引流，扩大品牌影响力</li>
            <li><strong>联合营销</strong>：分摊成本，扩大曝光度</li>
          </ul>
        </div>
        
        <div class="advantage-card">
          <div class="icon-container">
            <i class="fas fa-handshake"></i>
          </div>
          <h3>双赢分成，轻资产合作</h3>
          <ul>
            <li><strong>零库存压力</strong>：按需生产，降低库存风险</li>
            <li><strong>灵活分成</strong>：定制收益分配方案，确保双方利益最大化</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 合作对象招募 -->
    <section class="target-partners-section section-padding section-alt-bg">
      <h2 class="section-title">合作对象招募</h2>
      <p class="section-subtitle">我们优先开放以下领域的品牌合作：</p>
      
      <div class="partners-grid">
        <div class="partner-card">
          <div class="icon-container">
            <i class="fas fa-leaf"></i>
          </div>
          <h3>健康食品</h3>
          <p>茶饮、烘焙、代餐品牌</p>
          <div class="partner-value">→ 联名开发"天然甜味解决方案"</div>
        </div>
        
        <div class="partner-card">
          <div class="icon-container">
            <i class="fas fa-spa"></i>
          </div>
          <h3>美容个护</h3>
          <p>护肤品、精油品牌</p>
          <div class="partner-value">→ 定制"蜂蜜润养系列"（如面膜、唇膏）</div>
        </div>
        
        <div class="partner-card">
          <div class="icon-container">
            <i class="fas fa-gift"></i>
          </div>
          <h3>高端礼品</h3>
          <p>节庆礼品、商务礼赠平台</p>
          <div class="partner-value">→ 限量设计款礼盒，溢价空间超30%</div>
        </div>
        
        <div class="partner-card">
          <div class="icon-container">
            <i class="fas fa-mountain"></i>
          </div>
          <h3>文旅农创</h3>
          <p>农场体验、地方特产</p>
          <div class="partner-value">→ 共创"沉浸式蜂蜜主题服务"</div>
        </div>
      </div>
    </section>

    <!-- 四大权益 -->
    <section class="benefits-section section-padding">
      <h2 class="section-title">联名合作四大权益</h2>
      
      <div class="benefits-container">
        <div class="benefit-card">
          <div class="benefit-number">1</div>
          <div class="benefit-icon"><i class="fas fa-paint-brush"></i></div>
          <h3>灵活定制</h3>
          <ul>
            <li>包装设计：支持专属LOGO、IP形象、节日主题植入</li>
            <li>产品创新：提供蜂蜜原液、便携装、功能组合套装等选项</li>
          </ul>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-number">2</div>
          <div class="benefit-icon"><i class="fas fa-share-alt"></i></div>
          <h3>流量共享</h3>
          <ul>
            <li>双方官网/门店同步展示联名产品</li>
            <li>联合发起短视频挑战赛、直播带货（参考成功案例：双渠道销量增长30%+）</li>
          </ul>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-number">3</div>
          <div class="benefit-icon"><i class="fas fa-chart-line"></i></div>
          <h3>数据护航</h3>
          <ul>
            <li>提供联名产品专属溯源二维码，追踪用户消费行为</li>
            <li>定期输出销售报告，优化营销策略</li>
          </ul>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-number">4</div>
          <div class="benefit-icon"><i class="fas fa-handshake"></i></div>
          <h3>长期共赢</h3>
          <ul>
            <li>阶梯式分成模式：销量越高，合作方分成比例最高可达25%</li>
            <li>优先续约权：年度合作客户享新品研发优先参与资格</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 成功案例 -->
    <section class="case-studies-section section-padding section-alt-bg">
      <h2 class="section-title">合作案例见证</h2>
      
      <div class="cases-container">
        <div class="case-card">
          <div class="case-icon"><i class="fas fa-mug-hot"></i></div>
          <h3>案例1：蜂蜜×新式茶饮品牌</h3>
          <p>联名推出"蜜语茶香"限定礼盒，通过"买茶饮送联名蜂蜜包"活动，带动双方门店客单价提升40%。</p>
          <img src="/img/case-study-1.png" alt="蜂蜜茶饮合作案例" class="case-image">
        </div>
        
        <div class="case-card">
          <div class="case-icon"><i class="fas fa-box-open"></i></div>
          <h3>案例2：蜂蜜×高端礼品平台</h3>
          <p>设计敦煌文化主题蜂巢礼盒，入驻高端商务渠道，单款产品溢价达68%。</p>
          <img src="/img/case-study-2.jpg" alt="高端礼品合作案例" class="case-image">
        </div>
      </div>
    </section>

    <!-- 合作流程 -->
    <section class="process-section section-padding">
      <h2 class="section-title">三步开启合作</h2>
      
      <div class="process-steps">
        <div class="process-step">
          <div class="step-number">1</div>
          <div class="step-icon"><i class="fas fa-file-signature"></i></div>
          <h3>提交意向</h3>
          <p>填写合作需求表，告诉我们您的想法</p>
        </div>
        
        <div class="process-arrow">
          <i class="fas fa-long-arrow-alt-right"></i>
        </div>
        
        <div class="process-step">
          <div class="step-number">2</div>
          <div class="step-icon"><i class="fas fa-tasks"></i></div>
          <h3>方案定制</h3>
          <p>15个工作日内提供联名产品提案+分成测算</p>
        </div>
        
        <div class="process-arrow">
          <i class="fas fa-long-arrow-alt-right"></i>
        </div>
        
        <div class="process-step">
          <div class="step-number">3</div>
          <div class="step-icon"><i class="fas fa-rocket"></i></div>
          <h3>签约上线</h3>
          <p>最快15天完成产品落地，同步启动全域推广</p>
        </div>
      </div>
    </section>

    <!-- 联系表单 -->
    <section id="collaboration-form" class="form-section section-padding">
      <h2 class="section-title">立即抢占健康消费新风口！</h2>
      
      <div class="form-container">
        <CollaborationForm @form-submitted="handleFormSubmitted" />
        
        <div class="form-side-info">
          <h3>我们的承诺</h3>
          <ul>
            <li><i class="fas fa-check-circle"></i> 100%天然蜂蜜原料，通过有机认证与绿色食品检测</li>
            <li><i class="fas fa-shield-alt"></i> 严格保护合作方数据隐私，合同明确权责与知识产权归属</li>
            <li><i class="fas fa-headset"></i> 7×24小时联名产品专属客服支持</li>
          </ul>
          
          <div class="contact-info">
            <p><i class="fas fa-phone"></i> <strong>联系合作经理：</strong>XXX-XXXXXXX</p>
            <p><i class="fas fa-envelope"></i> <strong>邮箱：</strong>collaboration@ysj.com</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 提交成功弹窗 -->
    <div v-if="showSuccessModal" class="success-modal">
      <div class="modal-content">
        <i class="fas fa-check-circle"></i>
        <h3>提交成功！</h3>
        <p>感谢您的合作意向，我们的专业团队将在1-2个工作日内与您联系。</p>
        <button @click="showSuccessModal = false">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CollaborationForm from '@/components/brand-collaboration/CollaborationForm.vue';

const showSuccessModal = ref(false);

// 滚动到表单区域
const scrollToForm = () => {
  document.getElementById('collaboration-form').scrollIntoView({ 
    behavior: 'smooth' 
  });
};

// 处理表单提交成功
const handleFormSubmitted = () => {
  showSuccessModal.value = true;
  // 可以在这里添加其他处理逻辑，例如重置表单等
};
</script>

<style scoped>
.brand-collaboration-page {
  color: var(--text-color-light);
}

/* 顶部横幅样式 */
.hero-section {
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('/img/black-bee-bg.png');
  background-size: cover;
  background-position: center;
  height: 60vh;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
  padding: 0 2rem;
}

.hero-content {
  max-width: 800px;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-section h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 0.9rem 2.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: var(--primary-color-dark);
}

/* 通用部分样式 */
.section-padding {
  padding: 5rem 2rem;
}

.section-alt-bg {
  background-color: rgba(var(--primary-color-rgb), 0.05);
}

.section-title {
  text-align: center;
  font-size: 2.2rem;
  margin-bottom: 3rem;
  position: relative;
  color: var(--text-color-light);
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: -0.8rem;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background-color: var(--primary-color);
}

.section-subtitle {
  text-align: center;
  font-size: 1.2rem;
  max-width: 800px;
  margin: 0 auto 3rem;
  color: var(--text-color-medium);
}

/* 优势卡片样式 */
.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.advantage-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.advantage-card:hover {
  transform: translateY(-5px);
}

.icon-container {
  width: 70px;
  height: 70px;
  background-color: rgba(var(--primary-color-rgb), 0.2);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.advantage-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.advantage-card p {
  color: var(--text-color-medium);
  margin-bottom: 1rem;
  line-height: 1.6;
}

.advantage-card ul {
  padding-left: 1.5rem;
  color: var(--text-color-medium);
}

.advantage-card li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* 合作伙伴卡片样式 */
.partners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.partner-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s ease;
}

.partner-card:hover {
  transform: translateY(-5px);
}

.partner-card .icon-container {
  margin: 0 auto 1.5rem;
}

.partner-card h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
  color: var(--text-color-light);
}

.partner-card p {
  color: var(--text-color-medium);
  margin-bottom: 1rem;
}

.partner-value {
  padding: 0.8rem;
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 4px;
  color: var(--primary-color);
  font-weight: bold;
}

/* 权益卡片样式 */
.benefits-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.benefit-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  padding-top: 3rem;
  transition: transform 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
}

.benefit-number {
  position: absolute;
  top: -1.5rem;
  left: 1.5rem;
  width: 3rem;
  height: 3rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: bold;
}

.benefit-card h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.benefit-card ul {
  padding-left: 1.5rem;
  color: var(--text-color-medium);
}

.benefit-card li {
  margin-bottom: 0.7rem;
  line-height: 1.5;
}

.benefit-icon {
  color: var(--primary-color);
  font-size: 1.8rem;
  margin-bottom: 1rem;
  margin-top: 0.5rem;
}

/* 案例样式 */
.cases-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.case-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.case-card:hover {
  transform: translateY(-5px);
}

.case-icon {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
}

.case-card h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.case-card p {
  color: var(--text-color-medium);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.case-image {
  width: 100%;
  border-radius: 4px;
  height: 200px;
  object-fit: cover;
}

/* 流程步骤样式 */
.process-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1000px;
  margin: 0 auto;
}

.process-step {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  flex: 1;
  max-width: 260px;
  transition: transform 0.3s ease;
}

.process-step:hover {
  transform: translateY(-5px);
}

.process-arrow {
  font-size: 2rem;
  color: var(--primary-color);
  margin: 0 1rem;
}

.step-number {
  width: 2.5rem;
  height: 2.5rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-weight: bold;
}

.step-icon {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 1rem 0;
}

.process-step h3 {
  font-size: 1.3rem;
  margin-bottom: 0.7rem;
  color: var(--text-color-light);
}

.process-step p {
  color: var(--text-color-medium);
  font-size: 0.9rem;
}

/* 表单区域样式 */
.form-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  max-width: 1000px;
  margin: 0 auto;
}

.form-side-info {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
}

.form-side-info h3 {
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
  color: var(--text-color-light);
  position: relative;
}

.form-side-info h3::after {
  content: "";
  position: absolute;
  bottom: -0.6rem;
  left: 0;
  width: 50px;
  height: 2px;
  background-color: var(--primary-color);
}

.form-side-info ul {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
}

.form-side-info li {
  margin-bottom: 1rem;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
}

.form-side-info li i {
  color: var(--primary-color);
  margin-right: 0.8rem;
  margin-top: 0.2rem;
}

.contact-info {
  background-color: rgba(var(--primary-color-rgb), 0.1);
  padding: 1.5rem;
  border-radius: 4px;
}

.contact-info p {
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.contact-info i {
  color: var(--primary-color);
  margin-right: 0.5rem;
}

/* 成功弹窗样式 */
.success-modal {
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
  padding: 2rem;
  max-width: 400px;
  text-align: center;
}

.modal-content i {
  font-size: 3rem;
  color: #2ecc71;
  margin-bottom: 1rem;
}

.modal-content h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.modal-content p {
  color: var(--text-color-medium);
  margin-bottom: 1.5rem;
}

.modal-content button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 0.7rem 2rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.2rem;
  }
  
  .hero-section h2 {
    font-size: 1.5rem;
  }
  
  .advantages-grid,
  .partners-grid,
  .benefits-container,
  .cases-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .process-steps {
    flex-direction: column;
  }
  
  .process-step {
    margin-bottom: 2rem;
    width: 100%;
    max-width: 100%;
  }
  
  .process-arrow {
    transform: rotate(90deg);
    margin: 1rem 0;
  }
  
  .form-container {
    flex-direction: column;
  }
  
  .form-side-info {
    width: 100%;
    margin-top: 2rem;
    margin-left: 0;
  }
}

@media (min-width: 769px) and (max-width: 1023px) {
  .advantages-grid,
  .partners-grid,
  .benefits-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 