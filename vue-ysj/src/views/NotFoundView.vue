<template>
  <div class="not-found-page">
    <div class="container">
      <h1>页面不存在</h1>
      <p>您访问的页面可能已被移除或正在开发中。</p>
      <router-link to="/" class="home-link">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found-page {
  padding: 4rem 0;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 2rem;
  color: var(--text-color-light);
  opacity: 0.8;
}

.home-link {
  display: inline-block;
  padding: 0.8rem 2rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border-radius: 4px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s;
}

.home-link:hover {
  background-color: #ffab6f;
}
</style> 