import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Shield, Check, ArrowRight, ArrowLeft, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'

import { WelcomeStep } from './steps/WelcomeStep'
import { AzureSetupStep } from './steps/AzureSetupStep'
import { OrganizationStep } from './steps/OrganizationStep'
import { SecurityStep } from './steps/SecurityStep'
import { ComplianceStep } from './steps/ComplianceStep'
import { NotificationsStep } from './steps/NotificationsStep'
import { ReviewStep } from './steps/ReviewStep'
import { LoadingSpinner } from '../ui/LoadingSpinner'

interface SetupProgress {
  total_steps: number
  completed_steps: number
  completion_percentage: number
  current_step: string | null
  is_complete: boolean
  steps: Array<{
    step: string
    name: string
    description: string
    order: number
    is_completed: boolean
    is_skipped: boolean
    completion_percentage: number
  }>
}

interface SetupStatus {
  is_setup_complete: boolean
  requires_setup: boolean
  setup_progress: SetupProgress
}

const setupSteps = [
  {
    id: 'welcome',
    title: 'Welcome',
    description: 'Prerequisites & System Check',
    component: WelcomeStep,
  },
  {
    id: 'azure_setup',
    title: 'Azure AD',
    description: 'Configure Authentication',
    component: AzureSetupStep,
  },
  {
    id: 'organization_setup',
    title: 'Organization',
    description: 'Organization Details',
    component: OrganizationStep,
  },
  {
    id: 'security_setup',
    title: 'Security',
    description: 'Security Policies',
    component: SecurityStep,
  },
  {
    id: 'compliance_setup',
    title: 'Compliance',
    description: 'Compliance Frameworks',
    component: ComplianceStep,
  },
  {
    id: 'notifications_setup',
    title: 'Notifications',
    description: 'Email Configuration',
    component: NotificationsStep,
  },
  {
    id: 'review_complete',
    title: 'Complete',
    description: 'Review & Finish',
    component: ReviewStep,
  },
]

