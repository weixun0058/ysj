<!-- 导航栏 -->
<template>
  <header class="app-header">
    <nav class="container">
      <div class="logo">
        <!-- 使用 public 目录下的 logo.svg -->
        <img src="/logo.svg" alt="壹世健 Logo" height="40">
      </div>
      <ul class="nav-links">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/brand-story">品牌故事</router-link></li>
        <li><router-link to="/products">产品中心</router-link></li>
        <li><router-link to="/brand-collaboration">联名定制</router-link></li>
        <li><router-link to="/adoption">认养计划</router-link></li>
        <li><router-link to="/news">动态资讯</router-link></li>
        <li><router-link to="/contact">联系我们</router-link></li>
      </ul>
      <div class="user-actions">
        <template v-if="isAuthenticated">
          <!-- <router-link to="/user-center">{{ currentUser?.username || '用户中心' }}</router-link> --> 
          <router-link to="/user-center">欢迎, {{ currentUser?.username || '用户' }}</router-link> <!-- 修改链接指向 /user-center -->
          <span class="separator">|</span>
          <!-- 为管理员添加管理后台入口 -->
          <router-link v-if="currentUser?.is_admin" to="/admin/dashboard" class="admin-link">管理后台</router-link>
          <span v-if="currentUser?.is_admin" class="separator">|</span>
          <a href="#" @click.prevent="handleLogout" class="logout-link">退出登录</a>
          <span class="separator">|</span>
          <router-link to="/cart">购物车</router-link>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <span class="separator">/</span>
          <router-link to="/register">注册</router-link>
          <span class="separator">|</span>
          <router-link to="/cart">购物车</router-link> <!-- 购物车通常也允许未登录访问 -->
        </template>
      </div>
      <!-- 移动端菜单按钮 -->
      <button class="mobile-menu-button" @click="toggleMobileMenu">菜单</button>
    </nav>
    <!-- 移动端菜单内容 (初始隐藏) -->
    <div class="mobile-menu" v-if="isMobileMenuOpen">
      <ul>
        <li><router-link to="/" @click="closeMobileMenu">首页</router-link></li>
        <li><router-link to="/brand-story" @click="closeMobileMenu">品牌故事</router-link></li>
        <li><router-link to="/products" @click="closeMobileMenu">产品中心</router-link></li>
        <li><router-link to="/brand-collaboration" @click="closeMobileMenu">联名定制</router-link></li>
        <li><router-link to="/adoption" @click="closeMobileMenu">蜜蜂认养计划</router-link></li>
        <li><router-link to="/news" @click="closeMobileMenu">最新动态资讯</router-link></li>
        <li><router-link to="/contact" @click="closeMobileMenu">联系我们</router-link></li>
        <li class="mobile-user-actions">
          <template v-if="isAuthenticated">
            <router-link to="/user-center" @click="closeMobileMenu">用户中心</router-link> <!-- 恢复移动端链接 -->
            <!-- 移动端也为管理员添加管理后台入口 -->
            <router-link v-if="currentUser?.is_admin" to="/admin/dashboard" @click="closeMobileMenu" class="admin-link">管理后台</router-link>
             <a href="#" @click.prevent="handleLogout" class="logout-link">退出登录</a>
          </template>
          <template v-else>
             <router-link to="/login" @click="closeMobileMenu">登录</router-link>
             <router-link to="/register" @click="closeMobileMenu">注册</router-link>
          </template>
           <router-link to="/cart" @click="closeMobileMenu">购物车</router-link>
        </li>
      </ul>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 导入 useRouter
import { useAuthStore } from '../stores/auth'; // 导入 auth store
import { storeToRefs } from 'pinia'; // 导入 storeToRefs 以保持响应性

const router = useRouter(); // 获取 router 实例
const authStore = useAuthStore();
const { isAuthenticated, currentUser } = storeToRefs(authStore); // 使用 storeToRefs 获取响应式状态

const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const handleLogout = () => {
  authStore.logout();
  closeMobileMenu(); // 如果在移动菜单中登出，也关闭菜单
  router.push('/login'); // 登出后跳转到登录页
};

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

.admin-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: bold;
}

.admin-link:hover {
  text-decoration: underline;
}

.separator {
  color: var(--border-color);
}

.mobile-menu-button {
  display: none; /* 默认隐藏 */
  background: none;
  border: none;
  color: var(--text-color-light);
  font-size: 1.5rem;
  cursor: pointer;
}

.mobile-menu {
  position: absolute;
  top: 100%; /* 紧贴 header 底部 */
  left: 0;
  width: 100%;
  background-color: rgba(17, 17, 17, 0.75); /* 使用 rgba 实现半透明深色背景 */
  padding: 1rem 0; /* 上下内边距 */
  border-top: 1px solid var(--border-color);
  z-index: 999; /* 添加 z-index */
}

.mobile-menu ul {
  list-style: none;
  padding: 0 1.5rem; /* 增加左右内边距 */
  margin: 0;
}

.mobile-menu li {
  padding: 1rem 0; /* 增加上下内边距 */
  border-bottom: 1px solid var(--border-color-light); /* 使用稍亮的分隔线 */
}
.mobile-menu li:last-child {
  border-bottom: none;
}

.mobile-menu a {
  color: var(--text-color-light);
  text-decoration: none;
  display: block; /* 让链接占满整行 */
  font-size: 1.1rem;
  font-weight: 500; /* 可以稍微加粗 */
}
.mobile-menu a:hover {
  color: var(--primary-color);
}

.mobile-user-actions {
    padding-top: 1rem; /* 与上方链接留出一些间距 */
}

.mobile-user-actions a {
    display: inline-block; /* 让登录/购物车在一行 */
    margin-right: 1.5rem; /* 调整间距 */
    font-size: 1rem; /* 可以稍小一点 */
}

.logout-link {
  color: var(--text-color-light); /* 保持与其它链接一致 */
  text-decoration: none;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  font: inherit;
}
.logout-link:hover {
  color: var(--primary-color); /* 悬停效果 */
}

/* 响应式调整 */
@media (max-width: 960px) {
  .nav-links,
  .user-actions {
    display: none; /* 隐藏桌面版导航和用户操作 */
  }

  .mobile-menu-button {
    display: block; /* 显示移动端菜单按钮 */
  }

  nav.container {justify-content: space-between;

    /* 如果需要在移动端调整 Logo 和按钮的位置，可以在这里添加样式 */
    /* 例如： justify-content: space-between; 已经有了 */
  }

  /* .mobile-menu 的 display 由 v-if 控制，此处无需规则 */
}
</style> 