import { useState, useEffect } from 'react'
import { Building, User, Mail, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface OrganizationStepProps {
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
  validation_regex?: string
}

export function OrganizationStep({ onComplete, completing }: OrganizationStepProps) {
  const [configurations, setConfigurations] = useState<ConfigurationField[]>([])
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    loadConfigurations()
  }, [])

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/v1/setup/steps/organization_setup/configurations')
      const data = await response.json()
      
      setConfigurations(data)
      
      // Initialize form data with existing values
      const initialData: Record<string, string> = {}
      data.forEach((config: ConfigurationField) => {
        initialData[config.key] = config.value || ''
      })
      setFormData(initialData)
      
    } catch (error) {
      console.error('Failed to load organization configurations:', error)
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
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}
    
    configurations.forEach(config => {
      const value = formData[config.key]
      
      if (config.is_required && (!value || value.trim() === '')) {
        newErrors[config.key] = `${config.display_name} is required`
        return
      }
      
      if (value && config.validation_regex) {
        const regex = new RegExp(config.validation_regex)
        if (!regex.test(value)) {
          if (config.key === 'ORGANIZATION_DOMAIN') {
            newErrors[config.key] = 'Please enter a valid domain (e.g., company.com)'
          } else if (config.key === 'PRIMARY_ADMINISTRATOR_EMAIL') {
            newErrors[config.key] = 'Please enter a valid email address'
          } else {
            newErrors[config.key] = `${config.display_name} format is invalid`
          }
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
        value: formData[config.key] || ''
      }))

      const response = await fetch('/api/v1/setup/steps/organization_setup/configurations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: configurationData,
          change_reason: 'Organization setup configuration'
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

      toast.success('Organization configuration saved successfully')
      return true
      
    } catch (error) {
      console.error('Failed to save configurations:', error)
      toast.error('Failed to save organization configuration')
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
      case 'ORGANIZATION_NAME':
        return <Building className="w-5 h-5 text-gray-400" />
      case 'ORGANIZATION_DOMAIN':
        return <Building className="w-5 h-5 text-gray-400" />
      case 'PRIMARY_ADMINISTRATOR_EMAIL':
        return <User className="w-5 h-5 text-gray-400" />
      default:
        return <Mail className="w-5 h-5 text-gray-400" />
    }
  }

  const allRequiredFieldsFilled = configurations
    .filter(config => config.is_required)
    .every(config => formData[config.key] && formData[config.key].trim() !== '')

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading organization configuration..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Organization Configuration
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>
            Configure your organization details that will be used throughout the Menshun PAM system.
          </p>
          <div className="space-y-2">
            <p className="font-medium">This information will be used for:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Branding and display in the user interface</li>
              <li>Email notifications and communications</li>
              <li>Audit logs and compliance reporting</li>
              <li>Administrative contact for system alerts</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Configuration Form */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Organization Details
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
                type={config.key === 'PRIMARY_ADMINISTRATOR_EMAIL' ? 'email' : 'text'}
                value={formData[config.key] || ''}
                onChange={(e) => handleInputChange(config.key, e.target.value)}
                className={`w-full pl-12 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                  errors[config.key] ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder={getPlaceholder(config.key)}
              />
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

      {/* Organization Preview */}
      {formData.ORGANIZATION_NAME && (
        <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Organization Preview
          </h4>
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-6">
            <div className="flex items-center space-x-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-purple-600">
                <Building className="h-6 w-6 text-white" />
              </div>
              <div>
                <h5 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {formData.ORGANIZATION_NAME}
                </h5>
                {formData.ORGANIZATION_DOMAIN && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {formData.ORGANIZATION_DOMAIN}
                  </p>
                )}
                {formData.PRIMARY_ADMINISTRATOR_EMAIL && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Administrator: {formData.PRIMARY_ADMINISTRATOR_EMAIL}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Important Notes */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p className="font-medium">Important Notes:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>The organization domain should match your Azure AD tenant domain</li>
              <li>The primary administrator email will receive important system notifications</li>
              <li>This information can be updated later in the system settings</li>
              <li>The administrator email should be accessible and monitored regularly</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Completion Button */}
      <div className="text-center pt-6">
        <button
          onClick={handleComplete}
          disabled={completing || !allRequiredFieldsFilled}
          className="px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {completing ? (
            <div className="flex items-center space-x-2">
              <LoadingSpinner size="sm" />
              <span>Saving Configuration...</span>
            </div>
          ) : (
            'Continue to Security Setup'
          )}
        </button>
        
        {!allRequiredFieldsFilled && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Please fill in all required fields to continue
          </p>
        )}
      </div>
    </div>
  )
}

function getPlaceholder(key: string): string {
  switch (key) {
    case 'ORGANIZATION_NAME':
      return 'Acme Corporation'
    case 'ORGANIZATION_DOMAIN':
      return 'acme.com'
    case 'PRIMARY_ADMINISTRATOR_EMAIL':
      return 'admin@acme.com'
    default:
      return ''
  }
}