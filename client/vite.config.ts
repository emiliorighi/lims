import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'

export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  // import.meta.env.VITE_NAME available here with: process.env.VITE_NAME
  // import.meta.env.VITE_PORT available here with: process.env.VITE_PORT
  const basePath = env.VITE_BASE_PATH ? env.VITE_BASE_PATH + '/': undefined

  return defineConfig({
    base: basePath,
    plugins: [
      vue()],
  })
}
