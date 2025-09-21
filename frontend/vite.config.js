import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Detectar si estamos en desarrollo o producción
  const isDevelopment = mode === 'development'
  
  return {
    plugins: [react()],
    server: {
      port: 5178
    },
    define: {
      // Define environment variables at build time
      'import.meta.env.VITE_API_URL': JSON.stringify(
        process.env.VITE_API_URL || 
        (isDevelopment ? 'http://localhost:5000/api' : 'https://emailmanageriatesting.onrender.com/api')
      )
    }
  }
})
