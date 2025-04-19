<!-- 探索更多 -->
<template>
  <section class="entry-points-section container">
    <h2>探索更多</h2>
    <div class="entry-list">
      <div class="entry-item">
        <i class="entry-icon"></i>
        <h3>品牌故事</h3>
        <p>了解塞外本草与壹世健的缘起与坚守。</p>
        <a href="#brand-story" class="entry-link">深入了解 &rarr;</a>
      </div>
      <div class="entry-item">
        <i class="entry-icon"></i>
        <h3>蜜蜂认养计划</h3>
        <p>成为蜂巢守护者，获取专属溯源与福利。</p>
        <a href="#adoption" class="entry-link">立即认养 &rarr;</a>
      </div>
      <div class="entry-item">
        <i class="entry-icon"></i>
        <h3>动态资讯</h3>
        <p>获取最新品牌动态与蜂蜜知识。</p>
        <a href="#news" class="entry-link">查看动态 &rarr;</a>
      </div>
      <div class="entry-item">
        <i class="entry-icon"></i>
        <h3>溯源系统</h3>
        <p>输入编码，追溯您的蜂蜜之旅。</p>
        <a href="#traceability" class="entry-link">开始溯源 &rarr;</a>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.entry-points-section {
  padding: 4rem 1rem;
  text-align: center;
  background-color: var(--card-background); /* 可以给这个区域一个略微不同的背景 */
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.entry-points-section h2 {
  margin-bottom: 3rem;
  font-size: 2rem;
}

.entry-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.entry-item {
  background-color: var(--background-color); /* 内部卡片用主背景色 */
  padding: 2rem 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.entry-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(250, 150, 75, 0.1);
}

.entry-icon {
  display: block;
  width: 45px;
  height: 45px;
  background-color: var(--primary-color);
  margin: 0 auto 1.5rem auto;
  border-radius: 50%;
}

.entry-item h3 {
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.entry-item p {
  color: var(--text-color-light);
  opacity: 0.8;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.entry-link {
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.entry-link:hover {
  text-decoration: underline;
}
</style> 