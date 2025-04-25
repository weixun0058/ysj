<!-- vue-ysj/src/views/admin/TestEditorView.vue -->
<template>
  <div class="test-editor-container">
    <h1>富文本编辑器测试</h1>
    
    <div class="editor-section">
      <h2>Quill 编辑器测试</h2>
      <div class="quill-wrapper">
        <QuillEditor 
          v-model:content="quillContent" 
          contentType="html" 
          theme="snow"
          toolbar="full"
          :options="{
            placeholder: '请在此输入内容...',
          }"
        />
      </div>
      <div class="preview">
        <h3>编辑器内容预览：</h3>
        <div v-html="quillContent" class="content-preview"></div>
      </div>
    </div>
    
    <div class="action-buttons">
      <button @click="resetContent" class="reset-btn">重置内容</button>
      <button @click="saveContent" class="save-btn">保存内容</button>
    </div>
    
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';

// 初始内容
const defaultContent = '<h2>测试标题</h2><p>这是一个富文本编辑器测试。</p><ul><li>项目 1</li><li>项目 2</li><li>项目 3</li></ul>';
const quillContent = ref(defaultContent);
const message = ref('');
const messageType = ref('');

// 重置内容
const resetContent = () => {
  quillContent.value = defaultContent;
  showMessage('内容已重置', 'success');
};

// 保存内容
const saveContent = () => {
  // 这里只是模拟保存，实际应用中可能需要发送到服务器
  console.log('保存的内容:', quillContent.value);
  
  localStorage.setItem('testEditorContent', quillContent.value);
  showMessage('内容已保存到本地存储', 'success');
};

// 显示消息
const showMessage = (msg, type = 'info') => {
  message.value = msg;
  messageType.value = type;
  
  // 3秒后清除消息
  setTimeout(() => {
    message.value = '';
  }, 3000);
};
</script>

<style scoped>
.test-editor-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: var(--card-background, #ffffff);
  border: 1px solid var(--border-color, #e0e0e0);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1, h2, h3 {
  color: var(--text-color-light, #333333);
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.75rem;
}

h2 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
  border-bottom: 1px solid var(--border-color, #e0e0e0);
  padding-bottom: 0.5rem;
}

.editor-section {
  margin-bottom: 2rem;
}

/* 确保 Quill 编辑器容器有足够高度 */
.quill-wrapper {
  height: 300px;
  margin-bottom: 1.5rem;
}

.preview {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.content-preview {
  min-height: 100px;
  padding: 1rem;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn {
  background-color: #f8f8f8;
  color: #666;
  border: 1px solid #ddd;
}

.save-btn {
  background-color: var(--primary-color, #3498db);
  color: white;
}

.reset-btn:hover {
  background-color: #eee;
}

.save-btn:hover {
  opacity: 0.9;
}

.message {
  margin-top: 1.5rem;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background-color: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
}

.message.error {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.message.info {
  background-color: rgba(52, 152, 219, 0.2);
  color: #3498db;
}
</style> 