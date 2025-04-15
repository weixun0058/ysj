<template>
  <div class="brand-story-page">
    <!-- 1. Hero Section -->
    <section class="story-hero">
      <div class="hero-background" style="background-image: url('/img/story-hero-bg.jpg');"></div> <!-- 替换为实际背景图 -->
      <div class="hero-overlay"></div>
      <div class="hero-content container">
        <h1>天山深处的黑黄金<br/>国家地理标志的甜蜜馈赠</h1>
        <p>源自新疆伊犁尼勒克唐布拉，每一滴都是自然与时间的沉淀。</p>
      </div>
    </section>

    <!-- 2. Origin Section (地理标志与产区) -->
    <section class="story-section origin-section container">
      <div class="section-content">
        <div class="text-content">
          <h2>黄金蜜域 · 新疆伊犁尼勒克</h2>
          <p>北纬43°的馈赠，天山北麓的尼勒克唐布拉草原，与法国普罗旺斯薰衣草园、新西兰麦卢卡产区齐名的世界级蜜源地。这里拥有国家认证的"地理标志保护产品"身份，是品质与珍稀的象征。</p>
          <ul>
            <li><i class="icon-altitude"></i> 高海拔纯净：远离工业污染，雪山融水滋养。</li>
            <li><i class="icon-flora"></i> 76种药花蜜源：天山雪莲、贝母、党参等赋予蜂蜜独特营养。</li>
            <li><i class="icon-climate"></i> 独特小气候：昼夜温差大，利于糖分积累与风味形成。</li>
          </ul>
          <img src="/img/geo-logo.png" alt="地理标志保护产品 Logo" class="geo-logo"> <!-- 替换为实际 Logo -->
        </div>
        <div class="visual-content">
          <img src="/img/tangbula-map.png" alt="尼勒克唐布拉地图" class="map-image"> <!-- 替换为实际地图图片 -->
          <!-- <img src="/img/geo-cert.jpg" alt="地理标志证书" class="cert-image"> 证书可放画廊 -->
        </div>
      </div>
    </section>

    <!-- 3. Black Bee Section (新疆黑蜂) -->
    <section class="story-section black-bee-section">
        <div class="section-background" style="background-image: url('/img/black-bee-bg.png');"></div> <!-- 替换为实际背景图 -->
        <div class="section-overlay"></div>
        <div class="section-content container text-center">
          <h2>世界四大名蜂 · 新疆黑蜂传奇</h2>
          <p>全球仅存的珍稀蜂种，生命力顽强，拥有惊人的"六边形战士"般的能力：抗寒、高飞、定向准、采蜜足、寿命长、品质优。一年仅取一次成熟蜜，其活性酶含量远超普通蜂蜜。</p>
          <div class="bee-features">
              <div><i class="icon-snowflake"></i> 抗寒耐劳</div>
              <div><i class="icon-mountain"></i> 高原飞行</div>
              <div><i class="icon-honeycomb"></i> 高活性酶</div>
          </div>
          <img src="/img/black-bee-detail.jpg" alt="新疆黑蜂特写" class="bee-image-detail"> <!-- 替换为实际图片 -->
      </div>
    </section>

    <!-- 4. Nectar & Craft Section (花源、功效与工艺) -->
    <section class="story-section nectar-craft-section container">
      <h2>76味天山药花蜜韵 · 百年匠心酿造之道</h2>
      <div class="section-grid">
        <div class="grid-item">
          <img src="/img/nectar-flora.png" alt="天山花卉"> <!-- 替换图片 -->
          <h3>药食同源 天赋滋养</h3>
          <p>采集雪莲、贝母、党参、益母草等76种天山独有药用植物精华，赋予蜂蜜独特的营养价值与风味层次。</p>
        </div>
        <div class="grid-item">
           <img src="/img/health-benefits.png" alt="蜂蜜功效"> <!-- 替换图片 -->
          <h3>多重功效 自然呵护</h3>
          <p>润肠通便、美容养颜、改善睡眠、增强免疫... 天然能量，呵护全家健康。</p>
        </div>
        <div class="grid-item">
           <img src="/img/craftsmanship.png" alt="酿造工艺"> <!-- 替换图片 -->
          <h3>百年技艺 现代标准</h3>
          <p>传承百年养蜂智慧，结合现代无菌灌装工艺，保留原蜜活性，确保每一瓶都纯净、安全。</p>
        </div>
      </div>
    </section>

    <!-- 5. Social Impact Section (社会责任) -->
     <section class="story-section social-impact-section">
      <div class="section-content container">
          <div class="visual-content">
            <img src="/img/beekeeper.png" alt="快乐的蜂农"> 
          </div>
          <div class="text-content">
              <h2>守护黑蜂家园 · 共酿甜蜜事业</h2>
              <p>我们与当地300余户蜂农紧密合作，提供技术支持与稳定收购，参与国家认证的扶贫项目，将这份来自天山的甜蜜，转化为助力乡村振兴的力量，共同守护这片珍贵的黑蜂家园。</p>
              <!-- <img src="/img/csr-cert.png" alt="扶贫认证"> 可选 -->
          </div>
      </div>
    </section>

    <!-- 6. Certificates Gallery (证书画廊 - 可选独立组件) -->
    <section class="story-section certificates-section container">
        <h2>权威认证 品质保障</h2>
        <div class="certificate-gallery">
            <!-- 循环展示证书图片 -->
            <img src="/img/cert-geo.png" alt="地理标志认证"> <!-- 替换 -->
            <img src="/img/cert-sgs.png" alt="SGS认证"> <!-- 替换 -->
            <img src="/img/cert-organic.png" alt="有机认证 (如有)"> <!-- 替换 -->
            <!-- 更多证书 -->
        </div>
    </section>

    <!-- 7. Story CTA (行动号召) -->
    <section class="story-cta text-center">
        <div class="container">
            <h3>探索源自天山的纯净之选</h3>
            <router-link to="/products" class="cta-button">查看所有产品</router-link>
            <!-- 或链接到特定产品 -->
            <!-- <router-link to="/products/tian-shan-snow-honey" class="cta-button">品尝天山雪蜜</router-link> -->
        </div>
    </section>

  </div>
