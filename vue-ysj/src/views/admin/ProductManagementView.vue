<template>
  <div class="product-management">
    <!-- 产品列表 -->
    <div class="product-list-section">
      <div class="section-header">
        <h2>产品列表</h2>
        <button @click="showAddProductForm = true" class="btn-primary">
          <i class="fas fa-plus"></i> 添加新产品
        </button>
      </div>
      
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <div v-else-if="products.length === 0" class="empty-state">
        暂无产品，请添加新产品。
      </div>
      <div v-else class="product-table-container">
        <table class="product-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>图片</th>
              <th>名称</th>
              <th>价格</th>
              <th>分类</th>
              <th>总库存</th>
              <th>可用库存</th>
              <th>预警阈值</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.id }}</td>
              <td class="product-image-cell">
                <img 
                  v-if="product.images && product.images.length" 
                  :src="getImageUrl(product.images[0])" 
                  :alt="product.name"
                  @error="handleImgError($event)"
                />
                <div v-else class="no-image">无图片</div>
              </td>
              <td>{{ product.name }}</td>
              <td>¥{{ product.price }}</td>
              <td>{{ product.category || '无分类' }}</td>
              <td>{{ product.total_stock || 0 }}</td>
              <td>
                <span :class="{'stock-warning': product.available_stock <= product.warning_stock}">
                  {{ product.available_stock || 0 }}
                </span>
              </td>
              <td>{{ product.warning_stock || 10 }}</td>
              <td class="actions-cell">
                <button @click="editProduct(product)" class="btn-edit">
                  <i class="fas fa-edit"></i> 编辑
                </button>
                <button @click="adjustStock(product)" class="btn-adjust-stock">
                  <i class="fas fa-boxes"></i> 调整库存
                </button>
                <button @click="confirmDelete(product)" class="btn-delete">
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 添加产品表单 (对话框) -->
    <div v-if="showAddProductForm" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加新产品</h3>
          <button @click="showAddProductForm = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="addProduct" class="product-form">
          <div class="form-group">
            <label for="name">产品名称 <span class="required">*</span></label>
            <input 
              id="name"
              v-model="newProduct.name"
              type="text"
              required
              placeholder="请输入产品名称"
            >
          </div>
          
          <div class="form-group">
            <label for="description">产品描述</label>
            <textarea
              id="description"
              v-model="newProduct.description"
              rows="3"
              placeholder="请输入产品描述"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="price">价格 (元) <span class="required">*</span></label>
            <input 
              id="price"
              v-model.number="newProduct.price"
              type="number"
              step="0.01"
              min="0"
              required
              placeholder="请输入价格"
            >
          </div>
          
          <div class="form-group">
            <label for="category">分类</label>
            <input 
              id="category"
              v-model="newProduct.category"
              type="text"
              placeholder="请输入分类"
            >
          </div>
          
          <div class="form-group">
            <label for="total_stock">初始总库存</label>
            <input 
              id="total_stock"
              v-model.number="newProduct.total_stock"
              type="number"
              min="0"
              placeholder="请输入初始库存数量"
            >
          </div>
          
          <div class="form-group">
            <label for="warning_stock">库存预警阈值</label>
            <input 
              id="warning_stock"
              v-model.number="newProduct.warning_stock"
              type="number"
              min="0"
              placeholder="库存低于此值时提醒"
            >
            <small class="form-hint">当可用库存低于此值时将显示预警</small>
          </div>
          
          <div class="form-group">
            <label for="images">产品图片</label>
            <input 
              id="images"
              type="file"
              multiple
              @change="handleFileUpload"
              accept="image/*"
            >
            <div class="upload-preview" v-if="imagePreviewUrls.length">
              <div v-for="(url, index) in imagePreviewUrls" :key="index" class="preview-item">
                <img :src="url" alt="预览图片">
                <button type="button" @click="removeImage(index)" class="remove-image">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showAddProductForm = false" class="btn-cancel">
              取消
            </button>
            <button type="submit" class="btn-submit" :disabled="isSubmitting">
              <span v-if="isSubmitting">提交中...</span>
              <span v-else>提交</span>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 编辑产品表单 (对话框) -->
    <div v-if="showEditProductForm" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑产品</h3>
          <button @click="showEditProductForm = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="updateProduct" class="product-form">
          <div class="form-group">
            <label for="edit-name">产品名称 <span class="required">*</span></label>
            <input 
              id="edit-name"
              v-model="editingProduct.name"
              type="text"
              required
              placeholder="请输入产品名称"
            >
          </div>
          
          <div class="form-group">
            <label for="edit-description">产品描述</label>
            <textarea
              id="edit-description"
              v-model="editingProduct.description"
              rows="3"
              placeholder="请输入产品描述"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="edit-price">价格 (元) <span class="required">*</span></label>
            <input 
              id="edit-price"
              v-model.number="editingProduct.price"
              type="number"
              step="0.01"
              min="0"
              required
              placeholder="请输入价格"
            >
          </div>
          
          <div class="form-group">
            <label for="edit-category">分类</label>
            <input 
              id="edit-category"
              v-model="editingProduct.category"
              type="text"
              placeholder="请输入分类"
            >
          </div>
          
          <div class="form-group">
            <label for="edit-total-stock">总库存</label>
            <input 
              id="edit-total-stock"
              v-model.number="editingProduct.total_stock"
              type="number"
              min="0"
              placeholder="请输入总库存数量"
            >
          </div>
          
          <div class="form-group stock-info">
            <div>
              <label>可用库存</label>
              <div class="stock-value" :class="{'stock-warning': editingProduct.available_stock <= editingProduct.warning_stock}">
                {{ editingProduct.available_stock || 0 }}
              </div>
              <small class="form-hint">由系统自动计算，不可直接修改</small>
            </div>
            
            <div>
              <label>预扣库存</label>
              <div class="stock-value">{{ editingProduct.prelock_stock || 0 }}</div>
              <small class="form-hint">已下单未支付的库存量</small>
            </div>
          </div>
          
          <div class="form-group">
            <label for="edit-warning-stock">库存预警阈值</label>
            <input 
              id="edit-warning-stock"
              v-model.number="editingProduct.warning_stock"
              type="number"
              min="0"
              placeholder="库存低于此值时提醒"
            >
            <small class="form-hint">当可用库存低于此值时将显示预警</small>
          </div>
          
          <div class="form-group">
            <label>当前图片</label>
            <div class="current-images" v-if="editingProduct.images && editingProduct.images.length">
              <div v-for="(img, index) in editingProduct.images" :key="index" class="current-image-item">
                <img :src="getImageUrl(img)" :alt="`产品图片 ${index + 1}`" @error="handleImgError($event)">
              </div>
            </div>
            <p v-else>暂无图片</p>
          </div>
          
          <div class="form-group">
            <label for="edit-images">添加新图片</label>
            <input 
              id="edit-images"
              type="file"
              multiple
              @change="handleEditFileUpload"
              accept="image/*"
            >
            <div class="upload-preview" v-if="editImagePreviewUrls.length">
              <div v-for="(url, index) in editImagePreviewUrls" :key="index" class="preview-item">
                <img :src="url" alt="预览图片">
                <button type="button" @click="removeEditImage(index)" class="remove-image">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showEditProductForm = false" class="btn-cancel">
              取消
            </button>
            <button type="submit" class="btn-submit" :disabled="isSubmitting">
              <span v-if="isSubmitting">提交中...</span>
              <span v-else>保存修改</span>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 确认删除对话框 -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal-container delete-confirm-modal">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button @click="showDeleteConfirm = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-content">
          <p>确定要删除产品 "{{ productToDelete.name }}" 吗？</p>
          <p class="warning">此操作无法撤销！</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteConfirm = false" class="btn-cancel">
            取消
          </button>
          <button @click="deleteProduct" class="btn-delete" :disabled="isSubmitting">
            <span v-if="isSubmitting">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 新增: 库存调整对话框 -->
    <div v-if="showStockAdjustForm" class="modal-overlay">
      <div class="modal-container stock-adjust-modal">
        <div class="modal-header">
          <h3>调整库存 - {{ stockAdjustProduct.name }}</h3>
          <button @click="showStockAdjustForm = false" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="submitStockAdjust" class="product-form">
          <div class="form-group stock-info">
            <div>
              <label>当前总库存</label>
              <div class="stock-value">{{ stockAdjustProduct.total_stock || 0 }}</div>
            </div>
            
            <div>
              <label>当前可用库存</label>
              <div class="stock-value" :class="{'stock-warning': stockAdjustProduct.available_stock <= stockAdjustProduct.warning_stock}">
                {{ stockAdjustProduct.available_stock || 0 }}
              </div>
            </div>
            
            <div>
              <label>当前预扣库存</label>
              <div class="stock-value">{{ stockAdjustProduct.prelock_stock || 0 }}</div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="adjust-total-stock">调整后总库存 <span class="required">*</span></label>
            <input 
              id="adjust-total-stock"
              v-model.number="stockAdjustForm.newTotalStock"
              type="number"
              :min="stockAdjustProduct.prelock_stock || 0"
              required
              placeholder="请输入调整后的总库存"
            >
            <small class="form-hint">总库存不能小于当前预扣库存 ({{ stockAdjustProduct.prelock_stock || 0 }})</small>
          </div>
          
          <div class="form-group">
            <label for="adjust-reason">调整原因 <span class="required">*</span></label>
            <textarea
              id="adjust-reason"
              v-model="stockAdjustForm.reason"
              rows="3"
              required
              placeholder="请输入库存调整原因，如：采购入库、库存盘点、质量问题等"
            ></textarea>
          </div>
          
          <div class="stock-change-preview" v-if="stockChangeAmount !== 0">
            <div class="change-arrow" :class="{'increase': stockChangeAmount > 0, 'decrease': stockChangeAmount < 0}">
              {{ stockChangeAmount > 0 ? '↑' : '↓' }}
            </div>
            <div class="change-text">
              库存将{{ stockChangeAmount > 0 ? '增加' : '减少' }} <span class="change-amount">{{ Math.abs(stockChangeAmount) }}</span> 件
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showStockAdjustForm = false" class="btn-cancel">
              取消
            </button>
            <button type="submit" class="btn-submit" :disabled="isSubmitting || !isStockAdjustValid">
              <span v-if="isSubmitting">提交中...</span>
              <span v-else>确认调整</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';

