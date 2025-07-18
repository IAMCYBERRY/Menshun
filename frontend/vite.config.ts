import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import checker from 'vite-plugin-checker'

export default defineConfig({
  plugins: [
    react(),
    checker({
      typescript: true,
      eslint: {
        lintCommand: 'eslint "./src/**/*.{ts,tsx}"',
      },
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@/components': resolve(__dirname, './src/components'),
      '@/pages': resolve(__dirname, './src/pages'),
      '@/hooks': resolve(__dirname, './src/hooks'),
      '@/utils': resolve(__dirname, './src/utils'),
      '@/services': resolve(__dirname, './src/services'),
      '@/types': resolve(__dirname, './src/types'),
      '@/assets': resolve(__dirname, './src/assets'),
      '@/styles': resolve(__dirname, './src/styles'),
      '@/config': resolve(__dirname, './src/config'),
      '@/contexts': resolve(__dirname, './src/contexts'),
      '@/store': resolve(__dirname, './src/store'),
    },
  },
  server: {
    port: 3000,
    host: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    target: 'es2020',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-alert-dialog', '@radix-ui/react-button', '@radix-ui/react-dialog'],
          azure: ['@azure/msal-browser', '@azure/msal-react', '@microsoft/microsoft-graph-client'],
          utils: ['axios', 'date-fns', 'zod'],
        },
      },
    },
  },
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      '@azure/msal-browser',
      '@azure/msal-react',
      '@microsoft/microsoft-graph-client',
    ],
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
  },
})