<template>
  <div class="cart-page container">
    <h1>购物车</h1>

    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <p>您的购物车是空的。</p>
      <router-link to="/products">去逛逛</router-link>
    </div>

    <div v-else>
      <div class="cart-items">
        <div v-for="item in cartStore.items" :key="item.productId" class="cart-item">
          <img :src="getImageUrl(item.image)" :alt="item.name" class="item-image">
          <div class="item-details">
            <h2>{{ item.name }}</h2>
            <p>单价: ¥{{ item.price }}</p>
            <div class="item-quantity">
              <label>数量:</label>
              <button @click="decreaseItemQuantity(item)">-</button>
              <input type="number" :value="item.quantity" @change="updateItemQuantity(item, $event)" min="1">
              <button @click="increaseItemQuantity(item)">+</button>
            </div>
            <p>小计: ¥{{ (item.price * item.quantity).toFixed(2) }}</p>
          </div>
          <button @click="removeItemFromCart(item.productId)" class="remove-item-button">移除</button>
        </div>
      </div>

      <div class="cart-summary">
        <p>总计数量: {{ cartStore.totalItems }}</p>
        <p>总计金额: ¥{{ cartStore.totalPrice }}</p>
        <button @click="clearCartItems" class="clear-cart-button">清空购物车</button>
        <button class="checkout-button">去结算</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart';
import { computed } from 'vue';

const cartStore = useCartStore();
const backendBase = 'http://localhost:5000'; // 与 ProductDetailView 保持一致

const getImageUrl = (path) => {
  if (!path || path === '/img/placeholder.png') return '/img/placeholder.png';
  return path.startsWith('http') ? path : `${backendBase}${path}`;
};

const decreaseItemQuantity = (item) => {
  if (item.quantity > 1) {
    cartStore.updateQuantity(item.productId, item.quantity - 1);
  }
};

const increaseItemQuantity = (item) => {
  cartStore.updateQuantity(item.productId, item.quantity + 1);
};

const updateItemQuantity = (item, event) => {
  const newQuantity = parseInt(event.target.value, 10);
  if (!isNaN(newQuantity) && newQuantity >= 0) {
     cartStore.updateQuantity(item.productId, newQuantity);
  } else {
      // 如果输入无效，可能需要重置回原来的值
      event.target.value = item.quantity;
  }
};

const removeItemFromCart = (productId) => {
  if (confirm('确定要移除这个商品吗？')) {
    cartStore.removeItem(productId);
  }
};

const clearCartItems = () => {
  if (confirm('确定要清空购物车吗？')) {
    cartStore.clearCart();
  }
}
</script>

<style scoped>
.cart-page {
  padding: 2rem 1rem;
}

.cart-page h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.empty-cart {
  text-align: center;
  padding: 3rem 0;
}

.empty-cart p {
  margin-bottom: 1rem;
}

.cart-items {
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.item-details {
  flex-grow: 1;
}

.item-details h2 {
  font-size: 1.1rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-color-light); /* Ensure title color is appropriate */
}

.item-quantity {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
}
.item-quantity label {
  margin-right: 0.5rem;
}
.item-quantity button {
  width: 25px;
  height: 25px;
  cursor: pointer;
}
.item-quantity input {
  width: 40px;
  text-align: center;
  margin: 0 0.5rem;
  background-color: var(--background-color);
  color: var(--text-color-light);
  border: 1px solid var(--border-color);
   -moz-appearance: textfield;
}
.item-quantity input::-webkit-outer-spin-button,
.item-quantity input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}


.remove-item-button {
  background: none;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  font-size: 0.9rem;
}

.cart-summary {
  border-top: 2px solid var(--border-color-light);
  padding-top: 1.5rem;
  text-align: right;
}

.cart-summary p {
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
}

.cart-summary button {
   padding: 0.7rem 1.2rem;
   border-radius: 5px;
   cursor: pointer;
   font-weight: bold;
   margin-left: 1rem; /* Add some space between buttons */
}

.clear-cart-button {
    background-color: #555;
    color: #eee;
    border: none;
}
.clear-cart-button:hover {
    background-color: #777;
}

.checkout-button {
    background-color: var(--primary-color);
    color: var(--text-color-dark);
    border: none;
}
.checkout-button:hover {
    background-color: #ffab6f;
}
</style> 