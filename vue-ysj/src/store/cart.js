import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue'; 
import { useToast } from 'vue-toastification';

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
  const toast = useToast();
  
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

  const totalAmount = computed(() => {
    return items.value.reduce((total, item) => total + parseFloat(item.price) * item.quantity, 0);
  });

  const totalPrice = computed(() => {
    return items.value.reduce((total, item) => total + parseFloat(item.price) * item.quantity, 0).toFixed(2);
  });

  // Actions
  function addItem(product, quantity = 1) {
    if (!product || !product.id) {
      throw new Error('无效的商品数据');
    }
    
    if (quantity <= 0) {
      throw new Error('商品数量必须大于0');
    }
    
    if (product.stock <= 0) {
      throw new Error('该商品已售罄');
    }

    const existingItemIndex = items.value.findIndex(item => item.id === product.id);

    if (existingItemIndex >= 0) {
      // 已存在该商品，增加数量
      const newQuantity = items.value[existingItemIndex].quantity + quantity;
      
      // 检查库存
      if (newQuantity > product.stock) {
        throw new Error(`库存不足，当前最多可购买 ${product.stock} 件`);
      }
      
      items.value[existingItemIndex].quantity = newQuantity;
    } else {
      // 添加新商品
      items.value.push({
        id: product.id,
        name: product.name,
        price: product.price, // 已经在ProductsView和ProductDetailView中转换为数字
        image: product.image || (product.images && product.images.length > 0 ? product.images[0] : '/img/placeholder.png'),
        quantity: quantity,
        stock: product.stock
      });
    }
    
    saveCart();
  }

  function removeItem(productId) {
    items.value = items.value.filter(item => item.id !== productId);
     console.log('购物车已更新 (移除后):', items.value);
    saveCart();
  }

  function updateQuantity(productId, quantity) {
    const index = items.value.findIndex(item => item.id === productId);
    
    if (index < 0) {
      throw new Error('商品不在购物车中');
    }
    
    if (quantity <= 0) {
      throw new Error('商品数量必须大于0');
    }
    
    const item = items.value[index];
    
    if (quantity > item.stock) {
      throw new Error(`库存不足，当前最多可购买 ${item.stock} 件`);
    }
    
    item.quantity = quantity;
    saveCart();
  }

  function clearCart() {
    items.value = [];
    console.log('购物车已清空');
    saveCart();
  }

  // 从localStorage读取购物车数据
  const initCart = () => {
    try {
      const savedCart = localStorage.getItem('ysj_cart');
      if (savedCart) {
        items.value = JSON.parse(savedCart);
      }
    } catch (error) {
      console.error('读取购物车数据失败:', error);
      items.value = [];
    }
  };
  
  // 保存购物车数据到localStorage
  const saveCart = () => {
    try {
      localStorage.setItem('ysj_cart', JSON.stringify(items.value));
    } catch (error) {
      console.error('保存购物车数据失败:', error);
      toast.error('保存购物车失败，请检查浏览器存储设置');
    }
  };

  // 初始化购物车
  initCart();

  return {
    items,
    totalItems,
    totalAmount,
    totalPrice,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
  };
}); 