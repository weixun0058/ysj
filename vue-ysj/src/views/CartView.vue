<template>
  <div class="cart-page">
    <h1 class="page-title">购物车</h1>

    <!-- 加载中状态 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">正在加载购物车...</p>
    </div>

    <!-- 空购物车状态 -->
    <div v-else-if="!cartStore.items.length" class="empty-cart">
      <div class="cart-icon">
        <svg xmlns="http://www.w3.org/2000/svg" class="cart-svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h2 class="empty-title">您的购物车是空的</h2>
      <p class="empty-message">浏览我们的商品，将喜欢的商品添加到购物车</p>
      <router-link to="/products" class="browse-button">
        浏览商品
      </router-link>
    </div>

    <!-- 购物车内容 -->
    <div v-else class="cart-content">
      <div class="cart-table-container">
        <table class="cart-table">
          <thead>
            <tr>
              <th class="product-column">商品</th>
              <th class="price-column">单价</th>
              <th class="quantity-column">数量</th>
              <th class="subtotal-column">小计</th>
              <th class="action-column">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cartStore.items" :key="item.id" class="cart-item">
              <td class="product-cell">
                <div class="product-info">
                  <div class="product-image-container">
                    <img :src="formatImageUrl(item.image)" 
                      class="product-image" 
                      :alt="item.name"
                      @error="handleImageError">
                  </div>
                  <div class="product-details">
                    <h3 class="product-name">{{ item.name }}</h3>
                    <div v-if="item.stock <= 5" class="stock-warning">
                      <span class="low-stock" v-if="item.stock > 0">库存紧张: 仅剩 {{ item.stock }} 件</span>
                      <span class="out-of-stock" v-else>已售罄</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="price-cell">
                <span class="price-text">¥{{ parseFloat(item.price).toFixed(2) }}</span>
              </td>
              <td class="quantity-cell">
                <div class="quantity-selector">
                  <button 
                    @click="decreaseQuantity(item)"
                    class="quantity-btn decrease-btn"
                    :disabled="item.quantity <= 1 || updateLoading">
                    -
                  </button>
                  <input 
                    type="number"
                    v-model.number="item.quantity"
                    @change="updateItemQuantity(item)"
                    min="1"
                    :max="item.stock"
                    class="quantity-input"
                    :disabled="updateLoading">
                  <button 
                    @click="increaseQuantity(item)"
                    class="quantity-btn increase-btn"
                    :disabled="item.quantity >= item.stock || updateLoading">
                    +
                  </button>
                </div>
              </td>
              <td class="subtotal-cell">
                <span class="subtotal-text">¥{{ (parseFloat(item.price) * item.quantity).toFixed(2) }}</span>
              </td>
              <td class="action-cell">
                <button 
                  @click="removeFromCart(item.id)"
                  class="remove-btn"
                  :disabled="updateLoading">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 购物车底部结算区 -->
      <div class="cart-footer">
        <div class="cart-actions">
          <button 
            @click="clearCart"
            class="clear-cart-btn"
            :disabled="updateLoading">
            清空购物车
          </button>
            </div>
        
        <div class="cart-summary">
          <div class="summary-text">
            <span>已选 <span class="highlight">{{ cartStore.totalItems }}</span> 件商品</span>
            <span class="total-amount">总计: <span class="total-price">¥{{ cartStore.totalAmount.toFixed(2) }}</span></span>
          </div>
          <button 
            @click="goToCheckout"
            :disabled="updateLoading || cartStore.totalItems === 0"
            class="checkout-btn">
            结算
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCartStore } from '@/store/cart';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const cartStore = useCartStore();
const router = useRouter();
const toast = useToast();

const isLoading = ref(true);
const updateLoading = ref(false);

// 格式化图片URL
const formatImageUrl = (imgPath) => {
  if (!imgPath) return '/img/placeholder.png';
  
  // 检查是否已经是完整的URL（以http或https开头）
  if (imgPath.startsWith('http')) {
    return imgPath;
  }
  
  // 检查是否需要添加基础URL（如果以/开头）
  if (imgPath.startsWith('/')) {
    return `http://localhost:5000${imgPath}`;
  }
  
  // 默认返回占位图片
  return '/img/placeholder.png';
};

