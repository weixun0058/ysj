import axios from 'axios';

// 获取认证token的辅助函数
const getAuthHeader = () => {
  console.log('[getAuthHeader] Attempting to read authToken from localStorage.');
  const token = localStorage.getItem('authToken');
  const parsedToken = token ? JSON.parse(token) : null;
  console.log('[getAuthHeader] Raw token from localStorage:', token);
  console.log('[getAuthHeader] Parsed token:', parsedToken ? parsedToken.substring(0, 15) + '...' : 'null');
  
  if (!parsedToken) {
      console.warn('[getAuthHeader] No valid token found in localStorage.');
  }
  
  return parsedToken ? { Authorization: `Bearer ${parsedToken}` } : {};
};

// 公开API - 获取文章列表(分页)
export const getNewsList = async (page = 1, perPage = 10) => {
  try {
    const response = await axios.get('/api/news', {
      params: { page, per_page: perPage }
    });
    return response.data;
  } catch (error) {
    console.error('获取文章列表失败:', error);
    throw error;
  }
};

// 公开API - 获取单篇文章详情
export const getNewsDetail = async (slug) => {
  try {
    const response = await axios.get(`/api/news/${slug}`);
    return response.data;
  } catch (error) {
    console.error('获取文章详情失败:', error);
    throw error;
  }
};

// 管理员API - 获取所有文章(包括草稿)
export const getAdminNewsList = async (page = 1, perPage = 10, search = '') => {
  try {
    const response = await axios.get('/api/admin/news', {
      params: { page, per_page: perPage, search },
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('获取管理员文章列表失败:', error);
    throw error;
  }
};

// 管理员API - 获取单篇文章详情(管理员视角)
export const getAdminNewsDetail = async (articleId) => {
  try {
    const response = await axios.get(`/api/admin/news/${articleId}`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('获取管理员文章详情失败:', error);
    throw error;
  }
};

// 管理员API - 创建新文章
export const createNews = async (articleData) => {
  try {
    const response = await axios.post('/api/admin/news', articleData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('创建文章失败:', error);
    throw error;
  }
};

// 管理员API - 更新文章
export const updateNews = async (articleId, articleData) => {
  try {
    const response = await axios.put(`/api/admin/news/${articleId}`, articleData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('更新文章失败:', error);
    throw error;
  }
};

// 管理员API - 删除文章
export const deleteNews = async (articleId) => {
  try {
    const response = await axios.delete(`/api/admin/news/${articleId}`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('删除文章失败:', error);
    throw error;
  }
};

// 管理员API - 切换文章发布状态
export const toggleNewsPublishStatus = async (articleId) => {
  try {
    const response = await axios.put(`/api/admin/news/${articleId}/toggle-publish`, {}, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('切换文章发布状态失败:', error);
    throw error;
  }
}; 