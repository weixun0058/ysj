/**
 * API配置文件
 * 包含API相关的全局配置
 */

// API基础URL，根据环境变量获取或使用默认值
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

// API请求超时时间（毫秒）
export const API_TIMEOUT = 15000;

// API版本
export const API_VERSION = 'v1';

// 是否启用请求日志
export const ENABLE_API_LOGGING = import.meta.env.MODE !== 'production';

// 默认请求头
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// 导出默认配置对象
export default {
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  version: API_VERSION,
  enableLogging: ENABLE_API_LOGGING,
  headers: DEFAULT_HEADERS
}; 