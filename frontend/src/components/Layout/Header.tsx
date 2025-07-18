import { useState } from 'react'
import { Menu, Bell, Search, Moon, Sun, User, LogOut, Settings } from 'lucide-react'
import { useMsal } from '@azure/msal-react'
import { clsx } from 'clsx'

export function Header() {
  const { instance, accounts } = useMsal()
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)

  const currentUser = accounts[0]

  const handleLogout = () => {
    instance.logoutRedirect()
  }

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <header className='bg-white dark:bg-gray-800 shadow border-b border-gray-200 dark:border-gray-700'>
      <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
        <div className='flex h-16 justify-between items-center'>
          {/* Mobile menu button */}
          <div className='flex items-center lg:hidden'>
            <button
              type='button'
              className='inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
            >
              <Menu className='h-6 w-6' />
            </button>
          </div>

          {/* Search */}
          <div className='flex flex-1 items-center justify-center px-2 lg:ml-6 lg:justify-start'>
            <div className='w-full max-w-lg lg:max-w-xs'>
              <label htmlFor='search' className='sr-only'>
                Search
              </label>
              <div className='relative'>
                <div className='pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3'>
                  <Search className='h-5 w-5 text-gray-400' />
                </div>
                <input
                  id='search'
                  name='search'
                  className='block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 pl-10 pr-3 text-sm placeholder-gray-500 dark:placeholder-gray-400 focus:border-primary-500 focus:text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-primary-500'
                  placeholder='Search users, roles, identities...'
                  type='search'
                />
              </div>
            </div>
          </div>

          {/* Right side */}
          <div className='flex items-center space-x-4'>
            {/* Theme toggle */}
            <button
              onClick={toggleDarkMode}
              className='rounded-md p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
            >
              {isDarkMode ? <Sun className='h-5 w-5' /> : <Moon className='h-5 w-5' />}
            </button>

            {/* Notifications */}
            <button
              type='button'
              className='relative rounded-md p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
            >
              <Bell className='h-5 w-5' />
              <span className='absolute -top-0.5 -right-0.5 h-4 w-4 rounded-full bg-red-500 text-xs text-white flex items-center justify-center'>
                3
              </span>
            </button>

            {/* User menu */}
            <div className='relative'>
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className='flex items-center rounded-md p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
              >
                <div className='flex items-center space-x-2'>
                  <div className='h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center'>
                    <User className='h-5 w-5 text-white' />
                  </div>
                  <div className='hidden md:block text-left'>
                    <div className='text-sm font-medium text-gray-900 dark:text-gray-100'>
                      {currentUser?.name || 'User'}
                    </div>
                    <div className='text-xs text-gray-500 dark:text-gray-400'>
                      {currentUser?.username || 'user@domain.com'}
                    </div>
                  </div>
                </div>
              </button>

              {/* User dropdown */}
              {showUserMenu && (
                <div className='absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white dark:bg-gray-800 py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none'>
                  <div className='px-4 py-2 border-b border-gray-200 dark:border-gray-700'>
                    <div className='text-sm font-medium text-gray-900 dark:text-gray-100'>
                      {currentUser?.name || 'User'}
                    </div>
                    <div className='text-xs text-gray-500 dark:text-gray-400'>
                      {currentUser?.username || 'user@domain.com'}
                    </div>
                  </div>
                  
                  <button
                    className='flex w-full items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    onClick={() => setShowUserMenu(false)}
                  >
                    <User className='mr-3 h-4 w-4' />
                    Profile
                  </button>
                  
                  <button
                    className='flex w-full items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    onClick={() => setShowUserMenu(false)}
                  >
                    <Settings className='mr-3 h-4 w-4' />
                    Settings
                  </button>
                  
                  <button
                    onClick={handleLogout}
                    className='flex w-full items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  >
                    <LogOut className='mr-3 h-4 w-4' />
                    Sign out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}