import { Configuration, RedirectRequest, SilentRequest } from '@azure/msal-browser'

export const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_AZURE_CLIENT_ID || '',
    authority: `https://login.microsoftonline.com/${import.meta.env.VITE_AZURE_TENANT_ID || 'common'}`,
    redirectUri: import.meta.env.VITE_AZURE_REDIRECT_URI || window.location.origin,
    postLogoutRedirectUri: import.meta.env.VITE_AZURE_POST_LOGOUT_REDIRECT_URI || window.location.origin,
    navigateToLoginRequestUrl: true,
  },
  cache: {
    cacheLocation: 'localStorage',
    storeAuthStateInCookie: false,
  },
  system: {
    loggerOptions: {
      loggerCallback: (level, message, containsPii) => {
        if (containsPii) {
          return
        }
        switch (level) {
          case 0: // Error
            console.error(message)
            break
          case 1: // Warning
            console.warn(message)
            break
          case 2: // Info
            console.info(message)
            break
          case 3: // Verbose
            console.debug(message)
            break
        }
      },
      piiLoggingEnabled: false,
    },
    windowHashTimeout: 60000,
    iframeHashTimeout: 6000,
    loadFrameTimeout: 0,
  },
}

export const loginRequest: RedirectRequest = {
  scopes: [
    'User.Read',
    'User.ReadWrite.All',
    'Directory.Read.All',
    'Directory.ReadWrite.All',
    'Application.Read.All',
    'Application.ReadWrite.All',
    'RoleManagement.Read.All',
    'RoleManagement.ReadWrite.Directory',
    'AuditLog.Read.All',
  ],
  prompt: 'select_account',
}

export const silentRequest: SilentRequest = {
  scopes: [
    'User.Read',
    'User.ReadWrite.All',
    'Directory.Read.All',
    'Directory.ReadWrite.All',
    'Application.Read.All',
    'Application.ReadWrite.All',
    'RoleManagement.Read.All',
    'RoleManagement.ReadWrite.Directory',
    'AuditLog.Read.All',
  ],
}

export const graphRequest = {
  scopes: [
    'https://graph.microsoft.com/User.Read',
    'https://graph.microsoft.com/User.ReadWrite.All',
    'https://graph.microsoft.com/Directory.Read.All',
    'https://graph.microsoft.com/Directory.ReadWrite.All',
    'https://graph.microsoft.com/Application.Read.All',
    'https://graph.microsoft.com/Application.ReadWrite.All',
    'https://graph.microsoft.com/RoleManagement.Read.All',
    'https://graph.microsoft.com/RoleManagement.ReadWrite.Directory',
    'https://graph.microsoft.com/AuditLog.Read.All',
  ],
}