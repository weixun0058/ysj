<template>
  <section class="products-page container">
    <h1 class="page-title">产品列表</h1>

    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      <span>加载中，请稍候...</span>
    </div>
    
    <div v-else-if="error" class="error-message">
      <span>{{ error }}</span>
      <button class="retry-button" @click="fetchProducts">重试</button>
    </div>
    
    <div v-else-if="products.length === 0" class="empty-products">
      暂无产品，请稍后再来查看。
    </div>
    
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <router-link :to="`/products/${product.id}`" class="product-image">
            <img
            :src="imageUrl(product)" 
            :alt="product.name" 
            @error="handleImgError"
          />
          
          <!-- 添加库存状态标签 -->
          <div v-if="product.available_stock === 0" class="stock-badge out-of-stock">
            已售罄
          </div>
          <div v-else-if="product.available_stock <= 5" class="stock-badge low-stock">
            库存紧张
            </div>
        </router-link>
        
        <div class="product-info">
          <router-link :to="`/products/${product.id}`" class="product-name">
            {{ product.name }}
          </router-link>
          <div class="product-price">¥{{ parseFloat(product.price).toFixed(2) }}</div>
          
          <!-- 添加库存显示 -->
          <div class="product-stock">
            <span v-if="product.available_stock === 0" class="stock-text out-of-stock">
              库存不足
            </span>
            <span v-else-if="product.available_stock <= 5" class="stock-text low-stock">
              仅剩 {{ product.available_stock }} 件
            </span>
            <span v-else class="stock-text">
              库存: {{ product.available_stock }} 件
            </span>
          </div>
          
          <button 
            class="add-to-cart-btn" 
            @click="handleAddToCart(product)"
            :disabled="product.available_stock === 0"
          >
            {{ product.available_stock === 0 ? '缺货中' : '加入购物车' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import { useCartStore } from '@/store/cart';

const toast = useToast();
const cartStore = useCartStore();
const backendBase = 'http://localhost:5000';

const products = ref([]);
const loading = ref(true);
const error = ref(null);

const imageUrl = (p) => {
  if (p.images && p.images.length) {
    const path = p.images[0];
    return path.startsWith('http') ? path : `${backendBase}${path}`;
  }
  return '/img/placeholder.png';
};

const handleImgError = (e) => {
  e.target.src = '/img/placeholder.png';
};

const handleAddToCart = (product) => {
  if (product.available_stock <= 0) {
    toast.error('很抱歉，该商品已售罄');
    return;
  }
  
  try {
    cartStore.addItem({
      id: product.id,
      name: product.name,
      price: parseFloat(product.price),
      image: product.images && product.images.length ? product.images[0] : '/img/placeholder.png',
      stock: product.available_stock
    }, 1);
    
    toast.success(`已将 ${product.name} 添加到购物车`);
  } catch (error) {
    toast.error(`添加到购物车失败: ${error.message}`);
  }
};

const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const res = await fetch(`${backendBase}/api/products`);
    if (!res.ok) {
      throw new Error(`API请求失败，状态码: ${res.status}`);
    }
    
    const data = await res.json();
    products.value = data.products || [];
  } catch (err) {
    console.error('获取产品失败', err);
    error.value = '获取产品列表失败，请重试';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.products-page {
  padding: 4rem 1rem;
}

.loading-indicator {
  text-align: center;
  margin: 4rem 0;
  color: #888;
  font-size: 1.125rem;
}

.error-message {
  text-align: center;
  margin: 4rem 0;
  color: #f44336;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.retry-button {
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.empty-products {
  text-align: center;
  margin: 4rem 0;
  color: #888;
  font-size: 1.125rem;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

.product-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.product-image {
  position: relative;
  display: block;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

/* 库存状态标签样式 */
.stock-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  border-radius: 4px;
  z-index: 1;
}

.stock-badge.out-of-stock {
  background-color: #f44336;
}

.stock-badge.low-stock {
  background-color: #ff9800;
}

.product-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.product-name {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3rem;
}

.product-name:hover {
  color: var(--primary-color);
}

.product-price {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e53935;
}

/* 库存文本样式 */
.product-stock {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.stock-text {
  color: #555;
}

.stock-text.out-of-stock {
  color: #f44336;
  font-weight: 500;
}

.stock-text.low-stock {
  color: #ff9800;
  font-weight: 500;
}

.add-to-cart-btn {
  padding: 0.75rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.add-to-cart-btn:hover {
  background-color: var(--primary-dark-color, #e67e22);
}

.add-to-cart-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem;
  }
  
  .product-image {
    height: 180px;
  }
}

@media (max-width: 480px) {
  .products-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

  .product-image {
    height: 220px;
  }
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color);
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 