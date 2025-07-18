import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  Bot,
  Key,
  Shield,
  FileText,
  Settings,
  Crown,
  AlertTriangle,
} from 'lucide-react'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Privileged Users', href: '/users', icon: Users },
  { name: 'Service Identities', href: '/service-identities', icon: Bot },
  { name: 'Credentials', href: '/credentials', icon: Key },
  { name: 'Role Assignments', href: '/role-assignments', icon: Crown },
  { name: 'Audit Logs', href: '/audit', icon: FileText },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <div className='fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg border-r border-gray-200 dark:border-gray-700 lg:block hidden'>
      {/* Logo */}
      <div className='flex h-16 items-center justify-center border-b border-gray-200 dark:border-gray-700'>
        <div className='flex items-center space-x-3'>
          <div className='flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-primary-600 to-purple-600'>
            <Shield className='h-6 w-6 text-white' />
          </div>
          <div>
            <h1 className='text-xl font-bold text-gray-900 dark:text-white'>Menshun</h1>
            <p className='text-xs text-gray-500 dark:text-gray-400'>Enterprise PAM</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className='mt-6 px-3'>
        <div className='space-y-1'>
          {navigation.map(item => {
            const isActive = location.pathname === item.href || 
              (item.href !== '/' && location.pathname.startsWith(item.href))

            return (
              <NavLink
                key={item.name}
                to={item.href}
                className={clsx(
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'
                )}
              >
                <item.icon
                  className={clsx(
                    'mr-3 h-5 w-5 flex-shrink-0',
                    isActive
                      ? 'text-primary-600 dark:text-primary-400'
                      : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                  )}
                />
                {item.name}
              </NavLink>
            )
          })}
        </div>

        {/* Risk Indicator Section */}
        <div className='mt-8 px-3'>
          <h3 className='text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider'>
            Risk Overview
          </h3>
          <div className='mt-3 space-y-2'>
            <div className='flex items-center justify-between p-2 rounded-md bg-red-50 dark:bg-red-900/20'>
              <div className='flex items-center'>
                <AlertTriangle className='h-4 w-4 text-red-500 mr-2' />
                <span className='text-sm text-red-700 dark:text-red-400'>Critical</span>
              </div>
              <span className='text-sm font-medium text-red-800 dark:text-red-300'>2</span>
            </div>
            
            <div className='flex items-center justify-between p-2 rounded-md bg-yellow-50 dark:bg-yellow-900/20'>
              <div className='flex items-center'>
                <div className='h-2 w-2 rounded-full bg-yellow-500 mr-2' />
                <span className='text-sm text-yellow-700 dark:text-yellow-400'>High</span>
              </div>
              <span className='text-sm font-medium text-yellow-800 dark:text-yellow-300'>8</span>
            </div>
            
            <div className='flex items-center justify-between p-2 rounded-md bg-blue-50 dark:bg-blue-900/20'>
              <div className='flex items-center'>
                <div className='h-2 w-2 rounded-full bg-blue-500 mr-2' />
                <span className='text-sm text-blue-700 dark:text-blue-400'>Medium</span>
              </div>
              <span className='text-sm font-medium text-blue-800 dark:text-blue-300'>24</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className='mt-8 px-3'>
          <h3 className='text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider'>
            Quick Actions
          </h3>
          <div className='mt-3 space-y-1'>
            <button className='w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors'>
              Create Privileged User
            </button>
            <button className='w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors'>
              Assign Role
            </button>
            <button className='w-full text-left px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors'>
              Rotate Credentials
            </button>
          </div>
        </div>
      </nav>

      {/* Bottom section */}
      <div className='absolute bottom-0 w-full p-4 border-t border-gray-200 dark:border-gray-700'>
        <div className='text-xs text-gray-500 dark:text-gray-400 text-center'>
          v1.0.0 • Solo Leveling Theme
        </div>
      </div>
    </div>
  )
}