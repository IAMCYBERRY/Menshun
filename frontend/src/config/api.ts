export const apiConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  retries: 3,
  retryDelay: 1000,
} as const

export const endpoints = {
  // Authentication
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    profile: '/auth/profile',
  },
  
  // Users
  users: {
    list: '/users',
    create: '/users',
    get: (id: string) => `/users/${id}`,
    update: (id: string) => `/users/${id}`,
    delete: (id: string) => `/users/${id}`,
    search: '/users/search',
  },
  
  // Service Identities
  serviceIdentities: {
    list: '/service-identities',
    create: '/service-identities',
    get: (id: string) => `/service-identities/${id}`,
    update: (id: string) => `/service-identities/${id}`,
    delete: (id: string) => `/service-identities/${id}`,
    search: '/service-identities/search',
  },
  
  // Credentials
  credentials: {
    list: '/credentials',
    create: '/credentials',
    get: (id: string) => `/credentials/${id}`,
    update: (id: string) => `/credentials/${id}`,
    delete: (id: string) => `/credentials/${id}`,
    rotate: (id: string) => `/credentials/${id}/rotate`,
  },
  
  // Role Assignments
  roleAssignments: {
    list: '/role-assignments',
    create: '/role-assignments',
    get: (id: string) => `/role-assignments/${id}`,
    update: (id: string) => `/role-assignments/${id}`,
    delete: (id: string) => `/role-assignments/${id}`,
    approve: (id: string) => `/role-assignments/${id}/approve`,
    deny: (id: string) => `/role-assignments/${id}/deny`,
  },
  
  // Directory Roles
  directoryRoles: {
    list: '/directory-roles',
    get: (id: string) => `/directory-roles/${id}`,
    search: '/directory-roles/search',
  },
  
  // Audit Logs
  auditLogs: {
    list: '/audit-logs',
    get: (id: string) => `/audit-logs/${id}`,
    search: '/audit-logs/search',
    export: '/audit-logs/export',
  },
  
  // Dashboard
  dashboard: {
    stats: '/dashboard/stats',
    metrics: '/dashboard/metrics',
    alerts: '/dashboard/alerts',
  },
  
  // Health
  health: {
    check: '/health',
    ready: '/health/ready',
    live: '/health/live',
  },
} as const

export const graphEndpoints = {
  users: 'https://graph.microsoft.com/v1.0/users',
  groups: 'https://graph.microsoft.com/v1.0/groups',
  applications: 'https://graph.microsoft.com/v1.0/applications',
  servicePrincipals: 'https://graph.microsoft.com/v1.0/servicePrincipals',
  directoryRoles: 'https://graph.microsoft.com/v1.0/directoryRoles',
  roleAssignments: 'https://graph.microsoft.com/v1.0/roleAssignments',
  auditLogs: 'https://graph.microsoft.com/v1.0/auditLogs',
} as const