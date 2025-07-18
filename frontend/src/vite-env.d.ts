/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_AZURE_CLIENT_ID: string
  readonly VITE_AZURE_TENANT_ID: string
  readonly VITE_AZURE_REDIRECT_URI: string
  readonly VITE_AZURE_POST_LOGOUT_REDIRECT_URI: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_GRAPH_API_BASE_URL: string
  readonly VITE_APP_VERSION: string
  readonly VITE_APP_ENVIRONMENT: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}