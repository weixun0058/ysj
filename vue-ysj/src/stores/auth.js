import { defineStore } from 'pinia';
import axios from 'axios'; // 假设使用 axios 发送请求

// 辅助函数：从 localStorage 获取数据
const getFromLocalStorage = (key, defaultValue = null) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    const item = window.localStorage.getItem(key);
    try {
      return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
      console.error(`Error parsing localStorage item ${key}:`, e);
      window.localStorage.removeItem(key); // 如果解析错误，则移除该项
      return defaultValue;
    }
  }
  return defaultValue;
};

// 辅助函数：向 localStorage 存储数据
const saveToLocalStorage = (key, value) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.error(`Error saving to localStorage item ${key}:`, e);
    }
  }
};

// 辅助函数：从 localStorage 移除数据
const removeFromLocalStorage = (key) => {
  if (typeof window !== 'undefined' && window.localStorage) {
    window.localStorage.removeItem(key);
  }
};


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: getFromLocalStorage('authToken'),
    user: getFromLocalStorage('authUser'), // 存储整个用户对象可能更方便
    // isAuthenticated 最好是计算属性 (getter) 或在 action 中显式设置
    // status: null, // 可以用来跟踪加载状态 'loading', 'success', 'error'
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    currentUser: (state) => state.user,
    getToken: (state) => state.token,
  },

  actions: {
    // 1. 初始化：应用启动时调用，尝试从 localStorage 恢复状态
    async initializeAuth() {
      const token = getFromLocalStorage('authToken');
      if (token) {
        this.token = token;
        // 设置 Axios 默认请求头
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        // 尝试获取用户信息，如果 localStorage 没有或已过期
        if (!this.user) {
          await this.fetchUser();
        } else {
          // 如果 localStorage 有用户信息，可以考虑进行一次静默验证
          // await this.fetchUser(); // 或者信任 localStorage 的数据
        }
      } else {
        this.logout(); // 确保没有 token 时状态是干净的
      }
    },

    // 2. 登录
    async login(credentials) {
      // this.status = 'loading';
      try {
        // 准备发送给后端的数据，确保字段名为 login 和 password
        const loginPayload = {
            login: credentials.username || credentials.login, // 兼容直接传入 login 或 username 的情况
            password: credentials.password
        };
        if (!loginPayload.login || !loginPayload.password) {
            throw new Error("用户名/邮箱和密码不能为空"); // 前端也做个校验
        }

        // 注意: URL 应指向实际的后端 API 端点
        const response = await axios.post('/api/login', loginPayload); 
        const { access_token } = response.data;

        if (access_token) {
          this.token = access_token;
          // --- FRONTEND DEBUG PRINT --- 
          // console.log('[DEBUG authStore.login] Token received and set:', this.token);
          // --- END DEBUG ---
          saveToLocalStorage('authToken', access_token);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`; // 仍然保留默认设置，以防万一
          
          // --- FRONTEND DEBUG PRINT --- 
          // console.log('[DEBUG authStore.login] Token before calling fetchUser:', this.token);
          // --- END DEBUG ---
          await this.fetchUser(); 
          if (!this.user) {
              // --- FRONTEND DEBUG PRINT --- 
              // console.error('[DEBUG authStore.login] fetchUser completed but this.user is still null!');
              // --- END DEBUG ---
              throw new Error('Login succeeded but failed to fetch user details.');
          }
          // this.status = 'success';
          return true; // 表示登录成功
        } else {
          throw new Error('Login failed: Invalid response from server (missing token)');
        }
      } catch (error) {
        console.error('Login error:', error.response?.data || error.message);
        this.logout(); // 登录失败时清除状态
        // this.status = 'error';
        throw error; // 将错误向上抛出，方便 UI 处理
      }
    },

    // 3. 注册
    async register(userData) {
      // this.status = 'loading';
      try {
        // 注意: URL 应指向实际的后端 API 端点
        await axios.post('/api/register', userData);
        // 注册成功后尝试自动登录
        // this.status = 'success'; // 注册本身成功
        // --- 修改：传递给 login 的对象需要匹配 login action 的期望格式 (username/password) ---
        await this.login({ username: userData.username, password: userData.password });
        return true; // 表示注册并登录成功
      } catch (error) {
        console.error('Registration error:', error.response?.data || error.message);
        // this.status = 'error';
        throw error; // 将错误向上抛出
      }
    },

    // 4. 获取当前用户信息
    async fetchUser() {
      // --- FRONTEND DEBUG PRINT --- 
      // console.log('[DEBUG authStore.fetchUser] fetchUser called. Token at start:', this.token);
      // --- END DEBUG ---
      if (!this.token) {
           // console.warn('fetchUser called without a token.'); 
           return; 
      }
      // this.status = 'loading';
      try {
        // --- FRONTEND DEBUG PRINT --- 
        const headers = {
            'Authorization': `Bearer ${this.token}`
        };
        // console.log('[DEBUG authStore.fetchUser] Headers to be sent:', headers);
        // --- END DEBUG ---
        const response = await axios.get('/api/me', { headers }); 
        // ---------------------------------------
        this.user = response.data;
        // --- FRONTEND DEBUG PRINT --- 
        // console.log('[DEBUG authStore.fetchUser] User data received:', this.user);
        // --- END DEBUG ---
        saveToLocalStorage('authUser', this.user); // 更新 localStorage 中的用户信息
        // this.status = 'success';
      } catch (error) {
         // console.error('Fetch user error:', error.response?.data || error.message);
         if (error.response && error.response.status === 401) {
            // console.warn('Token seems invalid during fetchUser. Logging out.'); 
            this.logout();
         }
      }
    },

    // 5. 登出
    logout() {
      this.token = null;
      this.user = null;
      removeFromLocalStorage('authToken');
      removeFromLocalStorage('authUser');
      // 清除 Axios 默认请求头
      delete axios.defaults.headers.common['Authorization'];
      // this.status = null;
      // 可以选择重定向到登录页，但这通常在路由守卫或组件中处理
      // router.push('/login');
    },

    // 6. 更新用户信息 (示例，如果允许用户在前端修改信息)
    async updateUserProfile(profileData) {
        if (!this.isAuthenticated) return false;
        try {
            // 调用后端 PUT /api/me
            const response = await axios.put('/api/me', profileData);
            // 更新本地 user state (如果后端返回了更新后的 user)
            if (response.data && response.data.user) { // 假设后端可能返回更新后的用户
              this.user = response.data.user;
            } else {
              // 如果后端只返回成功消息，则合并更新
              this.user = { ...this.user, ...profileData };
            }
            saveToLocalStorage('authUser', this.user); // 更新 localStorage
            return true;
        } catch (error) {
            console.error('Update profile error:', error.response?.data || error.message);
            throw error; // 抛出错误供 UI 处理
        }
    },

    // --- 新增：修改密码 Action ---
    async changePassword(passwordData) {
        // passwordData 应包含 { currentPassword, newPassword }
        if (!this.isAuthenticated) return false;
        try {
            // 调用新的后端接口
            await axios.put('/api/me/password', {
                current_password: passwordData.currentPassword,
                new_password: passwordData.newPassword
            });
            // 密码修改成功，可以选择性地做一些事情，例如：
            // 1. 提示用户成功
            // 2. 强制用户重新登录 (更安全，但体验稍差)
            //    this.logout(); 
            //    router.push('/login?passwordChanged=true'); 
            return true; // 表示密码修改成功
        } catch (error) {
            console.error('Change password error:', error.response?.data || error.message);
            throw error; // 抛出错误供 UI 处理
        }
    }
    // --- 修改密码 Action 结束 ---

  },
});

// 可以在这里添加一个 axios 拦截器来处理 401 错误，自动登出
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      // 确保不是登录或注册接口本身的 401 错误
      const originalRequestUrl = error.config.url;
      if (!originalRequestUrl.endsWith('/api/login') && !originalRequestUrl.endsWith('/api/register')) {
          // console.warn('Unauthorized request or token expired. Logging out.');
          authStore.logout();
          // 可以考虑跳转到登录页，但最好在路由守卫里做
          // window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// 应用启动时初始化认证状态
// 注意：如果在 store 文件外部调用 useAuthStore，需要确保 Pinia 实例已创建并传递给它
// 或者在 main.js 或 App.vue 中调用 initializeAuth
// export function initializeAuthentication() {
//   const authStore = useAuthStore();
//   authStore.initializeAuth();
// } 