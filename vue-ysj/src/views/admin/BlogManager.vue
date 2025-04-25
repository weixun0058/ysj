<template>
  <div class="blog-manager">
    <h1 class="page-title">动态资讯管理</h1>

    <div class="blog-actions">
      <button @click="showAddForm = true" class="btn-primary">添加文章</button>
    </div>

    <!-- 文章列表 -->
    <div class="blog-list" v-if="!editMode && !showAddForm">
      <table class="blog-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>分类</th>
            <th>发布日期</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="blog in blogs" :key="blog.id">
            <td>{{ blog.title }}</td>
            <td>{{ getCategoryName(blog.category) }}</td>
            <td>{{ formatDate(blog.published_at) }}</td>
            <td>
              <span :class="['status', blog.published ? 'published' : 'draft']">
                {{ blog.published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td>
              <button @click="editBlog(blog)" class="btn-edit">编辑</button>
              <button @click="confirmDelete(blog)" class="btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页控件 -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
          class="btn-page"
        >
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)"
          class="btn-page"
        >
          下一页
        </button>
      </div>
    </div>

    <!-- 添加/编辑表单 -->
    <div class="blog-form" v-if="editMode || showAddForm">
      <h2>{{ editMode ? '编辑文章' : '添加文章' }}</h2>
      
      <div class="form-group">
        <label for="title">标题</label>
        <input type="text" id="title" v-model="formData.title" required />
      </div>
      
      <div class="form-group">
        <label for="category">分类</label>
        <select id="category" v-model="formData.category" required>
          <option value="">-- 请选择分类 --</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="summary">摘要</label>
        <textarea id="summary" v-model="formData.summary" rows="3"></textarea>
      </div>
      
      <div class="form-group">
        <label for="cover_image">封面图片</label>
        <input type="file" id="cover_image" @change="handleImageUpload" accept="image/*" />
        <div v-if="formData.cover_image" class="image-preview">
          <img :src="formData.cover_image" alt="封面预览" />
        </div>
      </div>
      
      <div class="form-group">
        <label>内容</label>
        <RichTextEditor v-model="formData.content" />
      </div>
      
      <div class="form-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.published" />
          立即发布
        </label>
      </div>
      
      <div class="form-actions">
        <button @click="saveBlog" class="btn-primary">保存</button>
        <button @click="cancelEdit" class="btn-cancel">取消</button>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div class="delete-modal" v-if="showDeleteModal">
      <div class="modal-content">
        <h3>确认删除</h3>
        <p>确定要删除文章"{{ blogToDelete.title }}"吗？此操作不可撤销。</p>
        <div class="modal-actions">
          <button @click="deleteBlog" class="btn-confirm">确认删除</button>
          <button @click="showDeleteModal = false" class="btn-cancel">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import RichTextEditor from '@/components/admin/RichTextEditor.vue'
import axios from 'axios'

export default {
  components: {
    RichTextEditor
  },
  setup() {
    const blogs = ref([])
    const categories = ref([
      { id: 'company', name: '公司动态' },
      { id: 'industry', name: '行业知识' },
      { id: 'origin', name: '产地风采' },
      { id: 'health', name: '健康生活' }
    ])
    
    const formData = reactive({
      id: null,
      title: '',
      category: '',
      summary: '',
      content: '',
      cover_image: '',
      published: false,
      published_at: null
    })
    
    const editMode = ref(false)
    const showAddForm = ref(false)
    const showDeleteModal = ref(false)
    const blogToDelete = ref({})
    
    const currentPage = ref(1)
    const itemsPerPage = 10
    const totalItems = ref(0)
    
    const totalPages = computed(() => {
      return Math.ceil(totalItems.value / itemsPerPage)
    })
    
    const loadBlogs = async (page = 1) => {
      try {
        const response = await axios.get('/api/blogs', {
          params: {
            page,
            per_page: itemsPerPage
          }
        })
        blogs.value = response.data.items
        totalItems.value = response.data.total
        currentPage.value = page
      } catch (error) {
        console.error('加载文章失败:', error)
        // 这里可以添加错误提示
      }
    }
    
    const resetForm = () => {
      formData.id = null
      formData.title = ''
      formData.category = ''
      formData.summary = ''
      formData.content = ''
      formData.cover_image = ''
      formData.published = false
      formData.published_at = null
    }
    
    const editBlog = (blog) => {
      editMode.value = true
      showAddForm.value = false
      formData.id = blog.id
      formData.title = blog.title
      formData.category = blog.category
      formData.summary = blog.summary
      formData.content = blog.content
      formData.cover_image = blog.cover_image
      formData.published = blog.published
      formData.published_at = blog.published_at
    }
    
    const cancelEdit = () => {
      editMode.value = false
      showAddForm.value = false
      resetForm()
    }
    
    const saveBlog = async () => {
      try {
        if (!formData.title || !formData.category || !formData.content) {
          alert('请填写标题、分类和内容')
          return
        }
        
        const data = { ...formData }
        
        if (formData.published && !formData.published_at) {
          data.published_at = new Date().toISOString()
        }
        
        if (editMode.value) {
          await axios.put(`/api/blogs/${formData.id}`, data)
        } else {
          await axios.post('/api/blogs', data)
        }
        
        editMode.value = false
        showAddForm.value = false
        resetForm()
        loadBlogs(currentPage.value)
      } catch (error) {
        console.error('保存文章失败:', error)
        // 这里可以添加错误提示
      }
    }
    
    const confirmDelete = (blog) => {
      blogToDelete.value = blog
      showDeleteModal.value = true
    }
    
    const deleteBlog = async () => {
      try {
        await axios.delete(`/api/blogs/${blogToDelete.value.id}`)
        showDeleteModal.value = false
        loadBlogs(currentPage.value)
      } catch (error) {
        console.error('删除文章失败:', error)
        // 这里可以添加错误提示
      }
    }
    
    const changePage = (page) => {
      loadBlogs(page)
    }
    
    const handleImageUpload = async (event) => {
      const file = event.target.files[0]
      if (!file) return
      
      const formData = new FormData()
      formData.append('file', file)
      
      try {
        const response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        formData.cover_image = response.data.url
      } catch (error) {
        console.error('上传图片失败:', error)
        // 这里可以添加错误提示
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }
    
    const getCategoryName = (categoryId) => {
      const category = categories.value.find(c => c.id === categoryId)
      return category ? category.name : '-'
    }
    
    onMounted(() => {
      loadBlogs()
    })
    
    return {
      blogs,
      categories,
      formData,
      editMode,
      showAddForm,
      showDeleteModal,
      blogToDelete,
      currentPage,
      totalPages,
      editBlog,
      cancelEdit,
      saveBlog,
      confirmDelete,
      deleteBlog,
      changePage,
      handleImageUpload,
      formatDate,
      getCategoryName
    }
  }
}
</script>

<style scoped>
.blog-manager {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.blog-actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #40a9ff;
}

.blog-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.blog-table th,
.blog-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.blog-table th {
  background-color: #f7f7f7;
  font-weight: bold;
}

.btn-edit,
.btn-delete {
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-edit {
  background-color: #52c41a;
  color: white;
}

.btn-delete {
  background-color: #ff4d4f;
  color: white;
}

.btn-edit:hover {
  background-color: #73d13d;
}

.btn-delete:hover {
  background-color: #ff7875;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.published {
  background-color: #e6f7ff;
  color: #1890ff;
}

.draft {
  background-color: #f9f9f9;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.btn-page {
  background-color: white;
  border: 1px solid #d9d9d9;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-page:hover:not(:disabled) {
  border-color: #1890ff;
  color: #1890ff;
}

.btn-page:disabled {
  cursor: not-allowed;
  color: #d9d9d9;
}

.page-info {
  margin: 0 10px;
}

.blog-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: normal;
}

.checkbox-label input {
  margin-right: 8px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.btn-cancel {
  background-color: white;
  border: 1px solid #d9d9d9;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.image-preview {
  margin-top: 10px;
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  border-radius: 4px;
}

.delete-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  max-width: 400px;
  width: 100%;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-confirm {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-confirm:hover {
  background-color: #ff7875;
}
</style> 