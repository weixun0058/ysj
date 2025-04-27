<template>
  <section class="product-detail-page container">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>正在加载产品信息...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchProduct">重试</button>
    </div>
    
    <div v-else-if="!product" class="not-found-container">
      <h2>很抱歉，未找到该产品</h2>
      <router-link to="/products" class="back-to-products">返回产品中心</router-link>
    </div>
    
    <div v-else class="product-detail-container">
      <div class="product-image-gallery">
        <div class="main-image-container">
          <img 
            :src="mainImage" 
            :alt="product.name" 
            class="main-image"
            @error="handleImgError"
          />
          <div 
            v-if="product.available_stock <= 0" 
            class="stock-badge out-of-stock"
          >
            已售罄
          </div>
          <div 
            v-else-if="product.available_stock <= product.warning_stock" 
            class="stock-badge low-stock"
          >
            库存紧张
          </div>
        </div>
        
        <div v-if="product.images && product.images.length > 1" class="thumbnail-container">
          <div 
            v-for="(image, index) in product.images" 
            :key="index"
            class="thumbnail"
            :class="{ active: selectedImageIndex === index }"
            @click="selectedImageIndex = index"
          >
            <img 
              :src="formatImageUrl(image)" 
              :alt="`${product.name} 预览 ${index + 1}`"
              @error="handleImgError"
          />
          </div>
        </div>
      </div>
      
      <div class="product-info">
        <h1 class="product-name">{{ product.name }}</h1>
        <div class="product-price">¥{{ parseFloat(product.price).toFixed(2) }}</div>
        
        <div class="product-stock" :class="{'out-of-stock': product.available_stock === 0, 'low-stock': product.available_stock > 0 && product.available_stock <= 5}">
          <span v-if="product.available_stock === 0" class="stock-status">库存不足</span>
          <span v-else-if="product.available_stock <= 5" class="stock-status">库存紧张，仅剩 {{ product.available_stock }} 件</span>
          <span v-else class="stock-status">库存充足：{{ product.available_stock }} 件</span>
        </div>
        
        <div class="product-description">
          {{ product.description }}
        </div>
        
        <div class="quantity-selector">
          <span class="quantity-label">数量:</span>
          <div class="quantity-controls">
            <button 
              class="quantity-btn" 
              @click="decreaseQuantity" 
              :disabled="quantity <= 1 || product.available_stock <= 0"
            >
              -
            </button>
            <input 
              type="number" 
              v-model.number="quantity" 
              :min="1"
              :max="product.available_stock" 
              :disabled="product.available_stock <= 0"
            />
            <button 
              class="quantity-btn" 
              @click="increaseQuantity" 
              :disabled="quantity >= product.available_stock || product.available_stock <= 0"
            >
              +
            </button>
          </div>
        </div>
        
        <div class="action-buttons">
          <button 
            class="add-to-cart-btn"
            :disabled="product.available_stock <= 0"
            @click="addToCart"
          >
            {{ product.available_stock === 0 ? '缺货中' : '加入购物车' }}
          </button>
          <button 
            class="buy-now-btn"
            :disabled="product.available_stock <= 0"
            @click="buyNow"
          >
            {{ product.available_stock === 0 ? '暂时无法购买' : '立即购买' }}
          </button>
        </div>
        
        <div class="product-meta">
          <div class="meta-item">
            <span class="meta-label">产品类别:</span>
            <span class="meta-value">{{ product.category || '未分类' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">产品编号:</span>
            <span class="meta-value">{{ product.sku || product.id }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="product" class="product-details-tabs">
      <div class="tabs-header">
        <div 
          v-for="(tab, index) in tabs" 
          :key="tab.id"
          class="tab-header-item"
          :class="{ active: activeTabIndex === index }"
          @click="activeTabIndex = index"
        >
          {{ tab.label }}
        </div>
      </div>
      
      <div class="tab-content">
        <div v-if="activeTabIndex === 0" class="tab-pane">
          <div class="detail-content">
            <h3>产品详情</h3>
            <div v-html="product.content || '暂无详细描述'"></div>
          </div>
        </div>
        
        <div v-if="activeTabIndex === 1" class="tab-pane">
          <div class="detail-content">
            <h3>规格参数</h3>
            <div v-if="product.specs && product.specs.length" class="specs-table">
              <div v-for="(spec, index) in product.specs" :key="index" class="spec-item">
                <div class="spec-name">{{ spec.name }}</div>
                <div class="spec-value">{{ spec.value }}</div>
              </div>
            </div>
            <div v-else class="no-specs-message">暂无规格参数信息</div>
          </div>
        </div>
      </div>
  </div>
  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useCartStore } from '@/store/cart';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const cartStore = useCartStore();

const backendBase = 'http://localhost:5000';
const product = ref(null);
const loading = ref(true);
const error = ref(null);
const quantity = ref(1);
const selectedImageIndex = ref(0);
const activeTabIndex = ref(0);

const tabs = [
  { id: 'details', label: '产品详情' },
  { id: 'specs', label: '规格参数' }
];

const formatImageUrl = (imagePath) => {
  if (!imagePath) return '/img/placeholder.png';
  return imagePath.startsWith('http') ? imagePath : `${backendBase}${imagePath}`;
};

const handleImgError = (e) => {
  e.target.src = '/img/placeholder.png';
};

const mainImage = computed(() => {
  if (!product.value || !product.value.images || product.value.images.length === 0) {
    return '/img/placeholder.png';
  }
  return formatImageUrl(product.value.images[selectedImageIndex.value]);
});

const stockStatusClass = computed(() => {
  if (!product.value) return '';
  if (product.value.available_stock <= 0) return 'out-of-stock';
  if (product.value.available_stock <= product.value.warning_stock) return 'low-stock';
  return 'in-stock';
});

const increaseQuantity = () => {
  if (product.value && quantity.value < product.value.available_stock) {
    quantity.value++;
  }
};

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};

const addToCart = () => {
  if (!product.value) return;
  
  if (product.value.available_stock <= 0) {
    toast.error('很抱歉，该商品已售罄');
    return;
  }
  
  if (quantity.value > product.value.available_stock) {
    toast.error(`库存不足，当前最多可购买 ${product.value.available_stock} 件`);
    quantity.value = product.value.available_stock;
    return;
  }
  
  try {
    cartStore.addItem({
      id: product.value.id,
      name: product.value.name,
      price: parseFloat(product.value.price),
      image: product.value.images && product.value.images.length ? product.value.images[0] : '/img/placeholder.png',
      stock: product.value.available_stock
    }, quantity.value);
    
    toast.success(`已将 ${quantity.value} 件 ${product.value.name} 添加到购物车`);
  } catch (error) {
    toast.error(`添加到购物车失败: ${error.message}`);
  }
};

const buyNow = () => {
  if (!product.value) return;
  
  if (product.value.available_stock <= 0) {
    toast.error('很抱歉，该商品已售罄');
    return;
  }
  
  if (quantity.value > product.value.available_stock) {
    toast.error(`库存不足，当前最多可购买 ${product.value.available_stock} 件`);
    quantity.value = product.value.available_stock;
    return;
  }
  
  try {
    // 先添加到购物车
    cartStore.addItem({
      id: product.value.id,
      name: product.value.name,
      price: parseFloat(product.value.price),
      image: product.value.images && product.value.images.length ? product.value.images[0] : '/img/placeholder.png',
      stock: product.value.available_stock
    }, quantity.value);
    
    // 然后跳转到结算页面
    router.push('/checkout');
  } catch (error) {
    toast.error(`立即购买失败: ${error.message}`);
  }
};

const fetchProduct = async () => {
  const productId = route.params.id;
  if (!productId) {
    return;
  }
  
  loading.value = true;
  error.value = null;
  
  try {
    const res = await fetch(`${backendBase}/api/products/${productId}`);
    if (!res.ok) {
      throw new Error(`获取产品信息失败，状态码: ${res.status}`);
      }
    
    const data = await res.json();
    product.value = data.product;
    quantity.value = 1;
    selectedImageIndex.value = 0;
  } catch (err) {
    console.error('获取产品信息失败', err);
    error.value = '获取产品信息失败，请重试或返回产品列表';
    product.value = null;
  } finally {
    loading.value = false;
  }
};

// 监听路由变化，获取产品信息
watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) {
    fetchProduct();
  }
});

