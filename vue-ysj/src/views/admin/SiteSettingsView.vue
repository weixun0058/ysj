<template>
  <div class="site-settings-container">
    <h1 class="page-title">网站设置</h1>
    
    <div v-if="loading" class="loading-spinner">
      <font-awesome-icon icon="spinner" spin />
      <span>加载中...</span>
    </div>
    
    <form v-else @submit.prevent="saveSettings" class="settings-form">
      <!-- 基本设置 -->
      <div class="form-section">
        <h2>基本设置</h2>
        
        <div class="form-group">
          <label for="siteName">网站名称</label>
          <input 
            type="text"
            id="siteName"
            v-model="settings.siteName"
            class="form-control"
            required
          />
        </div>
        
        <!-- Logo上传 -->
        <div class="form-group">
          <label>网站Logo</label>
          <div class="logo-preview-container">
            <img 
              v-if="settings.logo" 
              :src="settings.logo" 
              alt="网站Logo" 
              class="logo-preview"
            />
            <div v-else class="no-logo">暂无Logo</div>
          </div>
          
          <div class="logo-upload">
            <input 
              type="file" 
              id="logoFile" 
              ref="logoInput"
              @change="handleLogoChange" 
              accept=".jpg,.jpeg,.png,.gif,.svg"
              class="file-input"
            />
            <label for="logoFile" class="custom-file-upload">
              <font-awesome-icon icon="upload" /> 选择Logo文件
            </label>
            <button 
              v-if="logoFile" 
              type="button" 
              @click="uploadLogo" 
              class="upload-btn"
              :disabled="uploadingLogo"
            >
              <font-awesome-icon v-if="uploadingLogo" icon="spinner" spin />
              {{ uploadingLogo ? '上传中...' : '上传Logo' }}
            </button>
          </div>
          <div class="logo-help">
            建议尺寸: 200x50像素，最大文件大小: 5MB，支持的格式: PNG, JPG, JPEG, GIF, SVG
          </div>
        </div>
      </div>
      
      <!-- 联系信息 -->
      <div class="form-section">
        <h2>联系信息</h2>
        
        <div class="form-group">
          <label for="contactEmail">联系邮箱</label>
          <input 
            type="email"
            id="contactEmail"
            v-model="settings.contactEmail"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="contactPhone">联系电话</label>
          <input 
            type="text"
            id="contactPhone"
            v-model="settings.contactPhone"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="address">地址</label>
          <textarea 
            id="address"
            v-model="settings.address"
            class="form-control"
            rows="3"
          ></textarea>
        </div>
      </div>
      
      <!-- 社交媒体 -->
      <div class="form-section">
        <h2>社交媒体</h2>
        
        <div class="form-group">
          <label for="weixin">微信公众号</label>
          <input 
            type="text"
            id="weixin"
            v-model="settings.socialMedia.weixin"
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="weibo">微博</label>
          <input 
            type="text"
            id="weibo"
            v-model="settings.socialMedia.weibo"
            class="form-control"
          />
        </div>
      </div>
      
      <!-- 页脚文本 -->
      <div class="form-section">
        <h2>页脚设置</h2>
        
        <div class="form-group">
          <label for="footerText">页脚文本</label>
          <textarea 
            id="footerText"
            v-model="settings.footerText"
            class="form-control"
            rows="3"
          ></textarea>
        </div>
      </div>
      
      <!-- 保存按钮 -->
      <div class="form-actions">
        <button 
          type="submit" 
          class="save-btn" 
          :disabled="saving"
        >
          <font-awesome-icon v-if="saving" icon="spinner" spin />
          {{ saving ? '保存中...' : '保存设置' }}
        </button>
      </div>
    </form>
    
    <!-- 提示消息 -->
    <div v-if="message" class="message" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { getSiteSettings, updateSiteSettings, uploadLogo as uploadLogoApi } from '../../api/settingsApi';