// 状态变量
const products = ref([]);
const loading = ref(true);
const error = ref(null);
const showAddProductForm = ref(false);
const showEditProductForm = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const imagePreviewUrls = ref([]);
const editImagePreviewUrls = ref([]);
const uploadedFiles = ref([]);
const editUploadedFiles = ref([]);
const productToDelete = ref({});

// 新增: 库存调整相关状态
const showStockAdjustForm = ref(false);
const stockAdjustProduct = reactive({
  id: null,
  name: '',
  total_stock: 0,
  available_stock: 0,
  prelock_stock: 0,
  warning_stock: 10
});

const stockAdjustForm = reactive({
  newTotalStock: 0,
  reason: ''
});

// 库存变化量计算
const stockChangeAmount = computed(() => {
  return stockAdjustForm.newTotalStock - stockAdjustProduct.total_stock;
});

// 库存调整表单验证
const isStockAdjustValid = computed(() => {
  return (
    stockAdjustForm.newTotalStock >= (stockAdjustProduct.prelock_stock || 0) &&
    stockAdjustForm.reason.trim().length > 0
  );
});

// 新产品表单数据
const newProduct = reactive({
  name: '',
  description: '',
  price: '',
  category: '',
  total_stock: 0,       // 新增：初始库存
  warning_stock: 10     // 新增：预警阈值，默认10
});

