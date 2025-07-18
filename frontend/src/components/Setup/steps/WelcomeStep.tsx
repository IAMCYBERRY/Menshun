import { useState, useEffect } from 'react'
import { CheckCircle, XCircle, AlertTriangle, Server, Database, Shield, Globe } from 'lucide-react'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface WelcomeStepProps {
  onComplete: () => void
  onNext: () => void
  completing: boolean
}

interface SystemRequirement {
  name: string
  description: string
  status: 'checking' | 'passed' | 'failed' | 'warning'
  details?: string
  icon: React.ComponentType<{ className?: string }>
}

interface SystemInfo {
  application: {
    name: string
    version: string
    environment: string
  }
  system: {
    platform: string
    platform_release: string
    architecture: string
    hostname: string
  }
  resources: {
    cpu_count: number
    memory_total: number
    memory_available: number
    disk_usage: number
  }
  requirements_met: {
    minimum_memory: boolean
    minimum_disk: boolean
    python_version: string
    recommended_setup: boolean
  }
}

export function WelcomeStep({ onComplete, completing }: WelcomeStepProps) {
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [requirements, setRequirements] = useState<SystemRequirement[]>([
    {
      name: 'System Memory',
      description: 'Minimum 4GB RAM available',
      status: 'checking',
      icon: Server
    },
    {
      name: 'Disk Space',
      description: 'Minimum 10GB free disk space',
      status: 'checking',
      icon: Database
    },
    {
      name: 'Network Connectivity',
      description: 'Internet connection for Azure AD integration',
      status: 'checking',
      icon: Globe
    },
    {
      name: 'Security Requirements',
      description: 'HTTPS and secure configuration',
      status: 'checking',
      icon: Shield
    }
  ])

  useEffect(() => {
    checkSystemRequirements()
  }, [])

  const checkSystemRequirements = async () => {
    try {
      const response = await fetch('/api/v1/setup/system-info')
      const data: SystemInfo = await response.json()
      setSystemInfo(data)

      // Update requirements based on system info
      const updatedRequirements = requirements.map(req => {
        switch (req.name) {
          case 'System Memory':
            return {
              ...req,
              status: data.requirements_met.minimum_memory ? 'passed' : 'failed',
              details: `${formatBytes(data.resources.memory_available)} available of ${formatBytes(data.resources.memory_total)} total`
            }
          case 'Disk Space':
            return {
              ...req,
              status: data.requirements_met.minimum_disk ? 'passed' : 'warning',
              details: `${data.resources.disk_usage}% disk usage`
            }
          case 'Network Connectivity':
            return {
              ...req,
              status: 'passed', // Assume passed if we can reach the API
              details: 'Connection to setup API successful'
            }
          case 'Security Requirements':
            return {
              ...req,
              status: data.requirements_met.recommended_setup ? 'passed' : 'warning',
              details: data.requirements_met.recommended_setup ? 'All security requirements met' : 'Some security settings need attention'
            }
          default:
            return req
        }
      })

      setRequirements(updatedRequirements)
    } catch (error) {
      console.error('Failed to check system requirements:', error)
      // Mark all as failed if we can't get system info
      setRequirements(prev => prev.map(req => ({ ...req, status: 'failed', details: 'Unable to check system requirements' })))
    } finally {
      setLoading(false)
    }
  }

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'passed':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />
      default:
        return <LoadingSpinner size="sm" />
    }
  }

  const allRequirementsPassed = requirements.every(req => req.status === 'passed' || req.status === 'warning')
  const hasFailures = requirements.some(req => req.status === 'failed')

  return (
    <div className="space-y-8">
      {/* Welcome Message */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-primary-500 to-purple-600">
            <Shield className="h-8 w-8 text-white" />
          </div>
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome to Menshun PAM
        </h3>
        <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Menshun is an Enterprise Privileged Access Management solution for Microsoft Entra ID environments. 
          This setup wizard will guide you through the initial configuration to get your PAM system up and running.
        </p>
      </div>

      {/* System Information */}
      {systemInfo && (
        <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-6">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">System Information</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <strong className="text-gray-700 dark:text-gray-300">Application:</strong>
              <div className="text-gray-600 dark:text-gray-400">
                {systemInfo.application.name} v{systemInfo.application.version}
              </div>
            </div>
            <div>
              <strong className="text-gray-700 dark:text-gray-300">Environment:</strong>
              <div className="text-gray-600 dark:text-gray-400">
                {systemInfo.application.environment}
              </div>
            </div>
            <div>
              <strong className="text-gray-700 dark:text-gray-300">Platform:</strong>
              <div className="text-gray-600 dark:text-gray-400">
                {systemInfo.system.platform} {systemInfo.system.platform_release}
              </div>
            </div>
            <div>
              <strong className="text-gray-700 dark:text-gray-300">Architecture:</strong>
              <div className="text-gray-600 dark:text-gray-400">
                {systemInfo.system.architecture}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* System Requirements Check */}
      <div>
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          System Requirements Check
        </h4>
        
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <LoadingSpinner size="lg" label="Checking system requirements..." />
          </div>
        ) : (
          <div className="space-y-4">
            {requirements.map((requirement, index) => {
              const IconComponent = requirement.icon
              return (
                <div
                  key={index}
                  className="flex items-center space-x-4 p-4 rounded-lg border border-gray-200 dark:border-gray-600"
                >
                  <div className="flex-shrink-0">
                    <IconComponent className="w-6 h-6 text-gray-500 dark:text-gray-400" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <h5 className="font-medium text-gray-900 dark:text-white">
                        {requirement.name}
                      </h5>
                      {getStatusIcon(requirement.status)}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {requirement.description}
                    </p>
                    {requirement.details && (
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {requirement.details}
                      </p>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Prerequisites Information */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Before You Begin
        </h4>
        <div className="space-y-2 text-sm text-blue-800 dark:text-blue-200">
          <p>Please ensure you have the following information ready:</p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li>Azure AD Application (Client) ID</li>
            <li>Azure AD Client Secret</li>
            <li>Azure AD Tenant (Directory) ID</li>
            <li>Organization details and primary administrator email</li>
            <li>SMTP server information for email notifications (optional)</li>
          </ul>
          <p className="mt-3">
            If you don't have Azure AD application credentials, you'll need to create an app registration 
            in the Azure portal before proceeding.
          </p>
        </div>
      </div>

      {/* Status Summary */}
      {!loading && (
        <div className="text-center">
          {hasFailures ? (
            <div className="text-red-600 dark:text-red-400">
              <XCircle className="w-8 h-8 mx-auto mb-2" />
              <p className="font-medium">System requirements check failed</p>
              <p className="text-sm">Please resolve the failed requirements before continuing.</p>
            </div>
          ) : allRequirementsPassed ? (
            <div className="text-green-600 dark:text-green-400">
              <CheckCircle className="w-8 h-8 mx-auto mb-2" />
              <p className="font-medium">System requirements check passed</p>
              <p className="text-sm">Your system is ready for Menshun PAM setup.</p>
            </div>
          ) : (
            <div className="text-yellow-600 dark:text-yellow-400">
              <AlertTriangle className="w-8 h-8 mx-auto mb-2" />
              <p className="font-medium">System requirements check completed with warnings</p>
              <p className="text-sm">You can continue, but some features may not work optimally.</p>
            </div>
          )}
        </div>
      )}

      {/* Continue Button */}
      <div className="text-center">
        <button
          onClick={onComplete}
          disabled={completing || loading || hasFailures}
          className="px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {completing ? (
            <div className="flex items-center space-x-2">
              <LoadingSpinner size="sm" />
              <span>Starting Setup...</span>
            </div>
          ) : (
            'Begin Setup'
          )}
        </button>
      </div>
    </div>
  )
}