// 增加商品数量
const increaseQuantity = async (item) => {
  if (item.quantity >= item.stock) {
    toast.warning(`已达到最大可购买数量: ${item.stock}件`);
    return;
  }
  
  try {
    updateLoading.value = true;
    await cartStore.updateQuantity(item.id, item.quantity + 1);
    toast.success('已更新数量');
  } catch (error) {
    toast.error(error.message || '更新数量失败');
    await fetchCartData();
  } finally {
    updateLoading.value = false;
  }
};

// 减少商品数量
const decreaseQuantity = async (item) => {
  if (item.quantity <= 1) {
    return;
  }
  
  try {
    updateLoading.value = true;
    await cartStore.updateQuantity(item.id, item.quantity - 1);
    toast.success('已更新数量');
  } catch (error) {
    toast.error(error.message || '更新数量失败');
    await fetchCartData();
  } finally {
    updateLoading.value = false;
  }
};

// 直接更新商品数量
const updateItemQuantity = async (item) => {
  // 确保数量为有效值
  if (isNaN(item.quantity) || item.quantity < 1) {
    item.quantity = 1;
  } else if (item.quantity > item.stock) {
    item.quantity = item.stock;
    toast.warning(`已调整为最大可购买数量: ${item.stock}件`);
  }
  
  try {
    updateLoading.value = true;
    await cartStore.updateQuantity(item.id, item.quantity);
    toast.success('已更新数量');
  } catch (error) {
    toast.error(error.message || '更新数量失败');
    await fetchCartData();
  } finally {
    updateLoading.value = false;
  }
};

// 从购物车移除商品
const removeFromCart = async (productId) => {
  try {
    updateLoading.value = true;
    cartStore.removeItem(productId);
    toast.success('已从购物车移除');
  } catch (error) {
    toast.error(error.message || '移除商品失败');
  } finally {
    updateLoading.value = false;
  }
};

// 清空购物车
const clearCart = async () => {
  if (!confirm('确定要清空购物车吗？')) {
    return;
  }
  
  try {
    updateLoading.value = true;
    cartStore.clearCart();
    toast.success('购物车已清空');
  } catch (error) {
    toast.error(error.message || '清空购物车失败');
  } finally {
    updateLoading.value = false;
  }
};

// 处理图片加载错误
const handleImageError = (event) => {
  event.target.src = '/img/placeholder.png';
};

// 跳转到结算页面
const goToCheckout = () => {
  if (cartStore.totalItems === 0) {
    toast.warning('购物车中没有商品，无法结算');
    return;
  }
  // 检查是否有商品售罄
  const soldOutItems = cartStore.items.filter(item => item.stock <= 0);
  if (soldOutItems.length > 0) {
    toast.error('购物车中有已售罄商品，请移除后再结算');
    return;
  }
  
  // 检查是否有商品超出库存
  const overStockItems = cartStore.items.filter(item => item.quantity > item.stock);
  if (overStockItems.length > 0) {
    toast.error('部分商品库存不足，请调整数量后再结算');
    return;
  }
  
  router.push('/checkout');
};

// 获取购物车数据
const fetchCartData = async () => {
  isLoading.value = true;
  try {
    // 这里可以添加从后端获取最新购物车数据的逻辑
    await new Promise(resolve => setTimeout(resolve, 300));
  } catch (error) {
    toast.error('获取购物车数据失败');
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await fetchCartData();
});
</script>

