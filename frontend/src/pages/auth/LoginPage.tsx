import { useMsal } from '@azure/msal-react'
import { Shield, ArrowRight, Eye, Lock, Users } from 'lucide-react'
import { loginRequest } from '@/config/auth'

export function LoginPage() {
  const { instance } = useMsal()

  const handleLogin = () => {
    instance.loginRedirect(loginRequest)
  }

  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex'>
      {/* Left side - Branding */}
      <div className='hidden lg:flex lg:w-1/2 items-center justify-center p-12'>
        <div className='max-w-md text-center'>
          <div className='flex items-center justify-center mb-8'>
            <div className='flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 shadow-glow-primary'>
              <Shield className='h-12 w-12 text-white' />
            </div>
          </div>
          
          <h1 className='text-4xl font-bold text-white mb-4 font-display'>
            Menshun
          </h1>
          
          <p className='text-xl text-gray-300 mb-8 leading-relaxed'>
            Enterprise Privileged Access Management for Microsoft Entra ID
          </p>
          
          <div className='space-y-4 text-left'>
            <div className='flex items-center text-gray-300'>
              <Eye className='h-5 w-5 mr-3 text-primary-400' />
              <span>Monitor privileged access in real-time</span>
            </div>
            <div className='flex items-center text-gray-300'>
              <Lock className='h-5 w-5 mr-3 text-primary-400' />
              <span>Secure credential management & rotation</span>
            </div>
            <div className='flex items-center text-gray-300'>
              <Users className='h-5 w-5 mr-3 text-primary-400' />
              <span>Comprehensive user lifecycle management</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - Login */}
      <div className='flex-1 flex items-center justify-center p-8'>
        <div className='w-full max-w-md'>
          <div className='bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8'>
            {/* Mobile logo */}
            <div className='lg:hidden flex items-center justify-center mb-8'>
              <div className='flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-purple-600'>
                <Shield className='h-8 w-8 text-white' />
              </div>
              <div className='ml-3'>
                <h1 className='text-2xl font-bold text-gray-900 dark:text-white'>Menshun</h1>
                <p className='text-sm text-gray-500 dark:text-gray-400'>Enterprise PAM</p>
              </div>
            </div>

            <div className='text-center mb-8'>
              <h2 className='text-2xl font-bold text-gray-900 dark:text-white mb-2'>
                Welcome Back
              </h2>
              <p className='text-gray-600 dark:text-gray-400'>
                Sign in with your Microsoft account to continue
              </p>
            </div>

            <button
              onClick={handleLogin}
              className='w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200 shadow-glow-primary hover:shadow-glow-primary'
            >
              <svg className='w-5 h-5 mr-2' viewBox='0 0 23 23'>
                <path
                  fill='currentColor'
                  d='M11.5 0L0 8.5v6L11.5 23L23 14.5v-6L11.5 0z'
                />
              </svg>
              Sign in with Microsoft
              <ArrowRight className='ml-2 h-5 w-5' />
            </button>

            <div className='mt-6 text-center'>
              <p className='text-xs text-gray-500 dark:text-gray-400'>
                By signing in, you agree to our{' '}
                <a href='#' className='text-primary-600 hover:text-primary-500'>
                  Terms of Service
                </a>{' '}
                and{' '}
                <a href='#' className='text-primary-600 hover:text-primary-500'>
                  Privacy Policy
                </a>
              </p>
            </div>
          </div>

          {/* Features for mobile */}
          <div className='lg:hidden mt-8 text-center space-y-3'>
            <div className='flex items-center justify-center text-gray-300'>
              <Eye className='h-4 w-4 mr-2 text-primary-400' />
              <span className='text-sm'>Monitor privileged access</span>
            </div>
            <div className='flex items-center justify-center text-gray-300'>
              <Lock className='h-4 w-4 mr-2 text-primary-400' />
              <span className='text-sm'>Secure credential management</span>
            </div>
            <div className='flex items-center justify-center text-gray-300'>
              <Users className='h-4 w-4 mr-2 text-primary-400' />
              <span className='text-sm'>User lifecycle management</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}