<template>
  <div class="bee-adoption-page">
    <!-- 顶部横幅 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>蜜蜂认养计划</h1>
        <h2>您的专属蜂箱，甜蜜一生的承诺</h2>
        <p class="subtitle">让每一滴蜂蜜都有故事，让每一次选择都值得信赖！</p>
        <button class="cta-button" @click="scrollToAdoption">立即认养</button>
      </div>
    </section>

    <!-- 为什么选择我们 -->
    <section class="why-us-section section-padding">
      <h2 class="section-title">为什么选择我们的蜜蜂认养计划？</h2>
      
      <div class="features-grid">
        <div class="feature-card">
          <div class="icon-container">
            <i class="fas fa-qrcode"></i>
          </div>
          <h3>从蜂箱到餐桌，全程透明可追溯</h3>
          <ul>
            <li><strong>区块链溯源技术</strong>：每箱蜂蜜对应唯一ID，扫码即可查看蜂箱位置、采蜜时间、蜂农信息，全程阳光透明。</li>
            <li><strong>蜂箱直播互动</strong>：通过APP实时观看您的蜂箱状态，见证蜂群采蜜、蜂蜜封盖的全过程，感受自然的馈赠。</li>
          </ul>
        </div>
        
        <div class="feature-card">
          <div class="icon-container">
            <i class="fas fa-honey-pot"></i>
          </div>
          <h3>纯天然品质，专属您的甜蜜承诺</h3>
          <ul>
            <li><strong>零添加、无污染</strong>：蜂农遵循有机标准，拒绝农药与添加剂，确保每一滴蜂蜜的天然纯净。</li>
            <li><strong>定制化体验</strong>：蜂蜜瓶可刻字、定制标签，或搭配专属认养证书，成为独一无二的礼物。</li>
          </ul>
        </div>
        
        <div class="feature-card">
          <div class="icon-container">
            <i class="fas fa-tree"></i>
          </div>
          <h3>支持蜂农，守护生态农业</h3>
          <ul>
            <li><strong>稳定收益保障</strong>：您的认养让蜂农获得稳定订单，助力小农户可持续发展。</li>
            <li><strong>生态保护参与</strong>：蜜蜂是生态链的重要一环，您的选择为地球增添一份绿色力量。</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 认养套餐 -->
    <section id="adoption-packages" class="packages-section section-padding">
      <h2 class="section-title">选择您的蜜蜂认养套餐</h2>
      
      <div class="packages-grid">
        <div class="package-card">
          <div class="package-header">
            <h3>星芒套餐</h3>
            <div class="package-price">
              <span class="price">¥1,999</span>
              <span class="period">/ 年</span>
            </div>
            <span class="badge">最受欢迎</span>
          </div>
          <div class="package-content">
            <div class="package-description">
              <p>认养一箱蜜蜂，定期收获来自天山脚下的纯净蜂蜜，适合小家庭日常食用。</p>
            </div>
            <ul class="package-features">
              <li><i class="fas fa-check"></i> 认养1箱蜜蜂（纯种新疆黑蜂）</li>
              <li><i class="fas fa-check"></i> 每季度收到500g纯天然蜂蜜（全年共2kg）</li>
              <li><i class="fas fa-check"></i> 每月赠送5L低氘天山雪水</li>
              <li><i class="fas fa-check"></i> 区块链溯源证书（含专属QR码）</li>
              <li><i class="fas fa-check"></i> 在线查看蜂群生长状态</li>
              <li><i class="fas fa-check"></i> 会员专享价格购买其他产品</li>
            </ul>
            <button class="select-button">选择此套餐</button>
          </div>
        </div>
        
        <div class="package-card">
          <div class="package-header">
            <h3>璀璨套餐</h3>
            <div class="package-price">
              <span class="price">¥3,999</span>
              <span class="period">/ 年</span>
            </div>
          </div>
          <div class="package-content">
            <div class="package-description">
              <p>认养两箱蜜蜂，获取更多特色蜂蜜和健康服务，享受优先收获和更多互动体验。</p>
            </div>
            <ul class="package-features">
              <li><i class="fas fa-check"></i> 认养2箱蜜蜂（可选不同蜜源品种）</li>
              <li><i class="fas fa-check"></i> 每季度收到1.2kg蜂蜜（全年共5kg）</li>
              <li><i class="fas fa-check"></i> 每月赠送10L低氘天山雪水</li>
              <li><i class="fas fa-check"></i> 个性化蜂蜜定制标签服务</li>
              <li><i class="fas fa-check"></i> 专属蜂场探访机会（1次/年）</li>
              <li><i class="fas fa-check"></i> 蜂农视频连线服务（2次/年）</li>
              <li><i class="fas fa-check"></i> 全部星芒套餐权益</li>
            </ul>
            <button class="select-button">选择此套餐</button>
          </div>
        </div>
        
        <div class="package-card">
          <div class="package-header">
            <h3>皇家套餐</h3>
            <div class="package-price">
              <span class="price">¥9,999</span>
              <span class="period">/ 年</span>
            </div>
          </div>
          <div class="package-content">
            <div class="package-description">
              <p>认养整块蜂场区域，专享稀有品种蜂蜜，尊享权益和个性化定制，适合高端商务馈赠。</p>
            </div>
            <ul class="package-features">
              <li><i class="fas fa-check"></i> 认养5箱蜜蜂（独立蜂场区域）</li>
              <li><i class="fas fa-check"></i> 每季度收到3kg蜂蜜（全年共12kg）</li>
              <li><i class="fas fa-check"></i> 每月赠送20L低氘天山雪水</li>
              <li><i class="fas fa-check"></i> 独家花粉品种蜂蜜定制权</li>
              <li><i class="fas fa-check"></i> 个性化定制礼盒设计服务</li>
              <li><i class="fas fa-check"></i> VIP蜂场体验之旅（含住宿）</li>
              <li><i class="fas fa-check"></i> 专属健康顾问服务</li>
              <li><i class="fas fa-check"></i> 全部璀璨套餐权益</li>
            </ul>
            <button class="select-button">选择此套餐</button>
          </div>
        </div>
      </div>
      
      <div class="package-note">
        <p><i class="fas fa-info-circle"></i> 所有套餐均为一年期，到期后可优先续约并享受老会员优惠。支持灵活付款，可按季度分期支付。</p>
      </div>
    </section>
    
    <!-- 认养流程 -->
    <section class="process-section section-padding">
      <h2 class="section-title">认养流程 - 四步开启甜蜜旅程</h2>
      
      <div class="process-steps">
        <div class="process-step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>选择套餐</h3>
            <p>根据您的需求选择合适的认养套餐，完成在线支付。</p>
          </div>
        </div>
        
        <div class="process-step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>匹配蜂箱</h3>
            <p>我们会为您匹配指定的蜂箱并发送认养证书和溯源二维码。</p>
          </div>
        </div>
        
        <div class="process-step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>查看蜂箱</h3>
            <p>通过手机APP或网站，观察您认养的蜂群生长状态。</p>
          </div>
        </div>
        
        <div class="process-step">
          <div class="step-number">4</div>
          <div class="step-content">
            <h3>收获蜂蜜</h3>
            <p>按照套餐约定，定期收到从您认养蜂箱直接采集的纯天然蜂蜜。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 常见问题FAQ -->
    <section class="faq-section section-padding">
      <h2 class="section-title">常见问题</h2>
      
      <div class="faq-container">
        <div class="faq-item" v-for="(item, index) in faqItems" :key="index">
          <div class="faq-question" @click="toggleFaq(index)">
            <h3>{{ item.question }}</h3>
            <span class="toggle-icon">
              <i :class="activeFaq === index ? 'fas fa-minus' : 'fas fa-plus'"></i>
            </span>
          </div>
          <div class="faq-answer" :class="{ active: activeFaq === index }">
            <p>{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 认养须知 -->
    <section class="notes-section section-padding">
      <h2 class="section-title">认养须知</h2>
      
      <div class="notes-container">
        <div class="note-card">
          <div class="note-icon">
            <i class="fas fa-truck"></i>
          </div>
          <h3>配送说明</h3>
          <p>蜂蜜和低氘水会按照套餐约定的周期定期配送，全国范围内包邮。每次发货前会提前通过短信或邮件通知您。特殊地区（如港澳台、海外）可能需要额外运费。</p>
        </div>
        
        <div class="note-card">
          <div class="note-icon">
            <i class="fas fa-calendar-alt"></i>
          </div>
          <h3>认养期限</h3>
          <p>认养周期以一年为单位，到期前一个月您将收到续约提醒。续约可享受优惠价格，并保留原有蜂箱。如不再续约，认养关系自动终止，但您仍可以普通会员身份购买产品。</p>
        </div>
        
        <div class="note-card">
          <div class="note-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
          <h3>品质保障</h3>
          <p>所有出品的蜂蜜均经过严格的质量检测，确保符合食品安全标准。如收到的产品存在质量问题，请保留产品与包装，联系客服处理，我们将为您重新发货或退款。</p>
        </div>
        
        <div class="note-card">
          <div class="note-icon">
            <i class="fas fa-hand-holding-heart"></i>
          </div>
          <h3>公益责任</h3>
          <p>每一份认养套餐的售价中，都有一部分将用于支持蜜蜂保护计划和生态环境保护。选择认养，您也成为了环境保护的一份子。我们将定期公布公益项目进展。</p>
        </div>
      </div>
      
      <div class="notes-disclaimer">
        <p>注：蜂蜜是纯天然产品，不同批次、不同季节的产品在色泽、味道可能有所不同，属于正常现象。自然环境可能导致蜂蜜产量波动，如遇特殊情况（如极端天气），我们将及时与您沟通并提供相应解决方案。</p>
      </div>
    </section>

    <!-- 底部号召性文案 -->
    <section class="cta-bottom section-padding">
      <div class="cta-content">
        <h2>加入我们的蜜蜂认养计划</h2>
        <p>成为蜜蜂守护者，拥有专属甜蜜，传递健康幸福</p>
        <button class="cta-button" @click="scrollToAdoption">立即认养</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 滚动到认养套餐区域
const scrollToAdoption = () => {
  document.getElementById('adoption-packages').scrollIntoView({ 
    behavior: 'smooth' 
  });
};

// FAQ数据
const faqItems = [
  {
    question: "认养的蜂箱是真实存在的吗？",
    answer: "是的，每一位认养人对应的蜂箱都是在我们的天山蜂场实际存在的。我们为每个蜂箱分配了唯一的ID和定位，您可以通过溯源系统查看蜂箱的实时状态。"
  },
  {
    question: "一年能收到多少蜂蜜？会有季节性差异吗？",
    answer: "根据您选择的套餐不同，一年收到的蜂蜜数量从2kg到12kg不等。蜂蜜采集是有季节性的，通常在春季和秋季产量最丰富，我们会根据蜜蜂的自然采集周期安排发货，并保证全年总量符合承诺。"
  },
  {
    question: "我能去蜂场参观我认养的蜂箱吗？",
    answer: "可以！璀璨套餐和皇家套餐的会员可以预约蜂场参观体验。我们的蜂场位于新疆伊犁尼勒克地区，参观时我们会提供专业的防护装备和向导，确保您的安全和最佳体验。"
  },
  {
    question: "蜂箱出现问题或者产量不足怎么办？",
    answer: "自然环境中确实可能出现一些变数。如果您认养的蜂箱出现问题，我们会立即为您更换健康的蜂群；如遇产量不足，我们会从其他蜂箱调配优质蜂蜜确保您能按时收到承诺数量的产品。"
  },
  {
    question: "低氘水是什么？为什么搭配蜂蜜？",
    answer: "低氘水是指氘含量低于普通水的水，来自天山深层冰川融水，具有更好的渗透性和生物相容性。蜂蜜与低氘水搭配食用，能更好地发挥蜂蜜的营养价值，帮助人体更好地吸收和利用蜂蜜中的活性成分。"
  },
  {
    question: "认养套餐可以送人或作为礼品吗？",
    answer: "完全可以！我们提供精美的礼盒包装和定制化服务，是送给亲友、商务伙伴的高品质健康礼品。您可以在订购时选择礼品包装，并添加定制的祝福语。"
  }
];

// 当前展开的FAQ项
const activeFaq = ref(null);

// 切换FAQ项的展开/折叠状态
const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? null : index;
};
</script>

