import { useState, useEffect } from 'react'
import { Shield, Clock, UserCheck, AlertTriangle, Info } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface SecurityStepProps {
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
  default_value?: string
  validation_regex?: string
}

export function SecurityStep({ onComplete, completing }: SecurityStepProps) {
  const [configurations, setConfigurations] = useState<ConfigurationField[]>([])
  const [formData, setFormData] = useState<Record<string, any>>({})
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    loadConfigurations()
  }, [])

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/v1/setup/steps/security_setup/configurations')
      const data = await response.json()
      
      setConfigurations(data)
      
      // Initialize form data with existing values or defaults
      const initialData: Record<string, any> = {}
      data.forEach((config: ConfigurationField) => {
        if (config.type === 'boolean') {
          initialData[config.key] = config.value === 'true' || config.value === true || 
                                   (config.value === '' && config.default_value === 'true')
        } else {
          initialData[config.key] = config.value || config.default_value || ''
        }
      })
      setFormData(initialData)
      
    } catch (error) {
      console.error('Failed to load security configurations:', error)
      toast.error('Failed to load configuration fields')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (key: string, value: any) => {
    setFormData(prev => ({ ...prev, [key]: value }))
    
    // Clear error when user starts typing
    if (errors[key]) {
      setErrors(prev => ({ ...prev, [key]: '' }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}
    
    configurations.forEach(config => {
      const value = formData[config.key]
      
      if (config.is_required && (value === undefined || value === null || value === '')) {
        newErrors[config.key] = `${config.display_name} is required`
        return
      }
      
      if (config.type === 'integer' && value !== undefined && value !== '') {
        const numValue = parseInt(value)
        if (isNaN(numValue) || numValue <= 0) {
          newErrors[config.key] = `${config.display_name} must be a positive number`
        }
      }
    })
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const saveConfigurations = async (): Promise<boolean> => {
    try {
      const configurationData = configurations.map(config => ({
        key: config.key,
        value: formData[config.key]?.toString() || ''
      }))

      const response = await fetch('/api/v1/setup/steps/security_setup/configurations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: configurationData,
          change_reason: 'Security setup configuration'
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

      toast.success('Security configuration saved successfully')
      return true
      
    } catch (error) {
      console.error('Failed to save configurations:', error)
      toast.error('Failed to save security configuration')
      return false
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
      case 'DEFAULT_SESSION_TIMEOUT':
        return <Clock className="w-5 h-5 text-gray-400" />
      case 'REQUIRE_MFA_FOR_PRIVILEGED':
        return <UserCheck className="w-5 h-5 text-gray-400" />
      case 'MAX_ROLE_ASSIGNMENT_DURATION':
        return <Shield className="w-5 h-5 text-gray-400" />
      default:
        return <Shield className="w-5 h-5 text-gray-400" />
    }
  }

  const renderField = (config: ConfigurationField) => {
    switch (config.type) {
      case 'boolean':
        return (
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id={config.key}
              checked={formData[config.key] || false}
              onChange={(e) => handleInputChange(config.key, e.target.checked)}
              className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            />
            <label htmlFor={config.key} className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Enable {config.display_name}
            </label>
          </div>
        )
      
      case 'integer':
        return (
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {getFieldIcon(config.key)}
            </div>
            <input
              type="number"
              min="1"
              value={formData[config.key] || ''}
              onChange={(e) => handleInputChange(config.key, e.target.value)}
              className={`w-full pl-12 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                errors[config.key] ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder={config.default_value || ''}
            />
          </div>
        )
      
      default:
        return (
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {getFieldIcon(config.key)}
            </div>
            <input
              type="text"
              value={formData[config.key] || ''}
              onChange={(e) => handleInputChange(config.key, e.target.value)}
              className={`w-full pl-12 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                errors[config.key] ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder={config.default_value || ''}
            />
          </div>
        )
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading security configuration..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Security Policies Configuration
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>
            Configure the core security policies for your Menshun PAM system. These settings help ensure
            privileged access is properly controlled and monitored.
          </p>
          <div className="space-y-2">
            <p className="font-medium">Security policies include:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Session timeout controls for automatic logout</li>
              <li>Multi-factor authentication requirements</li>
              <li>Maximum duration for privileged role assignments</li>
              <li>Access control and authorization policies</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Configuration Form */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Security Policy Settings
        </h4>
        
        {configurations.map((config) => (
          <div key={config.key} className="space-y-3 p-4 border border-gray-200 dark:border-gray-600 rounded-lg">
            <div className="flex items-center space-x-2">
              {getFieldIcon(config.key)}
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {config.display_name}
                {config.is_required && <span className="text-red-500 ml-1">*</span>}
              </label>
            </div>
            
            {renderField(config)}
            
            {config.description && (
              <p className="text-xs text-gray-500 dark:text-gray-400 ml-7">
                {config.description}
              </p>
            )}
            
            {errors[config.key] && (
              <p className="text-sm text-red-600 dark:text-red-400 ml-7">
                {errors[config.key]}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Security Recommendations */}
      <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" />
          <div className="space-y-2 text-sm text-green-800 dark:text-green-200">
            <p className="font-medium">Security Best Practices:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Enable MFA for all privileged users to prevent unauthorized access</li>
              <li>Set reasonable session timeouts (15-60 minutes) based on your security requirements</li>
              <li>Limit role assignment duration to reduce the window of potential compromise</li>
              <li>Regularly review and audit these security settings</li>
              <li>Consider implementing additional authentication factors for highly privileged roles</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Current Security Summary */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Security Configuration Summary
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Session Timeout</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {formData.DEFAULT_SESSION_TIMEOUT || '30'} minutes
            </p>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <UserCheck className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">MFA Required</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {formData.REQUIRE_MFA_FOR_PRIVILEGED ? 'Yes' : 'No'}
            </p>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Max Role Duration</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {formData.MAX_ROLE_ASSIGNMENT_DURATION || '90'} days
            </p>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Security Level</span>
            </div>
            <p className="text-lg font-semibold text-green-600 dark:text-green-400">
              {formData.REQUIRE_MFA_FOR_PRIVILEGED ? 'High' : 'Standard'}
            </p>
          </div>
        </div>
      </div>

      {/* Important Security Notes */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p className="font-medium">Important Security Considerations:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Changes to security policies may require user re-authentication</li>
              <li>Shorter session timeouts improve security but may impact user experience</li>
              <li>MFA requirements apply to new logins and privileged operations</li>
              <li>These settings can be modified later in the system administration panel</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Completion Button */}
      <div className="text-center pt-6">
        <button
          onClick={handleComplete}
          disabled={completing}
          className="px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {completing ? (
            <div className="flex items-center space-x-2">
              <LoadingSpinner size="sm" />
              <span>Saving Configuration...</span>
            </div>
          ) : (
            'Continue to Compliance Setup'
          )}
        </button>
      </div>
    </div>
  )
}