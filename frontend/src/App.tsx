import { Routes, Route, Navigate } from 'react-router-dom'
import { useIsAuthenticated } from '@azure/msal-react'

import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react'
import { Layout } from './components/Layout'
import { LoginPage } from './pages/auth/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { UsersPage } from './pages/users/UsersPage'
import { ServiceIdentitiesPage } from './pages/service-identities/ServiceIdentitiesPage'
import { CredentialsPage } from './pages/credentials/CredentialsPage'
import { RoleAssignmentsPage } from './pages/role-assignments/RoleAssignmentsPage'
import { AuditLogsPage } from './pages/audit/AuditLogsPage'
import { SettingsPage } from './pages/settings/SettingsPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { LoadingSpinner } from './components/ui/LoadingSpinner'

function App() {
  const isAuthenticated = useIsAuthenticated()

  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900'>
      <UnauthenticatedTemplate>
        <Routes>
          <Route path='/login' element={<LoginPage />} />
          <Route path='*' element={<Navigate to='/login' replace />} />
        </Routes>
      </UnauthenticatedTemplate>

      <AuthenticatedTemplate>
        <Layout>
          <Routes>
            {/* Dashboard */}
            <Route path='/' element={<DashboardPage />} />
            <Route path='/dashboard' element={<Navigate to='/' replace />} />

            {/* User Management */}
            <Route path='/users' element={<UsersPage />} />
            <Route path='/users/:userId' element={<div>User Details</div>} />

            {/* Service Identities */}
            <Route path='/service-identities' element={<ServiceIdentitiesPage />} />
            <Route path='/service-identities/:identityId' element={<div>Identity Details</div>} />

            {/* Credentials */}
            <Route path='/credentials' element={<CredentialsPage />} />
            <Route path='/credentials/:credentialId' element={<div>Credential Details</div>} />

            {/* Role Assignments */}
            <Route path='/role-assignments' element={<RoleAssignmentsPage />} />
            <Route path='/role-assignments/:assignmentId' element={<div>Assignment Details</div>} />

            {/* Audit & Compliance */}
            <Route path='/audit' element={<AuditLogsPage />} />
            <Route path='/audit/:logId' element={<div>Audit Log Details</div>} />

            {/* Settings */}
            <Route path='/settings' element={<SettingsPage />} />
            <Route path='/settings/:section' element={<SettingsPage />} />

            {/* Catch all */}
            <Route path='/404' element={<NotFoundPage />} />
            <Route path='*' element={<Navigate to='/404' replace />} />
          </Routes>
        </Layout>
      </AuthenticatedTemplate>
    </div>
  )
}

export default App