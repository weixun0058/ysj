import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'; // 假设我们把 App.vue 的内容移到 HomeView
import BrandStoryView from '../views/BrandStoryView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/brand-story',
    name: 'BrandStory',
    component: BrandStoryView,
    // 可以在这里添加路由元信息，例如页面标题
    // meta: { title: '品牌故事 - 壹世健' }
  },
  // 在这里添加其他页面的路由，例如产品中心等
  // {
  //   path: '/products',
  //   name: 'Products',
  //   // 懒加载组件，提高初始加载速度
  //   component: () => import('../views/ProductsView.vue'),
  // },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 使用 HTML5 History 模式
  routes,
  // 路由切换时滚动到页面顶部
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

export default router; 