<style scoped>
/* 页面基础样式 */
.cart-page {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

/* 加载中状态 */
.loading-container {
  text-align: center;
  padding: 2.5rem 0;
}

.loading-spinner {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-bottom: 2px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 0.75rem;
  color: #666;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 空购物车状态 */
.empty-cart {
  text-align: center;
  padding: 2.5rem 0;
  border: 1px solid var(--border-color, #444);
  background-color: var(--card-background, #1a1a1a);
  border-radius: 4px;
}

.cart-icon {
  margin-bottom: 1rem;
}

.cart-svg {
  width: 4rem;
  height: 4rem;
  margin: 0 auto;
  color: #666;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-color-light, #f0f0f0);
}

.empty-message {
  color: #999;
  margin-bottom: 1rem;
}

.browse-button {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background-color: var(--primary-color);
  color: white;
  border-radius: 4px;
  font-size: 0.875rem;
  text-decoration: none;
  transition: background-color 0.2s;
}

.browse-button:hover {
  background-color: var(--primary-dark-color, #e67e22);
}

/* 购物车内容 */
.cart-content {
  margin-top: 1rem;
}

.cart-table-container {
  background-color: var(--card-background, #1a1a1a);
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  overflow: hidden;
}

.cart-table {
  width: 100%;
  border-collapse: collapse;
}

.cart-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 500;
  color: #999;
  background-color: rgba(0, 0, 0, 0.2);
}

.cart-table td {
  padding: 1rem;
  border-top: 1px solid var(--border-color, #444);
  color: var(--text-color-light, #f0f0f0);
}

.product-column {
  width: 40%;
}

.price-column, .quantity-column, .subtotal-column {
  width: 16%;
  text-align: center;
}

.action-column {
  width: 12%;
  text-align: center;
}

/* 表格内容样式 */
.product-info {
  display: flex;
  align-items: center;
}

.product-image-container {
  width: 4rem;
  height: 4rem;
  flex-shrink: 0;
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.product-details {
  margin-left: 1rem;
  flex: 1;
}

.product-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-color-light, #f0f0f0);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stock-warning {
  margin-top: 0.25rem;
  font-size: 0.75rem;
}

.low-stock {
  color: #ff9800;
  font-weight: 500;
}

.out-of-stock {
  color: #f44336;
  font-weight: 500;
}

.price-cell, .subtotal-cell {
  text-align: center;
}

.price-text {
  font-size: 0.875rem;
}

.subtotal-text {
  font-size: 0.875rem;
  color: var(--primary-color);
  font-weight: 500;
}

/* 数量选择器 */
.quantity-cell {
  text-align: center;
}

.quantity-selector {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
}

.quantity-btn {
  width: 1.75rem;
  height: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.2);
  border: none;
  color: var(--text-color-light, #f0f0f0);
  cursor: pointer;
}

.decrease-btn {
  border-radius: 4px 0 0 4px;
}

.increase-btn {
  border-radius: 0 4px 4px 0;
}

.quantity-btn:hover:not(:disabled) {
  background-color: rgba(0, 0, 0, 0.4);
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-input {
  width: 2.5rem;
  height: 1.75rem;
  border: none;
  border-left: 1px solid var(--border-color, #444);
  border-right: 1px solid var(--border-color, #444);
  text-align: center;
  font-size: 0.875rem;
  background-color: var(--card-background, #1a1a1a);
  color: var(--text-color-light, #f0f0f0);
}

.quantity-input::-webkit-inner-spin-button,
.quantity-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.quantity-input {
  -moz-appearance: textfield;
}

.action-cell {
  text-align: center;
}

.remove-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.remove-btn:hover {
  color: #f44336;
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 购物车底部结算区 */
.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--card-background, #1a1a1a);
  border: 1px solid var(--border-color, #444);
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
}

.clear-cart-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 0.875rem;
  cursor: pointer;
}

.clear-cart-btn:hover {
  color: #f44336;
}

.cart-summary {
  display: flex;
  align-items: center;
}

.summary-text {
  font-size: 0.875rem;
  margin-right: 1.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.highlight {
  color: var(--primary-color);
  font-weight: 500;
}

.total-amount {
  margin-left: 1rem;
}

.total-price {
  font-size: 1.25rem;
  color: var(--primary-color);
  font-weight: 500;
}

.checkout-btn {
  padding: 0.5rem 2rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
   cursor: pointer;
  transition: background-color 0.2s;
}

.checkout-btn:hover {
  background-color: var(--primary-dark-color, #e67e22);
}

.checkout-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .cart-footer {
    flex-direction: column;
    align-items: flex-start;
}

  .cart-actions {
    margin-bottom: 1rem;
  }
  
  .cart-summary {
    width: 100%;
    justify-content: space-between;
  }
  
  .product-column {
    width: 50%;
  }
  
  .price-column, .subtotal-column {
    width: 15%;
  }
  
  .quantity-column {
    width: 20%;
  }
}

@media (max-width: 640px) {
  .cart-table {
    display: block;
  }
  
  .cart-table thead {
    display: none;
}
  
  .cart-table tbody, .cart-table tr, .cart-table td {
    display: block;
    width: 100%;
}

  .cart-item {
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-color, #444);
  }
  
  .product-cell, .price-cell, .quantity-cell, .subtotal-cell, .action-cell {
    padding: 0.5rem 1rem;
    text-align: left;
    border: none;
}
  
  .price-cell::before, .quantity-cell::before, .subtotal-cell::before {
    content: attr(data-label);
    font-weight: 500;
    display: inline-block;
    width: 80px;
  }
  
  .action-cell {
    text-align: right;
  }
}
</style> 