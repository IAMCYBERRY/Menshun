import { clsx } from 'clsx'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
  label?: string
}

export function LoadingSpinner({ size = 'md', className, label = 'Loading...' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  }

  return (
    <div className={clsx('flex items-center justify-center', className)}>
      <div className='flex items-center space-x-2'>
        <div
          className={clsx(
            'animate-spin rounded-full border-2 border-gray-300 border-t-primary-600',
            sizeClasses[size]
          )}
          role='status'
          aria-label={label}
        />
        {label && <span className='text-sm text-gray-600 dark:text-gray-400'>{label}</span>}
      </div>
    </div>
  )
}