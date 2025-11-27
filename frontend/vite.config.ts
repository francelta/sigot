import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiUrl = env.VITE_API_URL || 'http://localhost:8000'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      port: 3000,
      proxy: {
        // Proxy for WebSocket connections
        '/ws': {
          target: apiUrl,
          ws: true,
          changeOrigin: true,
        },
        '/api': {
          target: apiUrl,
          changeOrigin: true,
        },
      },
    },
  }
})
