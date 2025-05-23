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
      console.log('[AuthStore] Attempting login with credentials:', credentials); // 新增日志
      try {
        // 准备发送给后端的数据
        const loginPayload = {
          login: credentials.login || credentials.username, // 支持login或username字段
          password: credentials.password
        };

        if (!loginPayload.login || !loginPayload.password) {
          throw new Error("登录标识和密码不能为空");
        }

        // 发送登录请求
        console.log('[AuthStore] Sending login request to /api/login with payload:', loginPayload); // 新增日志
        const response = await axios.post('/api/login', loginPayload);
        console.log('[AuthStore] Login response received:', response); // 新增日志

        // --- 开始: 重点检查响应和令牌提取 ---
        if (!response || !response.data) {
          console.error('[AuthStore] Login failed: Invalid response received from server.');
          throw new Error('登录失败：服务器返回无效响应');
        }
        console.log('[AuthStore] Login response data:', response.data); // 详细打印响应数据

        const { access_token } = response.data;
        console.log('[AuthStore] Extracted access_token:', access_token ? access_token.substring(0, 15) + '...' : 'undefined'); // 打印提取的令牌

        if (access_token) {
          this.token = access_token;
          console.log('[AuthStore] Saving token to localStorage:', access_token.substring(0, 15) + '...'); // 确认保存
          saveToLocalStorage('authToken', access_token);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
          console.log('[AuthStore] Set Axios default header.'); // 确认设置请求头

          // --- 结束: 重点检查响应和令牌提取 ---

          await this.fetchUser();
          if (!this.user) {
             console.error('[AuthStore] Login succeeded but failed to fetch user info.');
             // 即使获取用户信息失败，也认为登录基本成功，可能只是用户信息接口问题
             // throw new Error('登录成功但获取用户信息失败'); // 先注释掉，避免因 fetchUser 失败导致登录中断
             return true; // 返回成功状态
          }
          console.log('[AuthStore] User info fetched successfully:', this.user);
          return true; // 表示登录成功
        } else {
          console.error('[AuthStore] Login failed: access_token not found in response data.');
          throw new Error('登录失败：服务器响应中缺少 access_token');
        }
      } catch (error) {
        console.error('[AuthStore] Login error caught:', error); // 打印捕获的完整错误
        // 检查是网络错误还是后端返回的错误
        if (error.response) {
          // 请求已发出，但服务器响应状态码不在 2xx 范围
          console.error('[AuthStore] Login error response data:', error.response.data);
          console.error('[AuthStore] Login error response status:', error.response.status);
          console.error('[AuthStore] Login error response headers:', error.response.headers);
        } else if (error.request) {
          // 请求已发出，但没有收到响应
          console.error('[AuthStore] Login error request:', error.request);
        } else {
          // 在设置请求时触发了一些错误
          console.error('[AuthStore] Login setup error message:', error.message);
        }
        this.logout(); // 登录失败时清除状态
        throw error; // 将错误向上抛出，方便 UI 处理
      }
    },

    // 3. 注册
    async register(userData) {
      try {
        // 发送注册请求，支持所有新字段
        const response = await axios.post('/api/register', userData);
        
        // 检查是否直接返回了token（自动登录）
        if (response.data && response.data.access_token) {
          // 直接使用返回的token，不需要再进行登录请求
          const access_token = response.data.access_token;
          this.token = access_token;
          saveToLocalStorage('authToken', access_token);
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
          
          await this.fetchUser();
          return true;
        } else {
          // 如果没返回token，尝试自动登录
          // 使用手机号或用户名登录
          await this.login({ 
            login: userData.phone || userData.username, 
            password: userData.password 
          });
          return true; // 表示注册并登录成功
        }
      } catch (error) {
        console.error('注册错误:', error.response?.data || error.message);
        throw error; // 将错误向上抛出
      }
    },

    // 4. 获取当前用户信息
    async fetchUser() {
      if (!this.token) {
        return; 
      }
      
      try {
        const headers = {
          'Authorization': `Bearer ${this.token}`
        };
        
        // 获取包含详细信息的用户数据
        const response = await axios.get('/api/me?include_details=true&include_custom_fields=true', { headers }); 
        this.user = response.data;
        saveToLocalStorage('authUser', this.user); // 更新 localStorage 中的用户信息
      } catch (error) {
        if (error.response && error.response.status === 401) {
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
    },

    // 6. 更新用户信息
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
        console.error('更新用户信息错误:', error.response?.data || error.message);
        throw error; // 抛出错误供 UI 处理
      }
    },

    // 7. 修改密码
    async changePassword(passwordData) {
      // passwordData 应包含 { currentPassword, newPassword }
      if (!this.isAuthenticated) return false;
      try {
        // 调用新的后端接口
        await axios.put('/api/me/password', {
          current_password: passwordData.currentPassword,
          new_password: passwordData.newPassword
        });
        return true; // 表示密码修改成功
      } catch (error) {
        console.error('修改密码错误:', error.response?.data || error.message);
        throw error; // 抛出错误供 UI 处理
      }
    },
    
    // 8. 获取用户积分记录
    async fetchPointsRecords(page = 1, perPage = 10) {
      if (!this.isAuthenticated) return null;
      try {
        const response = await axios.get(`/api/points-records?page=${page}&per_page=${perPage}`);
        return response.data;
      } catch (error) {
        console.error('获取积分记录错误:', error.response?.data || error.message);
        throw error;
      }
    },

    // 9. 获取用户优惠券
    async fetchCoupons(page = 1, perPage = 10) {
      if (!this.isAuthenticated) return null;
      try {
        const response = await axios.get(`/api/coupons?page=${page}&per_page=${perPage}`);
        return response.data;
      } catch (error) {
        console.error('获取优惠券错误:', error.response?.data || error.message);
        throw error;
      }
    }
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
        authStore.logout();
      }
    }
    return Promise.reject(error);
  }
); 