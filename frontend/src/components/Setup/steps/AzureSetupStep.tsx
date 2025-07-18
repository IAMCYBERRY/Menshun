import { useState, useEffect } from 'react'
import { Eye, EyeOff, CheckCircle, XCircle, ExternalLink, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface AzureSetupStepProps {
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
  validation_regex?: string
}

interface TestResult {
  success: boolean
  error?: string
  tenant_info?: {
    tenant_id: string
    verified: boolean
  }
  missing_fields?: string[]
}

export function AzureSetupStep({ onComplete, completing }: AzureSetupStepProps) {
  const [configurations, setConfigurations] = useState<ConfigurationField[]>([])
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({})
  const [loading, setLoading] = useState(true)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState<TestResult | null>(null)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    loadConfigurations()
  }, [])

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/v1/setup/steps/azure_setup/configurations')
      const data = await response.json()
      
      setConfigurations(data)
      
      // Initialize form data with existing values
      const initialData: Record<string, string> = {}
      data.forEach((config: ConfigurationField) => {
        initialData[config.key] = config.value || ''
      })
      setFormData(initialData)
      
    } catch (error) {
      console.error('Failed to load Azure configurations:', error)
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
    
    configurations.forEach(config => {
      const value = formData[config.key]
      
      if (config.is_required && (!value || value.trim() === '')) {
        newErrors[config.key] = `${config.display_name} is required`
        return
      }
      
      if (value && config.validation_regex) {
        const regex = new RegExp(config.validation_regex)
        if (!regex.test(value)) {
          if (config.key.includes('ID')) {
            newErrors[config.key] = `${config.display_name} must be a valid GUID`
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

      const response = await fetch('/api/v1/setup/steps/azure_setup/configurations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: configurationData,
          change_reason: 'Azure AD setup configuration'
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

      toast.success('Azure AD configuration saved successfully')
      return true
      
    } catch (error) {
      console.error('Failed to save configurations:', error)
      toast.error('Failed to save Azure AD configuration')
      return false
    }
  }

  const testConnection = async () => {
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

      // Test the connection
      const response = await fetch('/api/v1/setup/test-azure-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      const result = await response.json()
      setTestResult(result)

      if (result.success) {
        toast.success('Azure AD connection test successful!')
      } else {
        toast.error(`Connection test failed: ${result.error}`)
      }
      
    } catch (error) {
      console.error('Connection test failed:', error)
      setTestResult({
        success: false,
        error: 'Failed to perform connection test'
      })
      toast.error('Connection test failed')
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

  const allRequiredFieldsFilled = configurations
    .filter(config => config.is_required)
    .every(config => formData[config.key] && formData[config.key].trim() !== '')

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading Azure AD configuration..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Azure AD App Registration Required
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>
            To integrate with Microsoft Entra ID (Azure AD), you need to create an app registration in the Azure portal.
          </p>
          <div className="space-y-2">
            <p className="font-medium">Required permissions for your app registration:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Directory.Read.All (to read directory information)</li>
              <li>User.Read.All (to read user profiles)</li>
              <li>RoleManagement.ReadWrite.Directory (to manage role assignments)</li>
              <li>Application.ReadWrite.All (for service principal management)</li>
            </ul>
          </div>
          <div className="flex items-center space-x-2 mt-4">
            <ExternalLink className="w-4 h-4" />
            <a
              href="https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Open Azure App Registrations
            </a>
          </div>
        </div>
      </div>

      {/* Configuration Form */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Azure AD Configuration
        </h4>
        
        {configurations.map((config) => (
          <div key={config.key} className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              {config.display_name}
              {config.is_required && <span className="text-red-500 ml-1">*</span>}
            </label>
            
            <div className="relative">
              <input
                type={config.is_sensitive && !showSecrets[config.key] ? 'password' : 'text'}
                value={formData[config.key] || ''}
                onChange={(e) => handleInputChange(config.key, e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                  errors[config.key] ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder={config.description}
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

      {/* Test Connection */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
            Test Connection
          </h4>
          <button
            onClick={testConnection}
            disabled={testing || !allRequiredFieldsFilled}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {testing && <LoadingSpinner size="sm" />}
            <span>{testing ? 'Testing...' : 'Test Connection'}</span>
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
                {testResult.success ? 'Connection Successful' : 'Connection Failed'}
              </span>
            </div>
            
            {testResult.success && testResult.tenant_info && (
              <div className="text-sm text-green-700 dark:text-green-300">
                <p>Successfully connected to Azure AD tenant: {testResult.tenant_info.tenant_id}</p>
              </div>
            )}
            
            {!testResult.success && (
              <div className="text-sm text-red-700 dark:text-red-300">
                {testResult.error && <p>Error: {testResult.error}</p>}
                {testResult.missing_fields && testResult.missing_fields.length > 0 && (
                  <p>Missing required fields: {testResult.missing_fields.join(', ')}</p>
                )}
              </div>
            )}
          </div>
        )}
        
        {!allRequiredFieldsFilled && (
          <div className="flex items-center space-x-2 text-yellow-600 dark:text-yellow-400 text-sm">
            <AlertTriangle className="w-4 h-4" />
            <span>Fill in all required fields to test the connection</span>
          </div>
        )}
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
            'Continue to Organization Setup'
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