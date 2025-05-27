import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    allowedHosts: [
      '11093329-8fd6-410d-bc09-2b0453e240ba-00-1wrm24z62h2qu.worf.replit.dev',
      'localhost',
      '127.0.0.1'
    ]
  }
})