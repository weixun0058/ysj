<!-- 核心优势 -->
<template>
  <section class="features-section container">
    <h2>核心优势</h2>
    <div class="feature-list">
      <div class="feature-item" v-for="feature in features" :key="feature.title">
        <span class="feature-emoji">{{ feature.emoji }}</span>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

// 使用 Emoji 代替 Font Awesome 图标
const features = ref([
  { emoji: '🐝', title: '珍稀新疆黑蜂', desc: '由生命力顽强、采蜜品质高的独特新疆黑蜂酿造。' },
  { emoji: '🏔️', title: '纯净无污染蜜源', desc: '天山深处，远离污染，万亩天然牧场，四季花开。' },
  { emoji: '🍯', title: '原蜜直出无添加', desc: '遵循自然成熟法则，物理过滤，保留天然活性酶。' },
  { emoji: '🛡️', title: '无菌灌装工艺', desc: '无菌灌装，确保每一滴蜜都纯净无污染。' },
  { emoji: '📍', title: '地理标志保护', desc: '源自新疆伊犁尼勒克唐布拉，国家认证地理标志保护产区。' },
  { emoji: '✅', title: '权威认证', desc: '展示 SGS 等权威背书。' }
]);
</script>

<style scoped>
.features-section {
  padding: 4rem 1rem; /* 上下边距 */
  text-align: center;
}

.features-section h2 {
  margin-bottom: 3rem;
  font-size: 2rem;
}

.feature-list {
  display: grid;
  /* 默认（桌面端）设置为 3 列 */
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.feature-item {
  background-color: var(--card-background);
  padding: 2rem 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex; /* 使用 Flexbox 垂直居中（如果需要） */
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 水平居中 */
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(250, 150, 75, 0.1); /* 主色调的阴影 */
}

/* 4. 为 FontAwesomeIcon 添加样式 */
.feature-item .feature-emoji {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.feature-item h3 {
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.feature-item p {
  color: var(--text-color-light);
  opacity: 0.8;
  font-size: 0.95rem;
}

/* 响应式调整 */
@media (max-width: 960px) {
  .feature-list {
    /* 移动端恢复使用 auto-fit，允许 2 列或 1 列 */
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem; /* 可以适当减小移动端间距 */
  }

  .feature-item {
      padding: 1.5rem 1rem; /* 减小卡片内边距 */
  }

  .features-section h2 {
      font-size: 1.8rem; /* 减小标题字体 */
      margin-bottom: 2rem;
  }

  .feature-item h3 {
      font-size: 1.1rem;
  }

  .feature-item p {
      font-size: 0.9rem;
  }
}
</style> 