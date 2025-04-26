import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'; // 假设我们把 App.vue 的内容移到 HomeView
import BrandStoryView from '../views/BrandStoryView.vue';
import NotFoundView from '../views/NotFoundView.vue';
import ProductsView from '../views/ProductsView.vue';
import ProductDetailView from '../views/ProductDetailView.vue';
import NewsView from '../views/NewsView.vue';
import NewsDetailView from '../views/NewsDetailView.vue';
import CreateNewsView from '../views/admin/CreateNewsView.vue';
// 导入文章管理相关组件
import ManageNewsView from '../views/admin/ManageNewsView.vue';
import EditNewsView from '../views/admin/EditNewsView.vue';
// 导入管理员用户管理界面
import UserManagementView from '../views/admin/UserManagementView.vue';
// 导入产品管理组件
import ProductManagementView from '../views/admin/ProductManagementView.vue';
// 导入网站设置组件
import SiteSettingsView from '../views/admin/SiteSettingsView.vue';
// 取消注释这些导入
import CartView from '../views/CartView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
// import GiftsView from '../views/GiftsView.vue';
import BeeAdoptionView from '../views/BeeAdoptionView.vue'; // 导入蜜蜂认养页面
import ContactView from '../views/ContactView.vue'; // 导入联系我们页面
import UserCenterView from '../views/UserCenterView.vue'; // 导入用户中心视图
import { useAuthStore } from '../stores/auth'; // 导入 auth store
import TestAuthView from '../views/TestAuthView.vue';
import BrandCollaborationView from '../views/BrandCollaborationView.vue'; // 导入联名合作页面

// 导入管理后台组件
import AdminLayout from '../layouts/AdminLayout.vue';
import DashboardView from '../views/admin/dashboard/DashboardView.vue';
// 移除管理员专用登录页导入
// import AdminLoginView from '../views/admin/AdminLoginView.vue';
import DevTestView from '../views/admin/DevTestView.vue'; // 导入测试视图
// 导入富文本编辑器测试页面
import TestEditorView from '../views/admin/TestEditorView.vue';

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
  // 添加联名定制页面路由
  {
    path: '/brand-collaboration',
    name: 'BrandCollaboration',
    component: BrandCollaborationView,
    meta: { title: '品牌联名合作 - 壹世健' }
  },
  // 启用产品中心路由
  {
    path: '/products',
    name: 'Products',
    component: ProductsView,
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: ProductDetailView,
    props: true
  },
  // 启用新闻相关路由
  {
    path: '/news',
    name: 'News',
    component: NewsView,
  },
  {
    path: '/news/:slug',
    name: 'NewsDetail', 
    component: NewsDetailView,
    props: true
  },
  {
    path: '/admin/news/create',
    name: 'CreateNews',
    component: CreateNewsView,
    meta: { requiresAdmin: true }
  },
  // 取消注释这些路由
  {
    path: '/cart',
    name: 'Cart',
    component: CartView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  /*
  {
    path: '/gifts',
    name: 'Gifts',
    component: GiftsView,
  },
  */
  // 添加蜜蜂认养页面路由
  {
    path: '/adoption',
    name: 'BeeAdoption',
    component: BeeAdoptionView,
    meta: { title: '蜜蜂认养 - 壹世健' }
  },
  // 添加联系我们页面路由
  {
    path: '/contact',
    name: 'Contact',
    component: ContactView,
    meta: { title: '联系我们 - 壹世健' }
  },
  {
    path: '/user-center',
    name: 'UserCenter',
    component: UserCenterView,
    meta: { requiresAuth: true }
  },

  // 添加测试认证路由
  {
    path: '/test-auth',
    name: 'TestAuth',
    component: TestAuthView,
  },
  
  // 添加富文本编辑器测试路由
  {
    path: '/test-editor',
    name: 'TestEditor',
    component: TestEditorView,
  },
  
  // 移除管理员专用登录路由
  // {
  //   path: '/admin/login',
  //   name: 'AdminLogin',
  //   component: AdminLoginView,
  //   meta: { adminLoginPage: true }
  // },
  
  // 管理后台路由组
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: DashboardView,
        meta: { title: '仪表盘' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: UserManagementView,
        meta: { title: '用户管理' }
      },
      {
        path: 'products',
        name: 'AdminProducts',
        component: ProductManagementView,
        meta: { title: '产品管理' }
      },
      {
        path: 'news/create',
        name: 'AdminCreateNews',
        component: CreateNewsView,
        meta: { title: '发布文章' }
      },
      // 添加文章管理路由
      {
        path: 'news',
        name: 'ManageNews',
        component: ManageNewsView,
        meta: { title: '文章管理' }
      },
      {
        path: 'news/edit/:id',
        name: 'EditNews',
        component: EditNewsView,
        props: true,
        meta: { title: '编辑文章' }
      },
      // 添加网站设置路由
      {
        path: 'settings',
        name: 'SiteSettings',
        component: SiteSettingsView,
        meta: { title: '网站设置' }
      },
      // 添加测试视图路由
      {
        path: 'dev-test',
        name: 'DevTest',
        component: DevTestView,
        meta: { title: 'API测试' }
      },
      // 添加富文本编辑器测试页面
      {
        path: 'test-editor',
        name: 'AdminTestEditor',
        component: TestEditorView,
        meta: { title: '富文本编辑器测试' }
      },
      // 未来会添加更多管理后台路由...
    ]
  },

  // 添加404页面路由，将匹配所有未匹配的路径
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  }
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

// --- 全局导航守卫 ---
router.beforeEach(async (to, from, next) => {
  // 确保 Pinia store 已经被初始化 (理论上 main.js 会先完成)
  const authStore = useAuthStore();

  // 尝试初始化（如果尚未完成）- 这个可能不需要，因为 main.js 已经做了
  // if (!authStore.token && localStorage.getItem('authToken')) {
  //   await authStore.initializeAuth();
  // }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  const guestOnly = to.matched.some(record => record.meta.guestOnly);
  const isAuthenticated = authStore.isAuthenticated; // 从 store 获取登录状态
  const isAdmin = authStore.currentUser?.is_admin; // 获取管理员状态

  // 处理需要管理员权限的路由
  if (requiresAdmin) {
    if (!isAuthenticated) {
      // 如果未登录，重定向到统一登录页
      return next({ 
        path: '/login', 
        query: { 
          redirect: to.fullPath,
          requireAdmin: 'true' // 添加标记，表示需要管理员权限
        } 
      });
    } 
    if (!isAdmin) {
      // 如果登录了但不是管理员，重定向到首页并提示权限不足
      // 可以考虑添加一个提示页面，或在登录页增加权限提示
      return next({ 
        path: '/login', 
        query: { 
          accessDenied: 'true',
          requireAdmin: 'true'
        }
      });
    }
    // 验证通过，继续访问
    return next();
  }

  // 处理需要普通用户权限的路由
  if (requiresAuth && !isAuthenticated) {
    // 如果目标路由需要认证但用户未登录，重定向到登录页
    return next({ path: '/login', query: { redirect: to.fullPath } });
  } 
  
  // 处理仅限游客访问的路由
  if (guestOnly && isAuthenticated) {
    // 如果目标路由只允许未登录用户访问（如登录、注册页），而已登录，则重定向到首页
    return next({ name: 'Home' });
  }
  
  // 其他情况，正常放行
  next();
});

export default router; 