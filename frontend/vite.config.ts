import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { TanStackRouterVite } from '@tanstack/router-vite-plugin'

export default defineConfig({
  define: {
    global: "window",
  },
  plugins: [
    react(),
    TanStackRouterVite(),
  ],
})
