<!-- 管理后台布局 -->
<template>
  <div class="admin-layout">
    <!-- 侧边栏导航 -->
    <aside :class="['admin-sidebar', {'collapsed': isSidebarCollapsed}]">
      <div class="sidebar-header">
        <div class="logo-container">
          <i class="fas fa-leaf logo-icon"></i>
          <span v-if="!isSidebarCollapsed" class="brand-name">壹世健管理系统</span>
        </div>
        <button class="toggle-btn" @click="toggleSidebar">
          <i :class="isSidebarCollapsed ? 'fas fa-angle-right' : 'fas fa-angle-left'"></i>
        </button>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/admin/dashboard" class="nav-item">
          <i class="fas fa-tachometer-alt"></i>
          <span v-if="!isSidebarCollapsed">仪表盘</span>
        </router-link>
        
        <router-link to="/admin/users" class="nav-item">
          <i class="fas fa-users"></i>
          <span v-if="!isSidebarCollapsed">用户管理</span>
        </router-link>
        
        <router-link to="/admin/products" class="nav-item">
          <i class="fas fa-box"></i>
          <span v-if="!isSidebarCollapsed">产品管理</span>
        </router-link>
        
        <router-link to="/admin/news" class="nav-item">
          <i class="fas fa-newspaper"></i>
          <span v-if="!isSidebarCollapsed">文章管理</span>
        </router-link>
        
        <router-link to="/admin/orders" class="nav-item">
          <i class="fas fa-shopping-cart"></i>
          <span v-if="!isSidebarCollapsed">订单管理</span>
        </router-link>
        
        <router-link to="/admin/categories" class="nav-item">
          <i class="fas fa-tags"></i>
          <span v-if="!isSidebarCollapsed">分类管理</span>
        </router-link>
        
        <router-link to="/admin/comments" class="nav-item">
          <i class="fas fa-comments"></i>
          <span v-if="!isSidebarCollapsed">评论管理</span>
        </router-link>
        
        <router-link to="/admin/settings" class="nav-item">
          <i class="fas fa-cog"></i>
          <span v-if="!isSidebarCollapsed">网站设置</span>
        </router-link>
        
        <router-link to="/admin/admins" class="nav-item">
          <i class="fas fa-user-shield"></i>
          <span v-if="!isSidebarCollapsed">管理员</span>
        </router-link>
      </nav>
    </aside>

    <!-- 主要内容区域 -->
    <div :class="['admin-main', {'expanded': isSidebarCollapsed}]">
      <!-- 顶部导航 -->
      <header class="admin-header">
        <div class="header-left">
          <button class="mobile-toggle" @click="toggleSidebar">
            <i class="fas fa-bars"></i>
          </button>
          <h2>{{ currentPageTitle }}</h2>
        </div>
        <div class="header-right">
          <div class="user-dropdown">
            <div class="user-info">
              <span>{{ user?.username || '管理员' }}</span>
              <i class="fas fa-chevron-down"></i>
            </div>
            <div class="dropdown-menu">
              <a href="/" target="_blank">前往网站</a>
              <button @click="logout">退出登录</button>
            </div>
          </div>
        </div>
      </header>
      
      <!-- 内容区域 -->
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const user = computed(() => authStore.currentUser);

// 侧边栏折叠状态
const isSidebarCollapsed = ref(false);

// 根据当前路由计算页面标题
const currentPageTitle = computed(() => {
  // 可以根据路由路径匹配标题
  const pathToTitle = {
    '/admin/dashboard': '仪表盘',
    '/admin/users': '用户管理',
    '/admin/news': '文章管理',
    '/admin/news/create': '发布文章',
    '/admin/products': '产品管理',
    '/admin/orders': '订单管理',
  };
  
  // 优先使用路由元数据中的标题
  return route.meta.title || pathToTitle[route.path] || '管理系统';
});

// 切换侧边栏折叠状态
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// 登出
const logout = () => {
  authStore.logout();
  router.push('/login');
};

// 检查认证状态
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    router.push('/admin/login');
  }
}, { immediate: true });

// 组件挂载时检查认证状态
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/admin/login');
  }
});
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* 侧边栏样式 */
.admin-sidebar {
  width: 250px;
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
  transition: width 0.3s ease;
  flex-shrink: 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.admin-sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color, #444);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  font-size: 2rem;
  color: var(--primary-color, #fa964b);
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-weight: bold;
  font-size: 1.2rem;
  white-space: nowrap;
}

.toggle-btn {
  background: transparent;
  border: none;
  color: var(--text-color-light, #f0f0f0);
  cursor: pointer;
  font-size: 1.2rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.8rem 1.5rem;
  color: var(--text-color-light, #f0f0f0);
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.router-link-active {
  background-color: var(--primary-color, #fa964b);
  color: var(--text-color-dark, #333);
}

.nav-item i {
  margin-right: 0.8rem;
  width: 20px;
  text-align: center;
}

/* 主内容区样式 */
.admin-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
}

.admin-header {
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color, #444);
}

.header-left {
  display: flex;
  align-items: center;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--text-color-light, #f0f0f0);
  font-size: 1.5rem;
  cursor: pointer;
  margin-right: 1rem;
}

.header-left h2 {
  margin: 0;
  font-size: 1.5rem;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: var(--card-background, #1a1a1a);
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  min-width: 150px;
  z-index: 100;
  display: none;
  overflow: hidden;
}

.user-dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-menu a,
.dropdown-menu button {
  display: block;
  padding: 0.8rem 1rem;
  color: var(--text-color-light, #f0f0f0);
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.dropdown-menu a:hover,
.dropdown-menu button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.admin-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: var(--background-color, #000);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    height: 100%;
    transform: translateX(0);
    transition: transform 0.3s ease, width 0.3s ease;
  }
  
  .admin-sidebar.collapsed {
    transform: translateX(-100%);
  }
  
  .admin-main {
    margin-left: 0 !important;
  }
  
  .mobile-toggle {
    display: block;
  }
}
</style> 