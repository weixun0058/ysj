<template>
  <section class="products-page container">
    <h1>产品中心</h1>

    <div v-if="products.length === 0" class="loading-indicator">加载中...</div>
    <div v-else class="product-list-container">
      <router-link
        v-for="p in products"
        :key="p.id"
        :to="`/products/${p.id}`"
        class="product-card-link"
      >
        <div
          class="product-card"
        >
          <div class="card-image-container">
            <img
              :src="imageUrl(p)"
              :alt="p.name"
              @error="handleImgError($event)"
            />
          </div>
          <div class="card-content">
            <h2>{{ p.name }}</h2>
            <p>{{ p.description }}</p>
            <div class="card-actions">
              <span class="price">¥{{ p.price }}</span>
              <button class="add-to-cart-button">加入购物车</button>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const products = ref([]);
const backendBase = 'http://localhost:5000';

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

onMounted(async () => {
  try {
    const res = await fetch('/api/products');
    const data = await res.json();
    products.value = data.products;
  } catch (err) {
    console.error('获取产品失败', err);
  }
});
</script>

<style scoped>
.products-page {
  padding: 4rem 1rem;
}

.loading-indicator {
  text-align: center;
  color: #888;
}

.product-list-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}

.product-card {
  width: 320px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  overflow: hidden;
  background-color: var(--card-background);
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
}

.card-image-container {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
}

.product-card img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-content h2 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.card-content p {
  font-size: 0.875rem;
  color: #aaa;
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-actions {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.price {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 1.25rem;
}

.add-to-cart-button {
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.add-to-cart-button:hover {
  background-color: #ffab6f;
}

.products-page h1 {
    font-size: 1.875rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
}

.product-card-link {
  text-decoration: none;
  color: inherit;
  display: flex;
}
</style> 