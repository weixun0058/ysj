import axios from 'axios';

// 测试API连通性
async function testSettingsAPI() {
  try {
    console.log('测试获取设置API');
    const response = await axios.get('http://localhost:5000/api/settings');
    console.log('API响应:', response.data);
    return response.data;
  } catch (error) {
    console.error('API请求失败:', error.message);
    if (error.response) {
      console.error('错误状态码:', error.response.status);
      console.error('错误数据:', error.response.data);
    }
    throw error;
  }
}

// 执行测试
testSettingsAPI()
  .then(data => {
    console.log('测试成功!');
  })
  .catch(error => {
    console.error('测试失败!');
  }); 