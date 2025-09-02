import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // 配置 unplugin-auto-import
    AutoImport({
      resolvers: [ElementPlusResolver()],
      // 自动导入 Vue 的 ref, onMounted, reactive 等 API
      imports: ['vue'], 
    }),
    // 配置 unplugin-vue-components
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost', // 目标是 Nginx 服务
        changeOrigin: true,
      }
    }
  }
})