export function SetupWizard() {
  const navigate = useNavigate()
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [setupStatus, setSetupStatus] = useState<SetupStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [completing, setCompleting] = useState(false)

  useEffect(() => {
    checkSetupStatus()
  }, [])

  const checkSetupStatus = async () => {
    try {
      const response = await fetch('/api/v1/setup/status')
      const data = await response.json()
      
      setSetupStatus(data)
      
      // If setup is complete, redirect to main application
      if (data.is_setup_complete) {
        navigate('/')
        return
      }
      
      // Find current step index
      const currentStep = data.setup_progress.current_step
      if (currentStep) {
        const stepIndex = setupSteps.findIndex(step => step.id === currentStep)
        if (stepIndex !== -1) {
          setCurrentStepIndex(stepIndex)
        }
      }
    } catch (error) {
      console.error('Failed to check setup status:', error)
      toast.error('Failed to load setup status')
    } finally {
      setLoading(false)
    }
  }

  const handleStepComplete = async () => {
    const currentStep = setupSteps[currentStepIndex]
    setCompleting(true)

    try {
      // Complete the current step
      const response = await fetch(`/api/v1/setup/steps/${currentStep.id}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          completion_notes: `Completed via setup wizard`,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to complete step')
      }

      const result = await response.json()
      
      // Check if this was the final step
      if (result.overall_progress.is_complete) {
        toast.success('Setup completed successfully!')
        // Redirect to main application after a brief delay
        setTimeout(() => {
          navigate('/')
        }, 2000)
      } else {
        // Move to next step
        if (currentStepIndex < setupSteps.length - 1) {
          setCurrentStepIndex(currentStepIndex + 1)
        }
      }

      // Refresh setup status
      await checkSetupStatus()
    } catch (error) {
      console.error('Failed to complete step:', error)
      toast.error('Failed to complete setup step')
    } finally {
      setCompleting(false)
    }
  }

  const handlePreviousStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(currentStepIndex - 1)
    }
  }

  const handleSkipStep = async () => {
    // For now, just move to next step
    // TODO: Implement actual skip functionality in backend
    if (currentStepIndex < setupSteps.length - 1) {
      setCurrentStepIndex(currentStepIndex + 1)
    }
  }

  if (loading) {
    return (
      <div className='min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center'>
        <LoadingSpinner size='lg' label='Loading setup...' />
      </div>
    )
  }

  if (!setupStatus) {
    return (
      <div className='min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center'>
        <div className='text-center text-white'>
          <AlertCircle className='w-16 h-16 mx-auto mb-4 text-red-400' />
          <h2 className='text-2xl font-bold mb-2'>Setup Error</h2>
          <p className='text-gray-300 mb-4'>Failed to load setup status</p>
          <button
            onClick={checkSetupStatus}
            className='btn btn-primary'
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const currentStep = setupSteps[currentStepIndex]
  const CurrentStepComponent = currentStep.component
  const progress = ((currentStepIndex + 1) / setupSteps.length) * 100

  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900'>
      {/* Header */}
      <div className='bg-slate-800 border-b border-slate-700'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex items-center justify-between h-16'>
            <div className='flex items-center space-x-3'>
              <div className='flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-purple-600'>
                <Shield className='h-6 w-6 text-white' />
              </div>
              <div>
                <h1 className='text-xl font-bold text-white'>Menshun PAM Setup</h1>
                <p className='text-xs text-gray-400'>Enterprise Privileged Access Management</p>
              </div>
            </div>
            
            <div className='text-right'>
              <div className='text-sm text-gray-300'>
                Step {currentStepIndex + 1} of {setupSteps.length}
              </div>
              <div className='text-xs text-gray-400'>
                {Math.round(progress)}% Complete
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className='bg-slate-800'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='h-2 bg-slate-700 rounded-full overflow-hidden'>
            <motion.div
              className='h-full bg-gradient-to-r from-primary-500 to-purple-500'
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </div>

      {/* Step Navigation */}
      <div className='bg-slate-800 border-b border-slate-700'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4'>
          <div className='flex items-center justify-between overflow-x-auto'>
            {setupSteps.map((step, index) => {
              const isCompleted = setupStatus.setup_progress.steps.find(s => s.step === step.id)?.is_completed || false
              const isCurrent = index === currentStepIndex
              const isPast = index < currentStepIndex

              return (
                <div
                  key={step.id}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                    isCurrent
                      ? 'bg-primary-600 text-white'
                      : isCompleted
                      ? 'bg-green-600 text-white'
                      : isPast
                      ? 'bg-slate-600 text-gray-300'
                      : 'bg-slate-700 text-gray-400'
                  }`}
                >
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                    isCompleted ? 'bg-green-500' : isCurrent ? 'bg-primary-500' : 'bg-slate-500'
                  }`}>
                    {isCompleted ? <Check className='w-4 h-4' /> : index + 1}
                  </div>
                  <div className='text-sm font-medium whitespace-nowrap'>
                    {step.title}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className='max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <AnimatePresence mode='wait'>
          <motion.div
            key={currentStepIndex}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className='bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-8'
          >
            {/* Step Header */}
            <div className='text-center mb-8'>
              <h2 className='text-3xl font-bold text-gray-900 dark:text-white mb-2'>
                {currentStep.title}
              </h2>
              <p className='text-gray-600 dark:text-gray-400'>
                {currentStep.description}
              </p>
            </div>

            {/* Step Content */}
            <CurrentStepComponent
              onComplete={handleStepComplete}
              onNext={handleStepComplete}
              completing={completing}
            />

            {/* Navigation */}
            <div className='flex items-center justify-between mt-8 pt-6 border-t border-gray-200 dark:border-gray-700'>
              <button
                onClick={handlePreviousStep}
                disabled={currentStepIndex === 0}
                className='flex items-center space-x-2 px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed'
              >
                <ArrowLeft className='w-4 h-4' />
                <span>Previous</span>
              </button>

              <div className='flex items-center space-x-3'>
                {currentStepIndex < setupSteps.length - 1 && (
                  <button
                    onClick={handleSkipStep}
                    className='px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                  >
                    Skip
                  </button>
                )}
                
                <button
                  onClick={handleStepComplete}
                  disabled={completing}
                  className='flex items-center space-x-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed'
                >
                  {completing ? (
                    <LoadingSpinner size='sm' />
                  ) : (
                    <>
                      <span>
                        {currentStepIndex === setupSteps.length - 1 ? 'Complete Setup' : 'Continue'}
                      </span>
                      <ArrowRight className='w-4 h-4' />
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}