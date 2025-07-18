import '@testing-library/jest-dom'

// Mock environment variables
process.env.VITE_AZURE_CLIENT_ID = 'test-client-id'
process.env.VITE_AZURE_TENANT_ID = 'test-tenant-id'
process.env.VITE_AZURE_REDIRECT_URI = 'http://localhost:3000'
process.env.VITE_API_BASE_URL = 'http://localhost:8000/api/v1'

// Mock MSAL
jest.mock('@azure/msal-browser', () => ({
  PublicClientApplication: jest.fn().mockImplementation(() => ({
    loginRedirect: jest.fn(),
    logout: jest.fn(),
    getAllAccounts: jest.fn(() => []),
    getAccountByUsername: jest.fn(),
    acquireTokenSilent: jest.fn(),
  })),
}))

// Mock MSAL React
jest.mock('@azure/msal-react', () => ({
  MsalProvider: ({ children }: { children: React.ReactNode }) => children,
  useMsal: () => ({
    instance: {
      loginRedirect: jest.fn(),
      logout: jest.fn(),
    },
    accounts: [],
    inProgress: 'none',
  }),
  useIsAuthenticated: () => false,
  AuthenticatedTemplate: ({ children }: { children: React.ReactNode }) => children,
  UnauthenticatedTemplate: ({ children }: { children: React.ReactNode }) => children,
}))

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
}

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
}