onMounted(() => {
  fetchProduct();
});
</script>

<style scoped>
.product-detail-page {
  padding: 4rem 1rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 2rem;
  background-color: #fff8f8;
  border: 1px solid #ffcdd2;
  border-radius: 4px;
  margin: 2rem 0;
}

.product-detail-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.product-image-gallery {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

.main-image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stock-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  z-index: 2;
}

.out-of-stock {
  background-color: rgba(244, 67, 54, 0.9);
  color: white;
}

.low-stock {
  background-color: rgba(255, 152, 0, 0.9);
  color: white;
}

.thumbnail-container {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 0.25rem;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
}

.thumbnail:hover {
  opacity: 0.8;
}

.thumbnail.active {
  border-color: var(--primary-color);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
  min-width: 300px;
}

.product-name {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.product-price {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.product-stock {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
  background-color: rgba(0,0,0,0.05);
}

.product-stock.out-of-stock .stock-value {
  color: #f44336;
}

.product-stock.low-stock .stock-value {
  color: #ff9800;
}

.product-stock.in-stock .stock-value {
  color: #4caf50;
}

.stock-label {
  font-weight: 600;
}

.product-description {
  margin-bottom: 1.5rem;
  color: var(--text-color-light);
  line-height: 1.6;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.quantity-label {
  font-weight: 600;
}

.quantity-controls {
  display: flex;
  align-items: center;
}

.quantity-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color-light);
  border: 1px solid var(--border-color);
  cursor: pointer;
}

.quantity-btn:first-child {
  border-radius: 4px 0 0 4px;
}

.quantity-btn:last-child {
  border-radius: 0 4px 4px 0;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-controls input {
  width: 50px;
  height: 32px;
  border: 1px solid var(--border-color);
  border-left: none;
  border-right: none;
  text-align: center;
  font-size: 0.875rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.add-to-cart-btn, 
.buy-now-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.add-to-cart-btn {
  background-color: rgba(255, 171, 111, 0.2);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.add-to-cart-btn:hover:not(:disabled) {
  background-color: rgba(255, 171, 111, 0.3);
}

.buy-now-btn {
  background-color: var(--primary-color);
  color: white;
}

.buy-now-btn:hover:not(:disabled) {
   background-color: #ffab6f;
}

.add-to-cart-btn:disabled, 
.buy-now-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.product-meta {
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
}

.meta-item {
  display: flex;
  margin-bottom: 0.5rem;
}

.meta-label {
  flex: 0 0 100px;
  font-weight: 600;
}

.meta-value {
  color: var(--text-color-light);
}

.product-details-tabs {
  margin-top: 3rem;
}

.tabs-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
}

.tab-header-item {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-weight: 600;
  transition: all 0.3s ease;
}

.tab-header-item.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.tab-content {
  min-height: 200px;
}

.tab-pane {
  padding: 1rem 0;
}

.detail-content h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.specs-table {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 0.5rem;
}

.spec-item {
  display: flex;
  padding: 0.5rem;
  background-color: rgba(0,0,0,0.02);
  border-radius: 0.25rem;
}

.spec-name {
  flex: 0 0 120px;
  font-weight: 600;
}

.no-specs-message {
  color: var(--text-color-light);
  font-style: italic;
}

@media (max-width: 768px) {
  .product-detail-container {
    flex-direction: column;
  }
  
  .product-image-gallery,
  .product-info {
    max-width: 100%;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .specs-table {
    grid-template-columns: 1fr;
  }
}
</style> 