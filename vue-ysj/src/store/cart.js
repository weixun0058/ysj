import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue'; 

// Helper function to load cart from localStorage
const loadCartFromLocalStorage = () => {
  const savedCart = localStorage.getItem('ysj_cart'); // Use a specific key
  if (savedCart) {
    try {
      const parsed = JSON.parse(savedCart);
      // Basic validation: check if it's an array
      if (Array.isArray(parsed)) {
        return parsed;
      } else {
        console.error('Cart data in localStorage is not an array, clearing.');
        localStorage.removeItem('ysj_cart');
      }
    } catch (e) {
      console.error('Failed to parse cart from localStorage, clearing.', e);
      localStorage.removeItem('ysj_cart'); // Clear invalid data
    }
  }
  return []; // Default to empty array if not found or invalid
};

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref(loadCartFromLocalStorage()); // Load initial state

  // Watch for changes in items and save to localStorage
  watch(
    items,
    (newItems) => {
      try {
        localStorage.setItem('ysj_cart', JSON.stringify(newItems));
        console.log('Cart saved to localStorage');
      } catch (e) {
        console.error('Failed to save cart to localStorage', e);
      }
    },
    { deep: true } // Use deep watch for nested changes (like quantity)
  );

  // Getters (computed properties)
  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0);
  });

  const totalPrice = computed(() => {
    return items.value.reduce((total, item) => total + item.price * item.quantity, 0).toFixed(2);
  });

  // Actions
  function addItem(product, quantity = 1) {
    if (!product || !product.id || quantity <= 0) {
      console.error('无效的产品或数量', product, quantity);
      return;
    }

    const existingItem = items.value.find(item => item.productId === product.id);

    if (existingItem) {
      // 如果已存在，增加数量
      existingItem.quantity += quantity;
    } else {
      // 如果不存在，添加新项目
      items.value.push({
        productId: product.id,
        name: product.name,
        price: product.price,
        image: product.images && product.images.length > 0 ? product.images[0] : '/img/placeholder.png', // 取第一张图或占位符
        quantity: quantity,
      });
    }
    console.log('购物车已更新:', items.value);
    // TODO: 后续可以考虑持久化到 localStorage
  }

  function removeItem(productId) {
     items.value = items.value.filter(item => item.productId !== productId);
     console.log('购物车已更新 (移除后):', items.value);
  }

  function updateQuantity(productId, quantity) {
    const item = items.value.find(item => item.productId === productId);
    if (item) {
      if (quantity > 0) {
        item.quantity = quantity;
      } else {
        // 数量小于等于0则移除
        removeItem(productId);
      }
    } else {
       console.warn('尝试更新不存在的购物车项目', productId);
    }
     console.log('购物车已更新 (数量更新后):', items.value);
  }

  function clearCart() {
    items.value = [];
    console.log('购物车已清空');
  }

  return {
    items,
    totalItems,
    totalPrice,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
  };
}); 