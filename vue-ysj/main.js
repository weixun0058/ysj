import { createApp } from 'vue'
import { createPinia } from 'pinia' // 引入 Pinia
import './style.css' // 导入全局样式一次
import 'leaflet/dist/leaflet.css'; // 导入 Leaflet CSS
import App from './App.vue'
import router from './router' // 导入路由配置
import { useAuthStore } from './stores/auth'; // 导入 auth store

// 引入 Font Awesome 图标库
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// 导入所有需要的 solid 图标 (如果需要 tree-shaking，可以按需导入)
import { fas } from '@fortawesome/free-solid-svg-icons'
library.add(fas) // 添加整个 solid 图标集

// 或者按需导入 specific icons
import { faShoppingCart, faPlusCircle, faEdit, faEye, faEyeSlash, faTrashAlt, faUser, faSearch, faHeart, faPhone, faEnvelope, faMapMarkerAlt, faChevronDown, faBars, faTimes,
  // 添加AdminLayout.vue中使用的其他图标
  faLeaf, faAngleRight, faAngleLeft, faTachometerAlt, faUsers, faBox, faNewspaper, faTags, faComments, faCog, faUserShield
} from '@fortawesome/free-solid-svg-icons'
library.add(faShoppingCart, faPlusCircle, faEdit, faEye, faEyeSlash, faTrashAlt, faUser, faSearch, faHeart, faPhone, faEnvelope, faMapMarkerAlt, faChevronDown, faBars, faTimes,
  // 添加AdminLayout.vue中使用的其他图标
  faLeaf, faAngleRight, faAngleLeft, faTachometerAlt, faUsers, faBox, faNewspaper, faTags, faComments, faCog, faUserShield
)

// 新增：导入 vue-toastification 及其 CSS
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)
const pinia = createPinia() // 创建 Pinia 实例

app.use(router) // 使用路由
app.use(pinia) // 应用 Pinia 插件

// 注册 Font Awesome 组件
app.component('font-awesome-icon', FontAwesomeIcon)

// 新增：使用 vue-toastification 插件，可以传递一些选项
const toastOptions = {
  // 你可以在这里添加全局配置，例如：
  // position: "top-right",
  // timeout: 5000,
  // closeOnClick: true,
  // pauseOnFocusLoss: true,
  // pauseOnHover: true,
  // draggable: true,
  // draggablePercent: 0.6,
  // showCloseButtonOnHover: false,
  // hideProgressBar: false,
  // closeButton: "button",
  // icon: true,
  // rtl: false
};
app.use(Toast, toastOptions);

// 初始化认证状态（使用立即执行的异步函数替代顶级await）
;(async () => {
  console.log('[main.js] Initializing authentication...'); // 新增日志
  const authStore = useAuthStore(pinia);
  try {
    await authStore.initializeAuth();
    console.log('[main.js] Authentication initialized successfully.'); // 新增日志
  } catch (error) {
    console.error("[main.js] Failed to initialize authentication:", error); // 修改日志
  } finally {
    // 确保应用在认证初始化后挂载
    console.log('[main.js] Mounting the app...'); // 新增日志
    app.mount('#app');
    console.log('[main.js] App mounted.'); // 新增日志
  }
})();
