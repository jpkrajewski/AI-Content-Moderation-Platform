export interface DashboardData {
  total_submissions: number
  pending_review: number
  approved_content: number
  rejected_content: number
  flagged_content: number
  insights: Insights
  recent_content: ContentItem[]
  moderation_stats: Moderation
}

export interface Insights {
  content_by_source: Record<string, number>
  content_by_language: Record<string, number>
  peak_hours: Record<string, number>
  average_response_time: number
  most_common_pii_types: Record<string, number>
  most_common_toxicity_labels: Record<string, number>
  pii_detected_rate: number
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
  submission_sources: Record<string, number>
  peak_hours: Record<string, number>
  submission_counts: {
    today: number
  }
  growth_rate: number
}

export interface ModerationResult {
  content_type: string
  automated_flag: boolean
  automated_flag_reason?: string
  model_version: string
  analysis_metadata: Record<string, unknown>
}

export interface Moderation {
  total_moderated: number
  average_response_time: number
  accuracy_rate: number
  false_positives: number
  false_negatives: number
  statuses: {
    approved: number
    flagged: number
    rejected: number
  }
  auto_flag_accuracy: number
  false_positive_rate: number
}

export interface Section {
  title: string
  data: Record<string, string | number>
}
