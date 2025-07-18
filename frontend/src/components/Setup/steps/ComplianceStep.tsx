import { useState, useEffect } from 'react'
import { FileCheck, Calendar, Shield, AlertTriangle, Info, CheckCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { LoadingSpinner } from '../../ui/LoadingSpinner'

interface ComplianceStepProps {
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
  possible_values?: string[]
}

const complianceFrameworks = [
  {
    id: 'SOX',
    name: 'Sarbanes-Oxley (SOX)',
    description: 'Financial reporting and internal controls',
    requirements: ['7-year audit log retention', 'Segregation of duties', 'Regular access reviews']
  },
  {
    id: 'SOC2',
    name: 'SOC 2 Type II',
    description: 'Security, availability, processing integrity',
    requirements: ['Continuous monitoring', 'Access controls', 'Incident response']
  },
  {
    id: 'ISO27001',
    name: 'ISO 27001',
    description: 'Information security management system',
    requirements: ['Risk management', 'Security controls', 'Documentation']
  },
  {
    id: 'GDPR',
    name: 'GDPR',
    description: 'General Data Protection Regulation',
    requirements: ['Data minimization', 'Right to erasure', 'Consent management']
  },
  {
    id: 'HIPAA',
    name: 'HIPAA',
    description: 'Health Insurance Portability and Accountability Act',
    requirements: ['PHI protection', 'Administrative safeguards', 'Audit controls']
  }
]

export function ComplianceStep({ onComplete, completing }: ComplianceStepProps) {
  const [configurations, setConfigurations] = useState<ConfigurationField[]>([])
  const [formData, setFormData] = useState<Record<string, any>>({})
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [selectedFrameworks, setSelectedFrameworks] = useState<string[]>([])

  useEffect(() => {
    loadConfigurations()
  }, [])

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/v1/setup/steps/compliance_setup/configurations')
      const data = await response.json()
      
      setConfigurations(data)
      
      // Initialize form data with existing values or defaults
      const initialData: Record<string, any> = {}
      data.forEach((config: ConfigurationField) => {
        if (config.type === 'boolean') {
          initialData[config.key] = config.value === 'true' || config.value === true || 
                                   (config.value === '' && config.default_value === 'true')
        } else if (config.type === 'json' && config.key === 'ENABLED_COMPLIANCE_FRAMEWORKS') {
          try {
            const frameworks = config.value ? JSON.parse(config.value) : JSON.parse(config.default_value || '["SOC2"]')
            initialData[config.key] = frameworks
            setSelectedFrameworks(frameworks)
          } catch {
            initialData[config.key] = ['SOC2']
            setSelectedFrameworks(['SOC2'])
          }
        } else {
          initialData[config.key] = config.value || config.default_value || ''
        }
      })
      setFormData(initialData)
      
    } catch (error) {
      console.error('Failed to load compliance configurations:', error)
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

  const handleFrameworkChange = (frameworkId: string, checked: boolean) => {
    let newFrameworks: string[]
    if (checked) {
      newFrameworks = [...selectedFrameworks, frameworkId]
    } else {
      newFrameworks = selectedFrameworks.filter(id => id !== frameworkId)
    }
    
    setSelectedFrameworks(newFrameworks)
    handleInputChange('ENABLED_COMPLIANCE_FRAMEWORKS', newFrameworks)
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}
    
    // Validate that at least one framework is selected
    if (selectedFrameworks.length === 0) {
      newErrors['ENABLED_COMPLIANCE_FRAMEWORKS'] = 'At least one compliance framework must be selected'
    }
    
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
      const configurationData = configurations.map(config => {
        let value = formData[config.key]
        
        if (config.key === 'ENABLED_COMPLIANCE_FRAMEWORKS') {
          value = JSON.stringify(selectedFrameworks)
        } else if (typeof value === 'boolean') {
          value = value.toString()
        } else {
          value = value?.toString() || ''
        }
        
        return {
          key: config.key,
          value: value
        }
      })

      const response = await fetch('/api/v1/setup/steps/compliance_setup/configurations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          configurations: configurationData,
          change_reason: 'Compliance setup configuration'
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

      toast.success('Compliance configuration saved successfully')
      return true
      
    } catch (error) {
      console.error('Failed to save configurations:', error)
      toast.error('Failed to save compliance configuration')
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

  const getRetentionYears = (days: number): string => {
    const years = Math.round(days / 365)
    return `${years} year${years !== 1 ? 's' : ''}`
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <LoadingSpinner size="lg" label="Loading compliance configuration..." />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Instructions */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Compliance Framework Configuration
        </h4>
        <div className="space-y-3 text-sm text-blue-800 dark:text-blue-200">
          <p>
            Configure compliance frameworks and audit settings to meet your organization's regulatory requirements.
            Menshun PAM provides built-in compliance features for major frameworks.
          </p>
          <div className="space-y-2">
            <p className="font-medium">Compliance features include:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Automated audit log retention and archival</li>
              <li>Access justification and approval workflows</li>
              <li>Segregation of duties controls</li>
              <li>Regular access reviews and certification</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Framework Selection */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Select Compliance Frameworks
        </h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {complianceFrameworks.map((framework) => (
            <div
              key={framework.id}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                selectedFrameworks.includes(framework.id)
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
              }`}
              onClick={() => handleFrameworkChange(framework.id, !selectedFrameworks.includes(framework.id))}
            >
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  checked={selectedFrameworks.includes(framework.id)}
                  onChange={(e) => handleFrameworkChange(framework.id, e.target.checked)}
                  className="mt-1 w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500"
                />
                <div className="flex-1">
                  <h5 className="font-medium text-gray-900 dark:text-white mb-1">
                    {framework.name}
                  </h5>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {framework.description}
                  </p>
                  <div className="space-y-1">
                    {framework.requirements.map((req, index) => (
                      <div key={index} className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                        <CheckCircle className="w-3 h-3" />
                        <span>{req}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {errors['ENABLED_COMPLIANCE_FRAMEWORKS'] && (
          <p className="text-sm text-red-600 dark:text-red-400">
            {errors['ENABLED_COMPLIANCE_FRAMEWORKS']}
          </p>
        )}
      </div>

      {/* Configuration Settings */}
      <div className="space-y-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
          Compliance Settings
        </h4>
        
        {configurations.filter(config => config.key !== 'ENABLED_COMPLIANCE_FRAMEWORKS').map((config) => (
          <div key={config.key} className="space-y-3 p-4 border border-gray-200 dark:border-gray-600 rounded-lg">
            <div className="flex items-center space-x-2">
              {config.key === 'AUDIT_LOG_RETENTION_DAYS' && <Calendar className="w-5 h-5 text-gray-400" />}
              {config.key === 'REQUIRE_JUSTIFICATION_FOR_PRIVILEGED' && <FileCheck className="w-5 h-5 text-gray-400" />}
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {config.display_name}
                {config.is_required && <span className="text-red-500 ml-1">*</span>}
              </label>
            </div>
            
            {config.type === 'boolean' ? (
              <div className="flex items-center space-x-3 ml-7">
                <input
                  type="checkbox"
                  id={config.key}
                  checked={formData[config.key] || false}
                  onChange={(e) => handleInputChange(config.key, e.target.checked)}
                  className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500"
                />
                <label htmlFor={config.key} className="text-sm text-gray-700 dark:text-gray-300">
                  Enable {config.display_name}
                </label>
              </div>
            ) : (
              <div className="ml-7">
                <input
                  type={config.type === 'integer' ? 'number' : 'text'}
                  min={config.type === 'integer' ? '1' : undefined}
                  value={formData[config.key] || ''}
                  onChange={(e) => handleInputChange(config.key, e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-slate-700 dark:border-slate-600 dark:text-white ${
                    errors[config.key] ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder={config.default_value || ''}
                />
                {config.key === 'AUDIT_LOG_RETENTION_DAYS' && formData[config.key] && (
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Equivalent to {getRetentionYears(parseInt(formData[config.key]))}
                  </p>
                )}
              </div>
            )}
            
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

      {/* Compliance Summary */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Compliance Configuration Summary
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Shield className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Active Frameworks</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {selectedFrameworks.length}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {selectedFrameworks.join(', ') || 'None selected'}
            </p>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Calendar className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Log Retention</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {getRetentionYears(parseInt(formData.AUDIT_LOG_RETENTION_DAYS || '2555'))}
            </p>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <FileCheck className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Justification Required</span>
            </div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              {formData.REQUIRE_JUSTIFICATION_FOR_PRIVILEGED ? 'Yes' : 'No'}
            </p>
          </div>
        </div>
      </div>

      {/* Framework-Specific Recommendations */}
      {selectedFrameworks.length > 0 && (
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <Info className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" />
            <div className="space-y-2 text-sm text-green-800 dark:text-green-200">
              <p className="font-medium">Compliance Recommendations for Selected Frameworks:</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                {selectedFrameworks.includes('SOX') && (
                  <li>SOX: Ensure 7-year audit log retention and implement segregation of duties</li>
                )}
                {selectedFrameworks.includes('SOC2') && (
                  <li>SOC 2: Enable continuous monitoring and access reviews</li>
                )}
                {selectedFrameworks.includes('ISO27001') && (
                  <li>ISO 27001: Document security policies and conduct regular risk assessments</li>
                )}
                {selectedFrameworks.includes('GDPR') && (
                  <li>GDPR: Implement data minimization and consent management practices</li>
                )}
                {selectedFrameworks.includes('HIPAA') && (
                  <li>HIPAA: Ensure PHI protection and implement administrative safeguards</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Important Compliance Notes */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
          <div className="space-y-2 text-sm text-yellow-800 dark:text-yellow-200">
            <p className="font-medium">Important Compliance Considerations:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Compliance settings affect audit log retention and storage requirements</li>
              <li>Some frameworks require specific retention periods that cannot be shortened</li>
              <li>Justification requirements may impact user workflows for privileged access</li>
              <li>Regular compliance audits should be scheduled based on selected frameworks</li>
              <li>These settings can be modified but changes may require compliance review</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Completion Button */}
      <div className="text-center pt-6">
        <button
          onClick={handleComplete}
          disabled={completing || selectedFrameworks.length === 0}
          className="px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {completing ? (
            <div className="flex items-center space-x-2">
              <LoadingSpinner size="sm" />
              <span>Saving Configuration...</span>
            </div>
          ) : (
            'Continue to Notifications Setup'
          )}
        </button>
        
        {selectedFrameworks.length === 0 && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Please select at least one compliance framework to continue
          </p>
        )}
      </div>
    </div>
  )
}