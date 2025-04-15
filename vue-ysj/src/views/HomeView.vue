<script setup>
// 导入之前在 App.vue 中使用的主页组件
import HeroSection from '../components/HeroSection.vue';
import FeaturesSection from '../components/FeaturesSection.vue';
import ProductsSection from '../components/ProductsSection.vue';
import EntryPointsSection from '../components/EntryPointsSection.vue';
</script>

<template>
  <div>
    <HeroSection />
    <FeaturesSection id="features" />
    <ProductsSection id="products" />
    <EntryPointsSection id="explore" />
     <!-- 未来可能还会有其他主页特定的区块 -->
  </div>
</template>

<style scoped>
/* HomeView 的特定样式 */
/* 可以为每个 section 添加滚动边距，如果需要 Header 不遮挡锚点链接 */
section[id] {
  scroll-margin-top: 80px; /* 根据 Header 高度调整 */
}
</style> 