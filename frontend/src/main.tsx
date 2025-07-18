import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { PublicClientApplication } from '@azure/msal-browser'
import { MsalProvider } from '@azure/msal-react'

import App from './App'
import { msalConfig } from './config/auth'
import { ErrorBoundary } from './components/ErrorBoundary'
import { Toaster } from 'react-hot-toast'

import './styles/globals.css'

const msalInstance = new PublicClientApplication(msalConfig)

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <MsalProvider instance={msalInstance}>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <App />
            <Toaster
              position='top-right'
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#1e293b',
                  color: '#f1f5f9',
                  border: '1px solid #334155',
                },
                success: {
                  iconTheme: {
                    primary: '#22c55e',
                    secondary: '#f1f5f9',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#f1f5f9',
                  },
                },
              }}
            />
          </BrowserRouter>
        </QueryClientProvider>
      </MsalProvider>
    </ErrorBoundary>
  </React.StrictMode>
)