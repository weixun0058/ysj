<template>
  <div class="quill-editor-container">
    <div class="quill-editor">
      <QuillEditor
        v-model:content="editorContent"
        contentType="html"
        :toolbar="toolbar"
        theme="snow"
        :options="options"
        style="height: 300px"
        @update:content="updateContent"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '请输入内容...'
  },
  height: {
    type: String,
    default: '300px'
  }
});

const emit = defineEmits(['update:modelValue']);

// 编辑器内容
const editorContent = ref(props.modelValue || '');

// 编辑器工具栏配置
const toolbar = [
  ['bold', 'italic', 'underline', 'strike'],
  ['blockquote', 'code-block'],
  [{ 'header': 1 }, { 'header': 2 }],
  [{ 'list': 'ordered' }, { 'list': 'bullet' }],
  [{ 'script': 'sub' }, { 'script': 'super' }],
  [{ 'indent': '-1' }, { 'indent': '+1' }],
  [{ 'direction': 'rtl' }],
  [{ 'size': ['small', false, 'large', 'huge'] }],
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  [{ 'color': [] }, { 'background': [] }],
  [{ 'font': [] }],
  [{ 'align': [] }],
  ['clean'],
  ['link', 'image']
];

// 编辑器选项
const options = {
  placeholder: props.placeholder,
  modules: {
    // 可以添加更多模块配置
  }
};

// 当内容变化时触发父组件的更新
const updateContent = (content) => {
  // 确保内容不是undefined或null
  const safeContent = content || '';
  emit('update:modelValue', safeContent);
};

// 监听父组件传入的值变化
watch(() => props.modelValue, (newValue) => {
  if (newValue !== undefined && newValue !== editorContent.value) {
    editorContent.value = newValue;
  }
}, { immediate: true });

// 组件挂载时处理初始值
onMounted(() => {
  // 如果初始值存在但编辑器内容为空，设置编辑器内容
  if (props.modelValue && !editorContent.value) {
    editorContent.value = props.modelValue;
  }
  
  // 添加额外的DOM事件监听，确保编辑器正常工作
  const editorElement = document.querySelector('.quill-editor .ql-editor');
  if (editorElement) {
    // 确保编辑器在点击后获得焦点
    editorElement.addEventListener('click', () => {
      editorElement.focus();
    });
  }
});
</script>

<style scoped>
.quill-editor-container {
  width: 100%;
  margin-bottom: 1rem;
}

:deep(.ql-editor) {
  min-height: v-bind('props.height');
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-color-light, #e0e0e0);
  background-color: var(--input-background, #2a2a2a);
}

:deep(.ql-container),
:deep(.ql-toolbar) {
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light, #e0e0e0);
  border-color: var(--border-color, #4a4a4a) !important;
}

:deep(.ql-toolbar .ql-stroke) {
  stroke: var(--text-color-light, #e0e0e0);
}

:deep(.ql-toolbar .ql-fill) {
  fill: var(--text-color-light, #e0e0e0);
}

:deep(.ql-toolbar .ql-picker) {
  color: var(--text-color-light, #e0e0e0);
}

:deep(.ql-toolbar .ql-picker-options) {
  background-color: var(--input-background, #2a2a2a);
  border-color: var(--border-color, #4a4a4a);
}

:deep(.ql-toolbar .ql-picker-label) {
  color: var(--text-color-light, #e0e0e0);
}

:deep(.ql-editor.ql-blank::before) {
  color: var(--text-color-medium, #999);
  opacity: 0.6;
}

:deep(.ql-snow .ql-picker-options .ql-picker-item) {
  color: var(--text-color-light, #e0e0e0);
}

:deep(.ql-tooltip) {
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light, #e0e0e0);
  border-color: var(--border-color, #4a4a4a);
}

:deep(.ql-tooltip input[type=text]) {
  background-color: #333;
  color: #e0e0e0;
  border: 1px solid #555;
}
</style> 