  <!-- 精选产品 -->
<template>
  <section class="products-section container">
    <h2>精选产品</h2>
    <div class="product-list">
      <div class="product-card">
        <!-- 产品图片占位 -->
        <div class="product-image-placeholder"></div>
        <h3>商务尊享套装</h3>
        <p>含水晶蜜勺+胡桃木礼盒，尽显尊贵。</p>
        <p class="price">¥XXX.XX</p>
        <button class="details-button">查看详情</button>
      </div>
      <div class="product-card">
        <div class="product-image-placeholder"></div>
        <h3>天山雪蜜</h3>
        <p>细腻如雪，口感独特，高海拔蜜源。</p>
        <p class="price">¥XXX.XX</p>
        <button class="details-button">查看详情</button>
      </div>
      <div class="product-card">
        <div class="product-image-placeholder"></div>
        <h3>稀有崖蜜</h3>
        <p>悬崖峭壁间的珍品，数量稀少。</p>
        <p class="price">¥XXX.XX</p>
        <button class="details-button">查看详情</button>
      </div>
      <!-- 可以添加更多产品 -->
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.products-section {
  padding: 4rem 1rem;
  text-align: center;
}

.products-section h2 {
  margin-bottom: 3rem;
  font-size: 2rem;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.product-card {
  background-color: var(--card-background);
  border-radius: 8px;
  overflow: hidden; /* 隐藏超出边界的内容 */
  border: 1px solid var(--border-color);
  text-align: left;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(250, 150, 75, 0.1);
}

.product-image-placeholder {
  height: 200px; /* 设定图片高度 */
  background-color: #333; /* 占位符颜色 */
  margin-bottom: 1rem;
  border-radius: 4px;
  /* 未来用 img 标签替换 */
  /* background-image: url('/img/product-image.jpg'); */
  background-size: cover;
  background-position: center;
}

.product-card h3 {
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
}

.product-card p {
  color: var(--text-color-light);
  opacity: 0.8;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.product-card .price {
  font-weight: bold;
  color: var(--primary-color);
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
}

.details-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 500;
  width: 100%; /* 让按钮占满卡片宽度 */
}

.details-button:hover {
  background-color: #ffab6f;
}
</style> 