<!-- 页脚 --> 
<template>
  <footer class="app-footer">
    <div class="container">
      <p>&copy; 2025 塞外本草 / 壹世健 保留所有权利.</p>
      <p>公司地址：新疆伊犁尼勒克地区 | 联系电话：XXX-XXXXXXX | 邮箱：contact@yishijian.com</p>
      <p>
        备案号：<a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">京ICP备XXXXXXXX号-X</a>
        <!-- 添加其他链接 -->
        | <a href="#privacy">隐私政策</a>
        | <a href="#terms">服务条款</a>
      </p>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.app-footer {
  background-color: #111; /* 页脚用更深的黑色 */
  color: var(--text-color-light);
  opacity: 0.7;
  padding: 2rem 0;
  margin-top: 4rem; /* 与上方内容留出距离 */
  text-align: center;
  font-size: 0.9em;
  border-top: 1px solid var(--border-color);
}

.app-footer p {
  margin: 0.5rem 0;
}

.app-footer a {
  color: var(--text-color-light);
  text-decoration: none;
}

.app-footer a:hover {
  color: var(--primary-color);
}

/* 响应式调整 */
@media (max-width: 960px) {
  .app-footer {
    padding: 1.5rem 1rem; /* 减少内边距 */
    font-size: 0.8em; /* 缩小字体 */
    margin-top: 2rem; /* 减少与上方距离 */
  }
  .app-footer p {
      line-height: 1.6; /* 调整行高避免文字太挤 */
  }
}
</style> 