// 编辑产品表单数据
const editingProduct = reactive({
  id: null,
  name: '',
  description: '',
  price: '',
  category: '',
  images: [],
  total_stock: 0,       // 新增：总库存
  available_stock: 0,   // 新增：可用库存 (展示用，不可直接修改)
  prelock_stock: 0,     // 新增：预扣库存 (展示用，不可直接修改)
  warning_stock: 10     // 新增：预警阈值
});

// 后端API地址
const backendBase = 'http://localhost:5000';

// 获取图片完整URL
const getImageUrl = (path) => {
  if (!path) return '/img/placeholder.png';
  return path.startsWith('http') ? path : `${backendBase}${path}`;
};

// 图片加载失败处理
const handleImgError = (e) => {
  e.target.src = '/img/placeholder.png';
};

// 加载产品列表
const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch('/api/products');
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    
    const data = await response.json();
    products.value = data.products || [];
  } catch (err) {
    console.error('获取产品列表失败:', err);
    error.value = '获取产品列表失败，请刷新页面重试';
  } finally {
    loading.value = false;
  }
};

// 处理新增产品中的文件上传
const handleFileUpload = (event) => {
  const files = event.target.files;
  if (!files.length) return;
  
  // 保存文件对象以便后续提交
  uploadedFiles.value = Array.from(files);
  
  // 创建本地预览
  imagePreviewUrls.value = []; // 清空旧的预览
  uploadedFiles.value.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviewUrls.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
};

