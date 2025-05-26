export interface AnalysisResult {
  content_type: string
  automated_flag: boolean
  automated_flag_reason: string
  model_version: string
  analysis_metadata: Record<string, unknown>
}

export interface ContentItem {
  id: string
  body: string
  tags: string[]
  localization: string
  source: string
  status: string
  created_at: string
  results: AnalysisResult[]
}
