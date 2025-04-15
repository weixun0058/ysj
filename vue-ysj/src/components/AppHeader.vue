<template>
  <header class="app-header">
    <nav class="container">
      <div class="logo">
        <!-- 使用 public 目录下的 logo.svg -->
        <img src="/logo.svg" alt="壹世健 Logo" height="40">
      </div>
      <ul class="nav-links">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/brand-story">品牌研究院</router-link></li>
        <li><router-link to="/products">单花蜜系列</router-link></li>
        <li><router-link to="/gifts">主厨联名礼盒</router-link></li>
        <li><router-link to="/adoption">蜜蜂认养</router-link></li>
        <li><router-link to="/news">动态资讯</router-link></li>
        <li><router-link to="/contact">联系我们</router-link></li>
      </ul>
      <div class="user-actions">
        <a href="#login">登录/注册</a>
        <span class="separator">|</span>
        <a href="#cart">购物车</a>
      </div>
    </nav>
  </header>
</template>

<script setup>
// 如果需要逻辑，可以在这里添加
</script>

<style scoped>
.app-header {
  background-color: rgba(0, 0, 0, 0.8); /* 页眉可以带点透明 */
  padding: 1rem 0;
  position: sticky; /* 可以让页眉固定 */
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--border-color);
}

nav.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo img {
  display: block;
}

.nav-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  gap: 1.5rem; /* 链接间距 */
}

.nav-links a {
  color: var(--text-color-light);
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-links a:hover,
.user-actions a:hover {
  color: var(--primary-color);
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.user-actions a {
  color: var(--text-color-light);
  text-decoration: none;
}

.separator {
  color: var(--border-color);
}
</style> 