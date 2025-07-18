import { useState, useEffect } from 'react'
import { CheckCircle, Shield, Building, Server, Mail, FileCheck, AlertTriangle, Loader } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface ReviewStepProps {
  onComplete: () => void
  onNext: () => void
  completing: boolean
}

interface ConfigurationSummary {
  category: string
  icon: React.ComponentType<{ className?: string }>
  items: Array<{
    label: string
    value: string | boolean
    sensitive?: boolean
  }>
}

interface SetupProgress {
  total_steps: number
  completed_steps: number
  completion_percentage: number
  is_complete: boolean
  steps: Array<{
    step: string
    name: string
    is_completed: boolean
  }>
}

export function ReviewStep({ onComplete, completing }: ReviewStepProps) {
  const [loading, setLoading] = useState(true)
  const [setupProgress, setSetupProgress] = useState<SetupProgress | null>(null)
  const [configurationSummary, setConfigurationSummary] = useState<ConfigurationSummary[]>([])
  const [finalizing, setFinalizing] = useState(false)

  useEffect(() => {
    loadSetupData()
  }, [])

  const loadSetupData = async () => {
    try {
      // Load setup progress
      const progressResponse = await fetch('/api/v1/setup/progress')
      const progressData = await progressResponse.json()
      setSetupProgress(progressData)

      // Load configuration summaries from each step
      const summaries: ConfigurationSummary[] = []

      // Azure AD Configuration
      try {
        const azureResponse = await fetch('/api/v1/setup/steps/azure_setup/configurations')
        const azureData = await azureResponse.json()
        const azureItems = azureData.map((config: any) => ({
          label: config.display_name,
          value: config.is_sensitive ? (config.value ? '••••••••' : 'Not configured') : (config.value || 'Not configured'),
          sensitive: config.is_sensitive
        }))
        summaries.push({
          category: 'Azure AD Configuration',
          icon: Shield,
          items: azureItems
        })
      } catch (error) {
        console.error('Failed to load Azure configuration:', error)
      }

      // Organization Configuration
      try {
        const orgResponse = await fetch('/api/v1/setup/steps/organization_setup/configurations')
        const orgData = await orgResponse.json()
        const orgItems = orgData.map((config: any) => ({
          label: config.display_name,
          value: config.value || 'Not configured'
        }))
        summaries.push({
          category: 'Organization Details',
          icon: Building,
          items: orgItems
        })
      } catch (error) {
        console.error('Failed to load organization configuration:', error)
      }

      // Security Configuration
      try {
        const securityResponse = await fetch('/api/v1/setup/steps/security_setup/configurations')
        const securityData = await securityResponse.json()
        const securityItems = securityData.map((config: any) => {
          let value = config.value || config.default_value || 'Not configured'
          if (config.type === 'boolean') {
            value = value === 'true' || value === true ? 'Enabled' : 'Disabled'
          } else if (config.key === 'DEFAULT_SESSION_TIMEOUT') {
            value = `${value} minutes`
          } else if (config.key === 'MAX_ROLE_ASSIGNMENT_DURATION') {
            value = `${value} days`
          }
          return {
            label: config.display_name,
            value: value
          }
        })
        summaries.push({
          category: 'Security Policies',
          icon: Shield,
          items: securityItems
        })
      } catch (error) {
        console.error('Failed to load security configuration:', error)
      }

      // Compliance Configuration
      try {
        const complianceResponse = await fetch('/api/v1/setup/steps/compliance_setup/configurations')
        const complianceData = await complianceResponse.json()
        const complianceItems = complianceData.map((config: any) => {
          let value = config.value || config.default_value || 'Not configured'
          if (config.type === 'boolean') {
            value = value === 'true' || value === true ? 'Enabled' : 'Disabled'
          } else if (config.key === 'ENABLED_COMPLIANCE_FRAMEWORKS') {
            try {
              const frameworks = JSON.parse(value)
              value = frameworks.length > 0 ? frameworks.join(', ') : 'None selected'
            } catch {
              value = 'Not configured'
            }
          } else if (config.key === 'AUDIT_LOG_RETENTION_DAYS') {
            const years = Math.round(parseInt(value) / 365)
            value = `${value} days (${years} years)`
          }
          return {
            label: config.display_name,
            value: value
          }
        })
        summaries.push({
          category: 'Compliance Settings',
          icon: FileCheck,
          items: complianceItems
        })
      } catch (error) {
        console.error('Failed to load compliance configuration:', error)
      }

      // Notifications Configuration
      try {
        const notificationsResponse = await fetch('/api/v1/setup/steps/notifications_setup/configurations')
        const notificationsData = await notificationsResponse.json()
        const hasEmailConfig = notificationsData.some((config: any) => config.value && config.value.trim() !== '')
        
        if (hasEmailConfig) {
          const notificationItems = notificationsData.map((config: any) => ({
            label: config.display_name,
            value: config.is_sensitive ? (config.value ? '••••••••' : 'Not configured') : (config.value || 'Not configured'),
            sensitive: config.is_sensitive
          }))
          summaries.push({
            category: 'Email Notifications',
            icon: Mail,
            items: notificationItems
          })
        } else {
          summaries.push({
            category: 'Email Notifications',
            icon: Mail,
            items: [{ label: 'Status', value: 'Skipped (can be configured later)' }]
          })
        }
      } catch (error) {
        console.error('Failed to load notifications configuration:', error)
      }

      setConfigurationSummary(summaries)

    } catch (error) {
      console.error('Failed to load setup data:', error)
      toast.error('Failed to load setup summary')
    } finally {
      setLoading(false)
    }
  }

  const handleCompleteSetup = async () => {
    setFinalizing(true)
    
    try {
      // Mark the final step as complete
      const response = await fetch('/api/v1/setup/steps/review_complete/complete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          completion_notes: 'Setup wizard completed successfully'
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to complete setup')
      }

      const result = await response.json()
      
      if (result.success) {
        toast.success('🎉 Menshun PAM setup completed successfully!')
        
        // Wait a moment for the user to see the success message
        setTimeout(() => {
          onComplete()
        }, 2000)
      } else {
        throw new Error('Setup completion failed')
      }

    } catch (error) {
      console.error('Failed to complete setup:', error)
      toast.error('Failed to complete setup. Please try again.')
    } finally {
      setFinalizing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading setup summary..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Completion Status */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-green-500 to-green-600">
            <CheckCircle className="h-8 w-8 text-white" />
          </div>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Setup Almost Complete!
        </h3>
        <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Review your configuration below and click "Complete Setup" to finish initializing your 
          Menshun PAM system. You can modify these settings later in the administration panel.
        </p>
      </div>

      {/* Setup Progress Summary */}
      {setupProgress && (
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-3">
            Setup Progress
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {setupProgress.completed_steps}
              </div>
              <div className="text-sm text-green-700 dark:text-green-300">Steps Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {setupProgress.completion_percentage}%
              </div>
              <div className="text-sm text-green-700 dark:text-green-300">Progress</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {setupProgress.total_steps}
              </div>
              <div className="text-sm text-green-700 dark:text-green-300">Total Steps</div>
            </div>
          </div>
        </div>
      )}

      {/* Configuration Summary */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Configuration Summary
        </h4>
        
        {configurationSummary.map((section, index) => {
          const IconComponent = section.icon
          return (
            <div key={index} className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-purple-600">
                  <IconComponent className="h-4 w-4 text-white" />
                </div>
                <h5 className="text-lg font-medium text-gray-900 dark:text-white">
                  {section.category}
                </h5>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {section.items.map((item, itemIndex) => (
                  <div key={itemIndex} className="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-600 last:border-b-0">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {item.label}:
                    </span>
                    <span className={`text-sm text-gray-600 dark:text-gray-400 text-right max-w-xs truncate ${
                      item.sensitive ? 'font-mono' : ''
                    }`}>
                      {typeof item.value === 'boolean' ? (item.value ? 'Yes' : 'No') : item.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Important Next Steps */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          What Happens Next
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>After completing the setup, you'll be redirected to the main Menshun PAM dashboard where you can:</p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li>Start managing privileged users and role assignments</li>
            <li>Configure additional security policies and workflows</li>
            <li>Set up automated access reviews and compliance reporting</li>
            <li>Integrate with additional Azure AD applications and services</li>
            <li>Monitor privileged access activities through the audit dashboard</li>
          </ul>
        </div>
      </div>

      {/* Pre-Setup Checklist */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p className="font-medium">Before You Begin:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Ensure your Azure AD application has the required permissions configured</li>
              <li>Verify that the primary administrator email is accessible</li>
              <li>Review your organization's security and compliance requirements</li>
              <li>Consider creating additional administrator accounts after setup</li>
              <li>Plan your initial privileged user onboarding strategy</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Completion Button */}
      <div className="text-center pt-6">
        <button
          onClick={handleCompleteSetup}
          disabled={finalizing}
          className="px-8 py-4 bg-gradient-to-r from-green-600 to-green-700 text-white font-semibold rounded-lg hover:from-green-700 hover:to-green-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg"
        >
          {finalizing ? (
            <div className="flex items-center space-x-2">
              <Loader className="w-5 h-5 animate-spin" />
              <span>Finalizing Setup...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5" />
              <span>Complete Menshun PAM Setup</span>
            </div>
          )}
        </button>
        
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-3">
          You'll be redirected to the main application after setup is complete
        </p>
      </div>

      {/* Support Information */}
      <div className="text-center text-sm text-gray-500 dark:text-gray-400 pt-4 border-t border-gray-200 dark:border-gray-700">
        <p>
          Need help? Check the documentation or contact support for assistance with your Menshun PAM deployment.
        </p>
      </div>
    </div>
  )
}