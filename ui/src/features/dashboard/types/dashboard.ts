export interface DashboardData {
  insights: Insights
  content: Content
  moderation: Moderation
}

export interface Insights {
  most_common_pii_types: Record<string, number>
  most_common_toxicity_labels: {
    insult: number
    toxicity: number
    [key: string]: number
  }
  pii_detected_rate: number
}

export interface Content {
  growth_rate: number
  peak_hours: Record<string, number>
  submission_counts: {
    today: number
    month: number
    week: number
    [key: string]: number
  }
  submission_sources: Record<string, number>
}

export interface Moderation {
  average_response_time: number
  statuses: {
    approved: number
    flagged: number
    rejected: number
    [key: string]: number
  }
  auto_flag_accuracy: number
  false_positive_rate: number
}

export interface ModerationResult {
  content_type: string
  automated_flag: boolean
  automated_flag_reason?: string
  model_version: string
  analysis_metadata: Record<string, unknown>
}

export interface Section {
  title: string
  data: Record<string, string | number>
}

export interface ContentItem {
  id: string
  title: string
  body: string
  tags: string[]
  localization: string
  source: string
  status: 'pending' | 'approved' | 'rejected' | 'flagged'
  created_at: string
  results?: ModerationResult[]
}
