import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  appType: 'spa',
  optimizeDeps: {
    include: ['@fortawesome/free-solid-svg-icons'],
  },
  plugins: [vue()],
  server: {
    port: 5678,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    }
  }
})
