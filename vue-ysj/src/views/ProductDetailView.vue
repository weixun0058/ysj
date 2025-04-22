<template>
  <div class="product-detail-page container">
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="product" class="product-content">
      <div class="product-gallery">
        <!-- 主图 -->
        <img :src="mainImageUrl" :alt="product.name" class="main-image" @error="handleImgError($event, 'main')"/>
        <!-- 缩略图列表 (如果有多张图片) -->
        <div v-if="product.images && product.images.length > 1" class="thumbnail-list">
          <img
            v-for="(img, index) in product.images"
            :key="index"
            :src="getImageUrl(img)"
            :alt="`${product.name} thumbnail ${index + 1}`"
            :class="{ active: img === currentImage }"
            class="thumbnail-image"
            @click="setMainImage(img)"
            @error="handleImgError($event, 'thumb')"
          />
        </div>
      </div>
      <div class="product-info">
        <h1>{{ product.name }}</h1>
        <p class="description">{{ product.description }}</p>
        <p class="price">¥{{ product.price }}</p>
        <!-- 数量选择 -->
        <div class="quantity-selector">
          <label for="quantity">数量:</label>
          <button @click="decreaseQuantity" :disabled="quantity <= 1">-</button>
          <input type="number" id="quantity" v-model.number="quantity" min="1">
          <button @click="increaseQuantity">+</button>
        </div>
        <!-- 操作按钮 -->
        <div class="actions">
          <button class="add-to-cart-button" @click="handleAddToCart">加入购物车</button>
          <button class="buy-now-button">立即购买</button>
        </div>
      </div>
    </div>
    <div v-else>产品未找到。</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useCartStore } from '../store/cart';

const route = useRoute();
const productId = ref(route.params.id);
const product = ref(null);
const loading = ref(true);
const error = ref(null);
const quantity = ref(1);
const currentImage = ref(null); // 当前显示的主图 URL
const cartStore = useCartStore();

const backendBase = 'http://localhost:5000';

// --- Helper Functions ---
const getImageUrl = (path) => {
  if (!path) return '/img/placeholder.png';
  return path.startsWith('http') ? path : `${backendBase}${path}`;
};

const mainImageUrl = computed(() => {
  return getImageUrl(currentImage.value);
});

const setMainImage = (imgPath) => {
  currentImage.value = imgPath;
};

const handleImgError = (e, type) => {
  console.warn(`图片加载失败 (${type}):`, e.target.src);
  e.target.src = '/img/placeholder.png'; // 统一替换为占位符
};

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--;
  }
};

const increaseQuantity = () => {
  quantity.value++;
};

// --- 新增：添加到购物车处理函数 ---
const handleAddToCart = () => {
  if (product.value) {
    cartStore.addItem(product.value, quantity.value);
    alert(`${quantity.value}件 ${product.value.name} 已加入购物车！`);
  } else {
    alert('无法添加产品，请稍后再试');
  }
};

// --- Fetch Data --- 
onMounted(async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch(`/api/products/${productId.value}`);
    if (!res.ok) {
      if (res.status === 404) {
        throw new Error('产品未找到');
      } else {
        throw new Error(`HTTP错误: ${res.status}`);
      }
    }
    const data = await res.json();
    product.value = data.product;
    // 设置初始主图
    if (product.value && product.value.images && product.value.images.length > 0) {
       currentImage.value = product.value.images[0];
    }

  } catch (err) {
    console.error('获取产品详情失败:', err);
    error.value = err.message || '加载失败，请稍后重试';
    product.value = null; // 清空产品信息
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.product-detail-page {
  padding: 4rem 1rem;
}

.product-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  align-items: start; /* 顶部对齐 */
}

.product-gallery {
  /* 样式可以后续细化 */
}

.main-image {
  width: 100%;
  aspect-ratio: 1 / 1; /* 主图保持方形 */
  object-fit: cover;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.thumbnail-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.thumbnail-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.thumbnail-image.active {
  border-color: var(--primary-color);
}

.product-info h1 {
  font-size: 2rem; /* 调整标题大小 */
  margin-bottom: 1rem;
}

.description {
  color: var(--text-color-light);
  opacity: 0.9;
  margin-bottom: 1.5rem;
  line-height: 1.7;
}

.price {
  font-size: 1.8rem;
  color: var(--primary-color);
  font-weight: bold;
  margin-bottom: 2rem;
}

.quantity-selector {
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
}

.quantity-selector label {
  margin-right: 0.5rem;
}

.quantity-selector button {
  width: 30px;
  height: 30px;
  border: 1px solid var(--border-color);
  background-color: var(--card-background);
  color: var(--text-color-light);
  cursor: pointer;
}

.quantity-selector input {
  width: 50px;
  height: 30px;
  text-align: center;
  border: 1px solid var(--border-color);
  background-color: var(--background-color);
  color: var(--text-color-light);
  margin: 0 0.5rem;
  /* 隐藏数字输入框的上下箭头 (可选) */
  -moz-appearance: textfield;
}
.quantity-selector input::-webkit-outer-spin-button,
.quantity-selector input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.actions button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease, color 0.3s ease;
  margin-right: 1rem;
}

.add-to-cart-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
}
.add-to-cart-button:hover {
   background-color: #ffab6f;
}

.buy-now-button {
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}
.buy-now-button:hover {
   background-color: var(--primary-color);
   color: var(--text-color-dark);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .product-content {
      grid-template-columns: 1fr; /* 移动端堆叠 */
      gap: 2rem;
  }
  .product-info h1 {
      font-size: 1.6rem;
  }
  .price {
      font-size: 1.5rem;
  }
}
</style> 