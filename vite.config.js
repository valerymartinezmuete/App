import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  root: './Frontend',
  server: {
    // pick a fixed port and don't silently switch if it's in use
    port: 5174,
    strictPort: true,
  },

  export default {
    build: {
      minify: "esbuild"
    }
  },


})
