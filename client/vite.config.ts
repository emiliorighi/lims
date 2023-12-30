import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'

export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  // import.meta.env.VITE_NAME available here with: process.env.VITE_NAME
  // import.meta.env.VITE_PORT available here with: process.env.VITE_PORT

  return defineConfig({
    base: env.VITE_BASE_PATH ? env.VITE_BASE_PATH : '/',
    plugins: [
      vue()],
  })
}