<style scoped>
.bee-adoption-page {
  color: var(--text-color-light);
}

/* 顶部横幅样式 */
.hero-section {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/img/bees-hero.png');
  background-size: cover;
  background-position: center;
  height: 70vh;
  min-height: 500px;
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
  font-size: 3.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-section h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.subtitle {
  font-size: 1.3rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 1rem 3rem;
  font-size: 1.3rem;
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

.section-title {
  text-align: center;
  font-size: 2.5rem;
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

/* 特色卡片样式 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
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

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.feature-card ul {
  padding-left: 1.2rem;
  color: var(--text-color-medium);
}

.feature-card li {
  margin-bottom: 0.7rem;
  line-height: 1.6;
}

/* 套餐卡片样式 */
.packages-section {
  background-color: var(--background-color-alt);
}

.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.package-card {
  background-color: var(--card-background);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.package-card:hover {
  transform: translateY(-10px);
}

.package-header {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  padding: 2rem;
  text-align: center;
  position: relative;
}

.package-header h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.package-price {
  font-size: 1.2rem;
}

.price {
  font-size: 2.5rem;
  font-weight: bold;
}

.period {
  font-size: 1.2rem;
}

.badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #ff6b6b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
}

.package-content {
  padding: 2rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.package-description {
  margin-bottom: 1.5rem;
  color: var(--text-color-medium);
}

.package-features {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
  flex-grow: 1;
}

.package-features li {
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color-light);
}

.package-features li:last-child {
  border-bottom: none;
}

.package-features i {
  color: var(--primary-color);
  margin-right: 0.7rem;
}

.select-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: auto;
}

.select-button:hover {
  background-color: var(--primary-color-dark);
}

.package-note {
  max-width: 1200px;
  margin: 2rem auto 0;
  padding: 1rem;
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 4px;
  text-align: center;
}

.package-note p {
  color: var(--text-color-medium);
}

.package-note i {
  color: var(--primary-color);
  margin-right: 0.5rem;
}

/* 认养流程 */
.process-steps {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
}

/* 连接线 */
.process-steps::before {
  content: "";
  position: absolute;
  top: 70px;
  left: 50px;
  width: calc(100% - 100px);
  height: 3px;
  background-color: var(--primary-color);
  z-index: 0;
}

.process-step {
  display: flex;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  position: relative;
  z-index: 1;
}

.step-number {
  flex-shrink: 0;
  width: 100px;
  height: 100px;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-right: 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.step-content {
  flex-grow: 1;
  padding-top: 1.5rem;
}

.step-content h3 {
  font-size: 1.8rem;
  margin-bottom: 0.7rem;
  color: var(--text-color-light);
}

.step-content p {
  color: var(--text-color-medium);
  font-size: 1.1rem;
  line-height: 1.6;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }
  
  .hero-section h2 {
    font-size: 1.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .process-steps::before {
    display: none; /* 移动端隐藏连接线 */
  }
  
  .process-step {
    flex-direction: column;
    text-align: center;
  }
  
  .step-number {
    margin: 0 auto 1.5rem;
  }
}

/* FAQ部分样式 */
.faq-section {
  background-color: var(--background-color);
}

.faq-container {
  max-width: 900px;
  margin: 0 auto;
}

.faq-item {
  margin-bottom: 1.5rem;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: var(--card-background);
}

.faq-question {
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.faq-question:hover {
  background-color: rgba(var(--primary-color-rgb), 0.1);
}

.faq-question h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 500;
  color: var(--text-color-light);
}

.toggle-icon {
  color: var(--primary-color);
  transform: rotate(0deg);
  transition: transform 0.3s ease;
  font-size: 1.2rem;
}

.faq-answer {
  padding: 0 2rem;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
}

.faq-answer.active {
  padding: 0 2rem 1.5rem;
  max-height: 300px; /* 足够容纳内容的高度 */
}

.faq-answer p {
  margin: 0;
  color: var(--text-color-medium);
  line-height: 1.6;
}

/* 认养须知样式 */
.notes-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.note-card {
  background-color: var(--card-background);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  text-align: center;
}

.note-card:hover {
  transform: translateY(-5px);
}

.note-icon {
  margin: 0 auto 1.5rem;
  width: 70px;
  height: 70px;
  background-color: rgba(var(--primary-color-rgb), 0.2);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.8rem;
}

.note-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--text-color-light);
}

.note-card p {
  color: var(--text-color-medium);
  line-height: 1.6;
  text-align: left;
}

.notes-disclaimer {
  max-width: 1200px;
  margin: 3rem auto 0;
  padding: 1.5rem;
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 8px;
  color: var(--text-color-medium);
  line-height: 1.6;
  font-style: italic;
}

/* 底部号召性区域 */
.cta-bottom {
  background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/img/honey-jar.png');
  background-size: cover;
  background-position: center;
  text-align: center;
  color: #fff;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 2.8rem;
  margin-bottom: 1.5rem;
}

.cta-content p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .faq-question h3 {
    font-size: 1.1rem;
  }
  
  .cta-content h2 {
    font-size: 2rem;
  }
  
  .cta-content p {
    font-size: 1.2rem;
  }
}
</style> 