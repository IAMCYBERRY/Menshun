import { Link } from 'react-router-dom'
import { Home, ArrowLeft } from 'lucide-react'

export function NotFoundPage() {
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4'>
      <div className='max-w-md w-full text-center'>
        <div className='mb-8'>
          <h1 className='text-9xl font-bold text-gray-300 dark:text-gray-700'>404</h1>
        </div>
        
        <h2 className='text-2xl font-bold text-gray-900 dark:text-white mb-2'>Page not found</h2>
        
        <p className='text-gray-600 dark:text-gray-400 mb-8'>
          Sorry, we couldn't find the page you're looking for.
        </p>
        
        <div className='space-y-3'>
          <Link
            to='/'
            className='w-full inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
          >
            <Home className='w-4 h-4 mr-2' />
            Go to Dashboard
          </Link>
          
          <button
            onClick={() => window.history.back()}
            className='w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
          >
            <ArrowLeft className='w-4 h-4 mr-2' />
            Go Back
          </button>
        </div>
      </div>
    </div>
  )
}