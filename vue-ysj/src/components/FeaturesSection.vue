<template>
  <section class="features-section container">
    <h2>核心优势</h2>
    <div class="feature-list">
      <div class="feature-item">
        <i class="feature-icon"></i> <!-- 可以用图标库替换 -->
        <h3>地理标志保护</h3>
        <p>源自新疆伊犁尼勒克唐布拉，国家认证地理标志保护产区。</p>
      </div>
      <div class="feature-item">
        <i class="feature-icon"></i>
        <h3>珍稀新疆黑蜂</h3>
        <p>由生命力顽强、采蜜品质高的独特新疆黑蜂酿造。</p>
      </div>
      <div class="feature-item">
        <i class="feature-icon"></i>
        <h3>纯净无污染蜜源</h3>
        <p>天山深处，远离污染，万亩天然牧场，四季花开。</p>
      </div>
      <div class="feature-item">
        <i class="feature-icon"></i>
        <h3>原蜜直出无添加</h3>
        <p>遵循自然成熟法则，物理过滤，保留天然活性酶。</p>
      </div>
      <div class="feature-item">
        <i class="feature-icon"></i>
        <h3>权威认证</h3>
        <p>展示SGS、有机认证等权威背书。</p>
      </div>
    </div>
  </section>
</template>

<script setup>
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
  /* 创建响应式网格布局，根据屏幕宽度调整列数 */
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
}

.feature-item {
  background-color: var(--card-background);
  padding: 2rem 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(250, 150, 75, 0.1); /* 主色调的阴影 */
}

.feature-icon {
  /* 样式化你的图标，可以用背景图、字体图标或 SVG */
  display: block;
  width: 50px;
  height: 50px;
  background-color: var(--primary-color); /* 临时用主色调占位 */
  margin: 0 auto 1.5rem auto;
  border-radius: 50%; /* 可以是圆形背景 */
  /* mask: url('/path/to/icon.svg') no-repeat center / contain; 如果用 SVG 图标 */
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
</style> 