export default {
  name: 'SiteSettingsView',
  
  setup() {
    // 状态
    const loading = ref(true);
    const saving = ref(false);
    const uploadingLogo = ref(false);
    const message = ref('');
    const messageType = ref('');
    const logoInput = ref(null);
    const logoFile = ref(null);
    
    // 设置数据
    const settings = reactive({
      siteName: '',
      logo: '',
      contactEmail: '',
      contactPhone: '',
      address: '',
      socialMedia: {
        weixin: '',
        weibo: ''
      },
      footerText: ''
    });
    
    // 加载设置数据
    const loadSettings = async () => {
      try {
        loading.value = true;
        console.log('正在获取网站设置...');
        const data = await getSiteSettings();
        console.log('获取到的设置数据:', data);
        
        // 更新reactive对象
        Object.assign(settings, data);
        
        // 确保社交媒体对象存在
        if (!settings.socialMedia) {
          settings.socialMedia = {
            weixin: '',
            weibo: ''
          };
        }
        
      } catch (error) {
        console.error('加载设置详细错误:', error);
        showMessage('加载设置失败: ' + (error.response?.data?.error || error.message), 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // 保存设置
    const saveSettings = async () => {
      try {
        saving.value = true;
        await updateSiteSettings(settings);
        showMessage('设置已成功保存', 'success');
      } catch (error) {
        showMessage('保存设置失败: ' + (error.response?.data?.error || error.message), 'error');
      } finally {
        saving.value = false;
      }
    };
    
    // 处理Logo文件选择
    const handleLogoChange = (event) => {
      const files = event.target.files;
      if (files.length > 0) {
        logoFile.value = files[0];
      } else {
        logoFile.value = null;
      }
    };
    
    // 上传Logo
    const uploadLogo = async () => {
      if (!logoFile.value) return;
      
      try {
        uploadingLogo.value = true;
        const result = await uploadLogoApi(logoFile.value);
        
        // 更新Logo URL
        settings.logo = result.logo_url;
        
        // 清空文件选择
        logoFile.value = null;
        if (logoInput.value) {
          logoInput.value.value = '';
        }
        
        showMessage('Logo上传成功', 'success');
      } catch (error) {
        showMessage('上传Logo失败: ' + (error.response?.data?.error || error.message), 'error');
      } finally {
        uploadingLogo.value = false;
      }
    };
    
    // 显示消息
    const showMessage = (text, type) => {
      message.value = text;
      messageType.value = type;
      
      // 3秒后清除消息
      setTimeout(() => {
        message.value = '';
      }, 3000);
    };
    
    // 组件挂载时加载设置
    onMounted(() => {
      loadSettings();
    });
    
    return {
      settings,
      loading,
      saving,
      message,
      messageType,
      saveSettings,
      logoInput,
      logoFile,
      handleLogoChange,
      uploadLogo,
      uploadingLogo
    };
  }
};
</script>

<style scoped>
.site-settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  font-size: 18px;
  color: #666;
}

.loading-spinner span {
  margin-left: 10px;
}

.settings-form {
  background: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.form-section h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #555;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #444;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

textarea.form-control {
  resize: vertical;
}

.form-actions {
  padding: 20px;
  text-align: right;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background-color: #45a049;
}

.save-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.logo-preview-container {
  margin-bottom: 10px;
  border: 1px dashed #ccc;
  padding: 10px;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100px;
}

.logo-preview {
  max-width: 100%;
  max-height: 100px;
}

.no-logo {
  color: #999;
  font-style: italic;
}

.logo-upload {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-input {
  display: none;
}

.custom-file-upload {
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
  background: #f8f8f8;
  border-radius: 4px;
  margin-right: 10px;
}

.upload-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.upload-btn:disabled {
  background-color: #cccccc;
}

.logo-help {
  font-size: 12px;
  color: #777;
  margin-top: 5px;
}

.message {
  margin-top: 20px;
  padding: 10px 15px;
  border-radius: 4px;
  font-weight: 500;
}

.message.success {
  background-color: #dff0d8;
  color: #3c763d;
  border: 1px solid #d6e9c6;
}

.message.error {
  background-color: #f2dede;
  color: #a94442;
  border: 1px solid #ebccd1;
}
</style> 