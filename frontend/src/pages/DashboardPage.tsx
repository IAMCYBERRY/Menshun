import {
  Users,
  Bot,
  Key,
  Crown,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
} from 'lucide-react'

export function DashboardPage() {
  const stats = [
    {
      name: 'Total Privileged Users',
      value: '1,247',
      change: '+4.3%',
      changeType: 'increase',
      icon: Users,
      color: 'blue',
    },
    {
      name: 'Service Identities',
      value: '892',
      change: '+12.1%',
      changeType: 'increase',
      icon: Bot,
      color: 'purple',
    },
    {
      name: 'Active Credentials',
      value: '3,456',
      change: '-2.1%',
      changeType: 'decrease',
      icon: Key,
      color: 'green',
    },
    {
      name: 'Role Assignments',
      value: '2,134',
      change: '+8.7%',
      changeType: 'increase',
      icon: Crown,
      color: 'yellow',
    },
  ]

  const riskAlerts = [
    {
      id: 1,
      title: 'High-risk role assignment detected',
      description: 'Global Administrator assigned to external user',
      severity: 'critical',
      time: '2 minutes ago',
    },
    {
      id: 2,
      title: 'Credential rotation overdue',
      description: '15 service accounts require immediate rotation',
      severity: 'high',
      time: '1 hour ago',
    },
    {
      id: 3,
      title: 'Compliance certification due',
      description: '8 privileged users need recertification',
      severity: 'medium',
      time: '4 hours ago',
    },
  ]

  const recentActivities = [
    {
      id: 1,
      action: 'Role assignment approved',
      user: 'john.doe@company.com',
      role: 'Security Administrator',
      time: '5 minutes ago',
      status: 'success',
    },
    {
      id: 2,
      action: 'Credential rotated',
      user: 'service-account-prod',
      resource: 'Azure Key Vault',
      time: '12 minutes ago',
      status: 'success',
    },
    {
      id: 3,
      action: 'Login attempt blocked',
      user: 'suspicious.user@domain.com',
      reason: 'Location anomaly',
      time: '23 minutes ago',
      status: 'warning',
    },
  ]

  return (
    <div className='space-y-6'>
      {/* Page header */}
      <div>
        <h1 className='text-2xl font-bold text-gray-900 dark:text-white'>Dashboard</h1>
        <p className='mt-1 text-sm text-gray-500 dark:text-gray-400'>
          Monitor your privileged access management system
        </p>
      </div>

      {/* Stats grid */}
      <div className='grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4'>
        {stats.map(stat => (
          <div
            key={stat.name}
            className='bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg border border-gray-200 dark:border-gray-700'
          >
            <div className='p-5'>
              <div className='flex items-center'>
                <div className='flex-shrink-0'>
                  <div
                    className={`p-3 rounded-lg ${
                      stat.color === 'blue'
                        ? 'bg-blue-100 dark:bg-blue-900/50'
                        : stat.color === 'purple'
                        ? 'bg-purple-100 dark:bg-purple-900/50'
                        : stat.color === 'green'
                        ? 'bg-green-100 dark:bg-green-900/50'
                        : 'bg-yellow-100 dark:bg-yellow-900/50'
                    }`}
                  >
                    <stat.icon
                      className={`h-6 w-6 ${
                        stat.color === 'blue'
                          ? 'text-blue-600 dark:text-blue-400'
                          : stat.color === 'purple'
                          ? 'text-purple-600 dark:text-purple-400'
                          : stat.color === 'green'
                          ? 'text-green-600 dark:text-green-400'
                          : 'text-yellow-600 dark:text-yellow-400'
                      }`}
                    />
                  </div>
                </div>
                <div className='ml-5 w-0 flex-1'>
                  <dl>
                    <dt className='text-sm font-medium text-gray-500 dark:text-gray-400 truncate'>
                      {stat.name}
                    </dt>
                    <dd className='flex items-baseline'>
                      <div className='text-2xl font-semibold text-gray-900 dark:text-white'>
                        {stat.value}
                      </div>
                      <div
                        className={`ml-2 flex items-baseline text-sm font-semibold ${
                          stat.changeType === 'increase'
                            ? 'text-green-600 dark:text-green-400'
                            : 'text-red-600 dark:text-red-400'
                        }`}
                      >
                        <TrendingUp className='self-center flex-shrink-0 h-4 w-4' />
                        <span className='ml-1'>{stat.change}</span>
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className='grid grid-cols-1 gap-6 lg:grid-cols-2'>
        {/* Risk Alerts */}
        <div className='bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700'>
          <div className='px-6 py-4 border-b border-gray-200 dark:border-gray-700'>
            <h3 className='text-lg font-medium text-gray-900 dark:text-white'>Risk Alerts</h3>
          </div>
          <div className='p-6'>
            <div className='space-y-4'>
              {riskAlerts.map(alert => (
                <div key={alert.id} className='flex items-start space-x-3'>
                  <div
                    className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${
                      alert.severity === 'critical'
                        ? 'bg-red-500'
                        : alert.severity === 'high'
                        ? 'bg-orange-500'
                        : 'bg-yellow-500'
                    }`}
                  />
                  <div className='flex-1 min-w-0'>
                    <p className='text-sm font-medium text-gray-900 dark:text-white'>
                      {alert.title}
                    </p>
                    <p className='text-sm text-gray-500 dark:text-gray-400'>{alert.description}</p>
                    <p className='text-xs text-gray-400 dark:text-gray-500 mt-1'>{alert.time}</p>
                  </div>
                  <AlertTriangle
                    className={`flex-shrink-0 h-5 w-5 ${
                      alert.severity === 'critical'
                        ? 'text-red-500'
                        : alert.severity === 'high'
                        ? 'text-orange-500'
                        : 'text-yellow-500'
                    }`}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Activities */}
        <div className='bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700'>
          <div className='px-6 py-4 border-b border-gray-200 dark:border-gray-700'>
            <h3 className='text-lg font-medium text-gray-900 dark:text-white'>Recent Activities</h3>
          </div>
          <div className='p-6'>
            <div className='space-y-4'>
              {recentActivities.map(activity => (
                <div key={activity.id} className='flex items-start space-x-3'>
                  <div className='flex-shrink-0'>
                    {activity.status === 'success' ? (
                      <CheckCircle className='h-5 w-5 text-green-500' />
                    ) : activity.status === 'warning' ? (
                      <AlertTriangle className='h-5 w-5 text-yellow-500' />
                    ) : (
                      <Clock className='h-5 w-5 text-gray-400' />
                    )}
                  </div>
                  <div className='flex-1 min-w-0'>
                    <p className='text-sm font-medium text-gray-900 dark:text-white'>
                      {activity.action}
                    </p>
                    <p className='text-sm text-gray-500 dark:text-gray-400'>
                      {activity.user} {activity.role && `→ ${activity.role}`}
                      {activity.resource && `→ ${activity.resource}`}
                      {activity.reason && `→ ${activity.reason}`}
                    </p>
                    <p className='text-xs text-gray-400 dark:text-gray-500 mt-1'>{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}