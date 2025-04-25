<template>
  <div class="editor-container">
    <div class="toolbar-container" ref="toolbarRef"></div>
    <div class="editor-content" ref="editorRef"></div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'

export default {
  name: 'RichTextEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    mode: {
      type: String,
      default: 'default'
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    // 编辑器实例
    const editorRef = ref(null)
    const toolbarRef = ref(null)
    const editor = ref(null)
    const toolbar = ref(null)

    // 创建编辑器
    const createEditor = () => {
      const editorConfig = {
        placeholder: '请输入内容...',
        onChange: (editorState) => {
          // 当编辑器内容变化时，更新 modelValue
          emit('update:modelValue', editor.value.getHtml())
        }
      }

      // 创建工具栏
      toolbar.value = new Toolbar({
        selector: toolbarRef.value,
        config: { excludeKeys: [] }, // 可以在这里配置要排除的菜单项
        mode: props.mode === 'simple' ? 'simple' : 'default'
      })

      // 创建编辑器
      editor.value = new Editor({
        selector: editorRef.value,
        content: props.modelValue,
        config: editorConfig,
        mode: props.mode === 'simple' ? 'simple' : 'default',
        html: props.modelValue
      })

      // 将工具栏绑定到编辑器
      toolbar.value.bindEditor(editor.value)
    }

    // 监听 modelValue 变化
    watch(() => props.modelValue, (newVal) => {
      if (editor.value && newVal !== editor.value.getHtml()) {
        editor.value.setHtml(newVal)
      }
    })

    // 组件挂载时创建编辑器
    onMounted(() => {
      createEditor()
    })

    // 组件卸载前销毁编辑器
    onBeforeUnmount(() => {
      if (editor.value) {
        editor.value.destroy()
      }
      if (toolbar.value) {
        toolbar.value.destroy()
      }
    })

    return {
      editorRef,
      toolbarRef,
      editor
    }
  }
}
</script>

<style scoped>
.editor-container {
  border: 1px solid var(--border-color, #4a4a4a);
  border-radius: 4px;
  overflow: hidden;
}

.toolbar-container {
  border-bottom: 1px solid var(--border-color, #4a4a4a);
  background-color: var(--input-background, #2a2a2a);
}

.editor-content {
  min-height: 300px;
  max-height: 600px;
  overflow-y: auto;
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-light, #e0e0e0);
}

:deep(.w-e-text-container) {
  background-color: var(--input-background, #2a2a2a) !important;
}

:deep(.w-e-text) {
  color: var(--text-color-light, #e0e0e0) !important;
}

:deep(.w-e-toolbar) {
  background-color: var(--input-background, #2a2a2a) !important;
  border-bottom: 1px solid var(--border-color, #4a4a4a) !important;
}

:deep(.w-e-bar-item) {
  color: var(--text-color-light, #e0e0e0) !important;
}

:deep(.w-e-bar-item svg) {
  fill: var(--text-color-light, #e0e0e0) !important;
}

:deep(.w-e-menu-tooltip) {
  background-color: var(--card-background, #333) !important;
  color: var(--text-color-light, #e0e0e0) !important;
}

:deep(.w-e-modal),
:deep(.w-e-panel) {
  background-color: var(--card-background, #333) !important;
  color: var(--text-color-light, #e0e0e0) !important;
  border-color: var(--border-color, #4a4a4a) !important;
}
</style> 