// 从预览中移除选择的图片
const removeImage = (index) => {
  imagePreviewUrls.value.splice(index, 1);
  uploadedFiles.value.splice(index, 1);
};

// 处理编辑产品中的文件上传
const handleEditFileUpload = (event) => {
  const files = event.target.files;
  if (!files.length) return;
  
  // 保存文件对象以便后续提交
  editUploadedFiles.value = Array.from(files);
  
  // 创建本地预览
  editImagePreviewUrls.value = []; // 清空旧的预览
  editUploadedFiles.value.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      editImagePreviewUrls.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
};

// 从编辑预览中移除选择的图片
const removeEditImage = (index) => {
  editImagePreviewUrls.value.splice(index, 1);
  editUploadedFiles.value.splice(index, 1);
};

// 添加新产品
const addProduct = async () => {
  isSubmitting.value = true;
  
  try {
    const formData = new FormData();
    formData.append('name', newProduct.name);
    formData.append('description', newProduct.description);
    formData.append('price', newProduct.price);
    formData.append('category', newProduct.category);
    // 添加库存相关字段
    formData.append('total_stock', newProduct.total_stock || 0);
    formData.append('warning_stock', newProduct.warning_stock || 10);
    
    // 添加上传的图片文件
    uploadedFiles.value.forEach(file => {
      formData.append('images', file);
    });
    
    const response = await fetch('/api/products', {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    
    // 成功后重置表单
    newProduct.name = '';
    newProduct.description = '';
    newProduct.price = '';
    newProduct.category = '';
    newProduct.total_stock = 0;
    newProduct.warning_stock = 10;
    uploadedFiles.value = [];
    imagePreviewUrls.value = [];
    showAddProductForm.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
    
    // 提示成功
    alert('产品添加成功');
  } catch (err) {
    console.error('添加产品失败:', err);
    alert(`添加产品失败: ${err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

// 打开编辑对话框并加载产品数据
const editProduct = (product) => {
  // 复制产品数据到编辑表单
  editingProduct.id = product.id;
  editingProduct.name = product.name;
  editingProduct.description = product.description || '';
  editingProduct.price = product.price;
  editingProduct.category = product.category || '';
  editingProduct.images = product.images || [];
  // 复制库存相关数据
  editingProduct.total_stock = product.total_stock || 0;
  editingProduct.available_stock = product.available_stock || 0;
  editingProduct.prelock_stock = product.prelock_stock || 0;
  editingProduct.warning_stock = product.warning_stock || 10;
  
  // 清空编辑中上传的图片
  editUploadedFiles.value = [];
  editImagePreviewUrls.value = [];
  
  // 显示编辑对话框
  showEditProductForm.value = true;
};

// 更新产品
const updateProduct = async () => {
  isSubmitting.value = true;
  
  try {
    const formData = new FormData();
    formData.append('name', editingProduct.name);
    formData.append('description', editingProduct.description);
    formData.append('price', editingProduct.price);
    formData.append('category', editingProduct.category);
    // 添加库存相关字段
    formData.append('total_stock', editingProduct.total_stock || 0);
    formData.append('warning_stock', editingProduct.warning_stock || 10);
    
    // 添加新上传的图片文件
    editUploadedFiles.value.forEach(file => {
      formData.append('images', file);
    });
    
    const response = await fetch(`/api/products/${editingProduct.id}`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    
    // 关闭编辑对话框
    showEditProductForm.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
    
    // 提示成功
    alert('产品更新成功');
  } catch (err) {
    console.error('更新产品失败:', err);
    alert(`更新产品失败: ${err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

// 确认删除产品
const confirmDelete = (product) => {
  productToDelete.value = product;
  showDeleteConfirm.value = true;
};

// 执行删除产品
const deleteProduct = async () => {
  isSubmitting.value = true;
  
  try {
    const response = await fetch(`/api/products/${productToDelete.value.id}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    
    // 关闭确认对话框
    showDeleteConfirm.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
    
    // 提示成功
    alert('产品已删除');
  } catch (err) {
    console.error('删除产品失败:', err);
    alert(`删除产品失败: ${err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

// 新增: 打开库存调整对话框
const adjustStock = (product) => {
  // 复制产品库存数据到调整表单
  stockAdjustProduct.id = product.id;
  stockAdjustProduct.name = product.name;
  stockAdjustProduct.total_stock = product.total_stock || 0;
  stockAdjustProduct.available_stock = product.available_stock || 0;
  stockAdjustProduct.prelock_stock = product.prelock_stock || 0;
  stockAdjustProduct.warning_stock = product.warning_stock || 10;
  
  // 设置初始调整值为当前总库存
  stockAdjustForm.newTotalStock = product.total_stock || 0;
  stockAdjustForm.reason = '';
  
  // 显示库存调整对话框
  showStockAdjustForm.value = true;
};

// 新增: 提交库存调整
const submitStockAdjust = async () => {
  if (!isStockAdjustValid.value) {
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    const formData = new FormData();
    formData.append('total_stock', stockAdjustForm.newTotalStock);
    formData.append('adjustment_reason', stockAdjustForm.reason);
    
    // 提交到专用的库存调整API
    const response = await fetch(`/api/products/${stockAdjustProduct.id}/adjust-stock`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error ${response.status}`);
    }
    
    // 关闭库存调整对话框
    showStockAdjustForm.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
    
    // 提示成功
    alert('库存调整成功');
  } catch (err) {
    console.error('库存调整失败:', err);
    alert(`库存调整失败: ${err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

// 组件挂载时获取产品列表
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.product-management {
  padding: 1.5rem;
}

.product-management h1 {
  margin-bottom: 2rem;
  font-size: 1.75rem;
  color: var(--text-color-light, #f0f0f0);
  border-bottom: 2px solid var(--primary-color, #ff9d4d);
  padding-bottom: 0.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.25rem;
  margin: 0;
  color: var(--text-color-light, #f0f0f0);
}

.btn-primary {
  background-color: var(--primary-color, #ff9d4d);
  color: var(--text-color-dark, #333);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background-color: var(--primary-color-dark, #e08a43);
}

.loading, .error-message, .empty-state {
  text-align: center;
  padding: 2rem;
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: var(--text-color-light, #f0f0f0);
}

.error-message {
  color: #e53935;
}

.product-table-container {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: auto;
  border: 1px solid var(--border-color, #444);
}

.product-table {
  width: 100%;
  border-collapse: collapse;
}

.product-table th,
.product-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #444);
  color: var(--text-color-light, #f0f0f0);
}

.product-table th {
  background-color: var(--table-header-background, #252525);
  font-weight: 600;
  color: var(--text-color-light, #f0f0f0);
}

.product-image-cell {
  width: 80px;
}

.product-image-cell img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid var(--border-color, #444);
}

.no-image {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--input-background, #2a2a2a);
  color: var(--text-color-medium, #a0a0a0);
  font-size: 0.75rem;
  border-radius: 4px;
  border: 1px solid var(--border-color, #444);
}

.actions-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  border: none;
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-edit {
  background-color: var(--success-color, #4caf50);
  color: white;
}

.btn-edit:hover {
  background-color: #43a047;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #e53935;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.delete-confirm-modal {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color, #444);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-color-light, #f0f0f0);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--text-color-light, #f0f0f0);
}

.modal-content {
  padding: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.25rem;
  border-top: 1px solid var(--border-color, #444);
}

.warning {
  color: #f44336;
  font-weight: bold;
}

/* 表单样式 */
.product-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color-light, #f0f0f0);
}

.required {
  color: #f44336;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  background-color: var(--input-background, #2a2a2a);
  font-size: 1rem;
  color: var(--text-color-light, #f0f0f0);
}

.form-group input[type="file"] {
  padding: 0.5rem 0;
  color: var(--text-color-light, #f0f0f0);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-cancel, .btn-submit {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  border: none;
}

.btn-cancel {
  background-color: var(--neutral-color, #757575);
  color: white;
}

.btn-submit {
  background-color: var(--primary-color, #ff9d4d);
  color: var(--text-color-dark, #333);
}

.btn-submit:disabled {
  background-color: #666;
  cursor: not-allowed;
}

/* 图片预览 */
.upload-preview, .current-images {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.preview-item, .current-image-item {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--border-color, #444);
}

.preview-item img, .current-image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .product-management {
    padding: 1rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .product-table th:nth-child(1),
  .product-table td:nth-child(1) {
    display: none; /* 隐藏ID列 */
  }
  
  .actions-cell {
    flex-direction: column;
  }
}

/* 库存预警样式 */
.stock-warning {
  color: #ff5252;
  font-weight: bold;
}

/* 库存信息显示样式 */
.stock-info {
  display: flex;
  gap: 1.5rem;
}

.stock-info > div {
  flex: 1;
}

.stock-value {
  font-size: 1.2rem;
  font-weight: 500;
  margin: 0.5rem 0;
  padding: 0.5rem;
  background-color: var(--input-background, #2a2a2a);
  border-radius: 4px;
  display: inline-block;
  min-width: 4rem;
  text-align: center;
}

.form-hint {
  display: block;
  color: var(--text-color-medium, #a0a0a0);
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

/* 适配小屏幕 */
@media (max-width: 992px) {
  .product-table th:nth-child(6),
  .product-table td:nth-child(6), 
  .product-table th:nth-child(8),
  .product-table td:nth-child(8) {
    display: none; /* 在小屏幕上隐藏总库存和预警阈值列 */
  }
}

@media (max-width: 768px) {
  .product-table th:nth-child(7),
  .product-table td:nth-child(7) {
    display: none; /* 在更小屏幕上隐藏可用库存列 */
  }
  
  .stock-info {
    flex-direction: column;
    gap: 1rem;
  }
}

/* 库存调整对话框样式 */
.stock-adjust-modal {
  max-width: 500px;
}

.stock-change-preview {
  background-color: var(--background-color-light, #252525);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.change-arrow {
  font-size: 1.5rem;
  font-weight: bold;
}

.change-arrow.increase {
  color: #4caf50;
}

.change-arrow.decrease {
  color: #f44336;
}

.change-amount {
  font-weight: bold;
  font-size: 1.2rem;
}

/* 调整库存按钮样式 */
.btn-adjust-stock {
  border: none;
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background-color: #2196f3;
  color: white;
}

.btn-adjust-stock:hover {
  background-color: #1976d2;
}
</style> 