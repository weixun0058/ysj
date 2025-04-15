<script setup>
// 导入所有创建的组件
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
</script>

<template>
  <div id="app-layout">
    <AppHeader />
    <main>
      <!-- 路由匹配的组件将在这里渲染 -->
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<style scoped>
/* App.vue 的特定样式，如果需要的话 */
#app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1; /* 让 main 部分占据剩余空间 */
}

/* 之前的 section[id] 样式已移除，滚动由 router 处理 */

</style>
