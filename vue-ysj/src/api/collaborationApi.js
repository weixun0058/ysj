import axios from 'axios';
import { API_BASE_URL } from './config';

/**
 * 品牌联名合作API模块
 */

/**
 * 提交品牌合作意向申请
 * @param {Object} data - 合作申请数据
 * @returns {Promise} - 返回API响应
 */
export const submitCollaborationRequest = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/collaboration/request`, data);
    return response.data;
  } catch (error) {
    console.error('提交合作意向失败:', error);
    throw error;
  }
};

/**
 * 获取行业类型列表
 * @returns {Promise} - 返回行业类型列表
 */
export const getIndustryTypes = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/collaboration/industry-types`);
    return response.data;
  } catch (error) {
    console.error('获取行业类型失败:', error);
    return null;
  }
};

/**
 * 获取合作类型列表
 * @returns {Promise} - 返回合作类型列表
 */
export const getCollaborationTypes = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/collaboration/types`);
    return response.data;
  } catch (error) {
    console.error('获取合作类型失败:', error);
    return null;
  }
};

/**
 * 获取往期合作案例列表
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回合作案例列表
 */
export const getCollaborationCases = async (params = {}) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/collaboration/cases`, { params });
    return response.data;
  } catch (error) {
    console.error('获取合作案例失败:', error);
    return null;
  }
};

/**
 * 获取合作案例详情
 * @param {string|number} caseId - 案例ID
 * @returns {Promise} - 返回案例详情
 */
export const getCollaborationCaseDetail = async (caseId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/collaboration/cases/${caseId}`);
    return response.data;
  } catch (error) {
    console.error('获取案例详情失败:', error);
    return null;
  }
};

/**
 * 获取合作申请状态（如果需要查询已提交申请的状态）
 * @param {string} requestId - 申请ID
 * @returns {Promise} - 请求结果的Promise
 */
export const getCollaborationStatus = async (requestId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/collaboration/status/${requestId}`);
    return response.data;
  } catch (error) {
    console.error('获取合作申请状态时出错:', error);
    throw error;
  }
};

export default {
  submitCollaborationRequest,
  getCollaborationStatus,
  getCollaborationCases,
  getCollaborationTypes,
  getIndustryTypes,
  getCollaborationCaseDetail
}; 