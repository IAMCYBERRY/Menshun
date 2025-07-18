import React, { Component, ErrorInfo, ReactNode } from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
  errorInfo?: ErrorInfo
}

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ error, errorInfo })
    
    // Log error to monitoring service
    console.error('Error Boundary caught an error:', error, errorInfo)
    
    // In a real app, you would send this to your error reporting service
    // Example: Sentry.captureException(error, { extra: errorInfo })
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className='min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4'>
          <div className='max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6'>
            <div className='flex items-center justify-center w-12 h-12 mx-auto bg-red-100 dark:bg-red-900 rounded-full mb-4'>
              <AlertTriangle className='w-6 h-6 text-red-600 dark:text-red-400' />
            </div>
            
            <div className='text-center'>
              <h1 className='text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2'>
                Something went wrong
              </h1>
              
              <p className='text-gray-600 dark:text-gray-400 mb-6'>
                We encountered an unexpected error. Please try refreshing the page or contact support if the problem persists.
              </p>
              
              <div className='space-y-3'>
                <button
                  onClick={this.handleRetry}
                  className='w-full inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                >
                  <RefreshCw className='w-4 h-4 mr-2' />
                  Try Again
                </button>
                
                <button
                  onClick={() => window.location.reload()}
                  className='w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                >
                  Refresh Page
                </button>
              </div>
              
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className='mt-6 text-left'>
                  <summary className='cursor-pointer text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'>
                    Error Details (Development Only)
                  </summary>
                  <div className='mt-2 p-3 bg-gray-100 dark:bg-gray-700 rounded text-xs font-mono text-gray-800 dark:text-gray-200 overflow-auto max-h-40'>
                    <div className='mb-2'>
                      <strong>Error:</strong> {this.state.error.message}
                    </div>
                    <div className='mb-2'>
                      <strong>Stack:</strong>
                      <pre className='whitespace-pre-wrap'>{this.state.error.stack}</pre>
                    </div>
                    {this.state.errorInfo && (
                      <div>
                        <strong>Component Stack:</strong>
                        <pre className='whitespace-pre-wrap'>{this.state.errorInfo.componentStack}</pre>
                      </div>
                    )}
                  </div>
                </details>
              )}
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}