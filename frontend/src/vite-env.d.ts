/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_AWS_ACCESS_KEY_ID: string
  readonly VITE_AWS_REGION: string
  readonly VITE_LOCALSTACK_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
