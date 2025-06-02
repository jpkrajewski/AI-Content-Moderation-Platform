export interface ApiKey {
  id: string
  api_key: string
  status: string
  created_at: string
  source: string
  access_count: number
  current_scope: string[]
  is_active: boolean
}
