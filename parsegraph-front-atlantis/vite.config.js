import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/evapi": {
        target: "http://10.200.71.31:8890",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/evapi/, '')
      },
      "/viz_api": "https://10.200.71.31:5000"
    }
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
