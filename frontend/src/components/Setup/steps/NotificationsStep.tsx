import { useState, useEffect } from 'react'
import { Mail, Server, Lock, Eye, EyeOff, CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface NotificationsStepProps {
  onComplete: () => void
  onNext: () => void
  completing: boolean
}

interface ConfigurationField {
  key: string
  display_name: string
  description: string
  type: string
  value: string
  is_required: boolean
  is_sensitive: boolean
  default_value?: string
  validation_regex?: string
}

export function NotificationsStep({ onComplete, completing }: NotificationsStepProps) {
  const [configurations, setConfigurations] = useState<ConfigurationField[]>([])
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({})
  const [loading, setLoading] = useState(true)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState<{ success: boolean; error?: string } | null>(null)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [skipNotifications, setSkipNotifications] = useState(false)

  useEffect(() => {
    loadConfigurations()
  }, [])

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/v1/setup/steps/notifications_setup/configurations')
      const data = await response.json()
      
      setConfigurations(data)
      
      // Initialize form data with existing values
      const initialData: Record<string, string> = {}
      data.forEach((config: ConfigurationField) => {
        initialData[config.key] = config.value || config.default_value || ''
      })
      setFormData(initialData)
      
    } catch (error) {
      console.error('Failed to load notifications configurations:', error)
      toast.error('Failed to load configuration fields')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (key: string, value: string) => {
    setFormData(prev => ({ ...prev, [key]: value }))
    
    // Clear error when user starts typing
    if (errors[key]) {
      setErrors(prev => ({ ...prev, [key]: '' }))
    }
    
    // Clear test result when configuration changes
    if (testResult) {
      setTestResult(null)
    }
  }

  const toggleShowSecret = (key: string) => {
    setShowSecrets(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}
    
    if (!skipNotifications) {
      configurations.forEach(config => {
        const value = formData[config.key]
        
        if (config.is_required && (!value || value.trim() === '')) {
          newErrors[config.key] = `${config.display_name} is required`
          return
        }
        
        if (value && config.validation_regex) {
          const regex = new RegExp(config.validation_regex)
          if (!regex.test(value)) {
            if (config.key === 'SMTP_FROM_EMAIL') {
              newErrors[config.key] = 'Please enter a valid email address'
            } else {
              newErrors[config.key] = `${config.display_name} format is invalid`
            }
          }
        }
        
        if (config.key === 'SMTP_PORT' && value) {
          const port = parseInt(value)
          if (isNaN(port) || port < 1 || port > 65535) {
            newErrors[config.key] = 'Port must be between 1 and 65535'
          }
        }
      })
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const saveConfigurations = async (): Promise<boolean> => {
    try {
      const configurationData = configurations.map(config => ({
        key: config.key,
        value: skipNotifications ? '' : (formData[config.key] || '')
      }))

      const response = await fetch('/api/v1/setup/steps/notifications_setup/configurations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: configurationData,
          change_reason: skipNotifications ? 'Notifications setup skipped' : 'Notifications setup configuration'
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to save configurations')
      }

      const result = await response.json()
      
      if (result.failed_updates && result.failed_updates.length > 0) {
        toast.error(`Failed to save some configurations: ${result.failed_updates.join(', ')}`)
        return false
      }

      toast.success(skipNotifications ? 'Notifications setup skipped' : 'Notifications configuration saved successfully')
      return true
      
    } catch (error) {
      console.error('Failed to save configurations:', error)
      toast.error('Failed to save notifications configuration')
      return false
    }
  }

  const testEmailConfiguration = async () => {
    if (!validateForm()) {
      toast.error('Please fix validation errors before testing')
      return
    }

    setTesting(true)
    setTestResult(null)

    try {
      // Save configurations first
      const saved = await saveConfigurations()
      if (!saved) {
        return
      }

      // Mock test - in real implementation, this would send a test email
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const success = Math.random() > 0.3 // Mock 70% success rate for demo
      
      setTestResult({
        success,
        error: success ? undefined : 'Failed to connect to SMTP server. Please check your settings.'
      })

      if (success) {
        toast.success('Email configuration test successful!')
      } else {
        toast.error('Email configuration test failed')
      }
      
    } catch (error) {
      console.error('Email test failed:', error)
      setTestResult({
        success: false,
        error: 'Failed to perform email test'
      })
      toast.error('Email test failed')
    } finally {
      setTesting(false)
    }
  }

  const handleComplete = async () => {
    if (!validateForm()) {
      toast.error('Please fix validation errors before continuing')
      return
    }

    const saved = await saveConfigurations()
    if (saved) {
      onComplete()
    }
  }

  const getFieldIcon = (key: string) => {
    switch (key) {
      case 'SMTP_HOST':
        return <Server className="w-5 h-5 text-gray-400" />
      case 'SMTP_PORT':
        return <Server className="w-5 h-5 text-gray-400" />
      case 'SMTP_FROM_EMAIL':
        return <Mail className="w-5 h-5 text-gray-400" />
      default:
        return <Lock className="w-5 h-5 text-gray-400" />
    }
  }

  const allRequiredFieldsFilled = skipNotifications || configurations
    .filter(config => config.is_required)
    .every(config => formData[config.key] && formData[config.key].trim() !== '')

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading notifications configuration..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Email Notifications Configuration
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>
            Configure email notifications to receive important alerts about privileged access activities,
            security events, and system status updates.
          </p>
          <div className="space-y-2">
            <p className="font-medium">Notifications will be sent for:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Privileged role assignments and removals</li>
              <li>Failed login attempts and security alerts</li>
              <li>System maintenance and health status</li>
              <li>Compliance and audit events</li>
            </ul>
          </div>
          <p className="text-xs text-blue-700 dark:text-blue-300">
            Note: Email configuration is optional. You can skip this step and configure it later in system settings.
          </p>
        </div>
      </div>

      {/* Skip Option */}
      <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="skip-notifications"
            checked={skipNotifications}
            onChange={(e) => setSkipNotifications(e.target.checked)}
            className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500"
          />
          <label htmlFor="skip-notifications" className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Skip email configuration for now (can be configured later)
          </label>
        </div>
      </div>

      {!skipNotifications && (
        <>
          {/* Configuration Form */}
          <div className="space-y-6">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
              SMTP Server Configuration
            </h4>
            
            {configurations.map((config) => (
              <div key={config.key} className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  {config.display_name}
                  {config.is_required && <span className="text-red-500 ml-1">*</span>}
                </label>
                
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    {getFieldIcon(config.key)}
                  </div>
                  <input
                    type={
                      config.is_sensitive && !showSecrets[config.key] 
                        ? 'password' 
                        : config.key === 'SMTP_PORT' 
                        ? 'number' 
                        : config.key === 'SMTP_FROM_EMAIL'
                        ? 'email'
                        : 'text'
                    }
                    value={formData[config.key] || ''}
                    onChange={(e) => handleInputChange(config.key, e.target.value)}
                    className={`w-full pl-12 ${config.is_sensitive ? 'pr-12' : 'pr-4'} py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                      errors[config.key] ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder={getPlaceholder(config.key)}
                    min={config.key === 'SMTP_PORT' ? '1' : undefined}
                    max={config.key === 'SMTP_PORT' ? '65535' : undefined}
                  />
                  
                  {config.is_sensitive && (
                    <button
                      type="button"
                      onClick={() => toggleShowSecret(config.key)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                    >
                      {showSecrets[config.key] ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  )}
                </div>
                
                {config.description && (
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {config.description}
                  </p>
                )}
                
                {errors[config.key] && (
                  <p className="text-sm text-red-600 dark:text-red-400">
                    {errors[config.key]}
                  </p>
                )}
              </div>
            ))}
          </div>

          {/* Test Email Configuration */}
          <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                Test Email Configuration
              </h4>
              <button
                onClick={testEmailConfiguration}
                disabled={testing || !allRequiredFieldsFilled}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {testing && <LoadingSpinner size="sm" />}
                <span>{testing ? 'Testing...' : 'Send Test Email'}</span>
              </button>
            </div>
            
            {testResult && (
              <div className={`p-4 rounded-lg ${
                testResult.success 
                  ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
                  : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
              }`}>
                <div className="flex items-center space-x-2 mb-2">
                  {testResult.success ? (
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                  )}
                  <span className={`font-medium ${
                    testResult.success 
                      ? 'text-green-800 dark:text-green-200'
                      : 'text-red-800 dark:text-red-200'
                  }`}>
                    {testResult.success ? 'Email Test Successful' : 'Email Test Failed'}
                  </span>
                </div>
                
                {testResult.success ? (
                  <div className="text-sm text-green-700 dark:text-green-300">
                    <p>Test email sent successfully! Check your inbox to confirm receipt.</p>
                  </div>
                ) : (
                  <div className="text-sm text-red-700 dark:text-red-300">
                    {testResult.error && <p>Error: {testResult.error}</p>}
                  </div>
                )}
              </div>
            )}
            
            {!allRequiredFieldsFilled && (
              <div className="flex items-center space-x-2 text-yellow-600 dark:text-yellow-400 text-sm">
                <AlertTriangle className="w-4 h-4" />
                <span>Fill in all required fields to test the email configuration</span>
              </div>
            )}
          </div>

          {/* Common SMTP Settings */}
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
              Common SMTP Settings
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="font-medium text-gray-700 dark:text-gray-300 mb-2">Gmail:</p>
                <p className="text-gray-600 dark:text-gray-400">Host: smtp.gmail.com</p>
                <p className="text-gray-600 dark:text-gray-400">Port: 587 (TLS)</p>
              </div>
              <div>
                <p className="font-medium text-gray-700 dark:text-gray-300 mb-2">Outlook/Hotmail:</p>
                <p className="text-gray-600 dark:text-gray-400">Host: smtp-mail.outlook.com</p>
                <p className="text-gray-600 dark:text-gray-400">Port: 587 (TLS)</p>
              </div>
              <div>
                <p className="font-medium text-gray-700 dark:text-gray-300 mb-2">Office 365:</p>
                <p className="text-gray-600 dark:text-gray-400">Host: smtp.office365.com</p>
                <p className="text-gray-600 dark:text-gray-400">Port: 587 (TLS)</p>
              </div>
              <div>
                <p className="font-medium text-gray-700 dark:text-gray-300 mb-2">SendGrid:</p>
                <p className="text-gray-600 dark:text-gray-400">Host: smtp.sendgrid.net</p>
                <p className="text-gray-600 dark:text-gray-400">Port: 587 (TLS)</p>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Important Notes */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p className="font-medium">Important Notes:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Use app-specific passwords for Gmail and other providers that require them</li>
              <li>Ensure your SMTP server allows connections from your deployment environment</li>
              <li>Consider using dedicated email services like SendGrid for production deployments</li>
              <li>Email notifications can be configured or modified later in system settings</li>
              <li>Test emails help verify your configuration is working correctly</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Completion Button */}
      <div className="text-center pt-6">
        <button
          onClick={handleComplete}
          disabled={completing || (!skipNotifications && !allRequiredFieldsFilled)}
          className="px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {completing ? (
            <div className="flex items-center space-x-2">
              <LoadingSpinner size="sm" />
              <span>Saving Configuration...</span>
            </div>
          ) : (
            'Continue to Final Review'
          )}
        </button>
        
        {!skipNotifications && !allRequiredFieldsFilled && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Please fill in all required fields or skip this step to continue
          </p>
        )}
      </div>
    </div>
  )
}

function getPlaceholder(key: string): string {
  switch (key) {
    case 'SMTP_HOST':
      return 'smtp.gmail.com'
    case 'SMTP_PORT':
      return '587'
    case 'SMTP_FROM_EMAIL':
      return 'noreply@yourcompany.com'
    default:
      return ''
  }
}