</template>

<script setup>
// 如果需要，可以在这里导入子组件或添加逻辑
import { onMounted } from 'vue';

onMounted(() => {
  // 可以在这里设置页面标题
  document.title = '品牌故事 - 壹世健';
});
</script>

<style scoped>
/* 通用 Section 样式 */
.story-section {
  padding: 5rem 0;
  position: relative;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1rem;
  position: relative;
  z-index: 2;
}

h2 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

p {
  color: var(--text-color-light);
  opacity: 0.9;
  line-height: 1.8;
  margin-bottom: 1.5rem;
}

.text-center { text-align: center; }

/* Section 背景和覆盖层 */
.section-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  z-index: 0;
}
.section-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* 调整透明度 */
  z-index: 1;
}

/* 1. Hero Section */
.story-hero {
  height: 70vh; /* 调整高度 */
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  color: #fff;
}
.story-hero .hero-background {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-size: cover; background-position: center center;
    filter: brightness(0.7);
}
.story-hero .hero-overlay {
     position: absolute; top: 0; left: 0; width: 100%; height: 100%;
     background: linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0.1)); /* 底部渐变加深 */
     z-index: 1;
}
.story-hero .hero-content {
   position: relative; z-index: 2;
}
.story-hero h1 {
  font-size: 3.5rem;
  color: #fff;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
}
.story-hero p {
  font-size: 1.3rem;
  color: #eee;
  opacity: 1;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
}

/* 2. Origin Section */
.origin-section .section-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}
.origin-section ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 2rem;
}
.origin-section li {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}
.origin-section .icon-altitude, .icon-flora, .icon-climate {
  /* 替换为实际图标 */
  display: inline-block; width: 24px; height: 24px; background-color: var(--primary-color); margin-right: 0.8rem; border-radius: 50%;
}
.origin-section .geo-logo {
  max-width: 150px;
  margin-top: 1rem;
}
.origin-section .map-image {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* 3. Black Bee Section */
.black-bee-section {
  color: #fff;
}
.black-bee-section .section-content {
   padding: 6rem 1rem;
}
.black-bee-section h2 {
  color: #fff;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
}
.black-bee-section p {
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  font-size: 1.1rem;
  color: #eee;
}
.bee-features {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin: 2.5rem 0;
}
.bee-features div {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
}
.bee-features i {
   display: block; width: 40px; height: 40px; background-color: var(--primary-color); margin-bottom: 0.8rem; border-radius: 50%;
}
.black-bee-section .bee-image-detail {
    max-width: 300px;
    margin-top: 2rem;
    border-radius: 50%;
    border: 5px solid var(--primary-color);
}

/* 4. Nectar & Craft Section */
.nectar-craft-section h2 {
    margin-bottom: 3rem;
}
.nectar-craft-section .section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}
.nectar-craft-section .grid-item {
  background-color: var(--card-background);
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  border: 1px solid var(--border-color);
}
.nectar-craft-section .grid-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}
.nectar-craft-section .grid-item h3 {
  margin-bottom: 1rem;
  font-size: 1.4rem;
}
.nectar-craft-section .grid-item p {
  font-size: 0.95rem;
  opacity: 0.8;
}

/* 5. Social Impact Section */
.social-impact-section .section-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}
.social-impact-section .visual-content img {
  width: 100%;
  border-radius: 8px;
}
.social-impact-section h2 {
    text-align: left;
    margin-bottom: 1rem;
}

/* 6. Certificates Section */
.certificates-section {
    background-color: var(--card-background);
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
}
.certificates-section h2 {
    margin-bottom: 3rem;
}
.certificate-gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
}
.certificate-gallery img {
  height: 150px;
  border: 1px solid var(--border-color);
  padding: 0.5rem;
  background-color: var(--background-color);
  cursor: pointer; /* Add zoom effect later */
  transition: transform 0.3s ease;
}
.certificate-gallery img:hover {
    transform: scale(1.05);
}

/* 7. Story CTA */
.story-cta {
  padding: 4rem 0;
  background-color: var(--primary-color);
}
.story-cta h3 {
  color: var(--text-color-dark);
  font-size: 2rem;
  margin-bottom: 1.5rem;
}
.cta-button {
  padding: 0.8rem 2.5rem;
  font-size: 1.1rem;
  background-color: var(--background-color);
  color: var(--text-color-light);
  border: 2px solid var(--background-color);
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.cta-button:hover {
  background-color: transparent;
  color: var(--text-color-dark);
  border-color: var(--text-color-dark);
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .origin-section .section-content,
  .social-impact-section .section-content {
    grid-template-columns: 1fr; /* Stack columns */
  }
  .social-impact-section .text-content {
      order: -1; /* Move text above image on mobile */
      text-align: center;
  }
   .social-impact-section h2 {
      text-align: center;
   }
   .origin-section .visual-content {
      margin-top: 2rem;
   }
}

@media (max-width: 768px) {
  h2 { font-size: 2rem; }
  .story-hero h1 { font-size: 2.5rem; }
  .story-hero p { font-size: 1.1rem; }
  .bee-features { gap: 1.5rem; flex-wrap: wrap; }
  .certificate-gallery img { height: 120px; }
}

</style> 