import axios from 'axios';

/**
 * 获取网站设置
 * @returns {Promise<Object>} 包含网站设置的对象
 */
export async function getSiteSettings() {
  try {
    const response = await axios.get('/api/settings');
    // 后端直接返回设置对象
    return response.data;
  } catch (error) {
    console.error('获取网站设置失败:', error);
    throw error;
  }
}

/**
 * 更新网站设置
 * @param {Object} settings - 要更新的设置
 * @returns {Promise<Object>} 更新结果
 */
export async function updateSiteSettings(settings) {
  try {
    const response = await axios.put('/api/settings', settings);
    // 返回更新后的设置对象
    return response.data.settings || response.data;
  } catch (error) {
    console.error('更新网站设置失败:', error);
    throw error;
  }
}

/**
 * 上传网站logo
 * @param {File} file - 要上传的logo文件
 * @returns {Promise<Object>} 上传结果，包含logo URL
 */
export async function uploadLogo(file) {
  try {
    const formData = new FormData();
    formData.append('logo', file);
    
    const response = await axios.post('/api/settings/logo', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // 返回logo的URL
    return {logo_url: response.data.logo_url};
  } catch (error) {
    console.error('上传Logo失败:', error);
    throw error;
  }
} 