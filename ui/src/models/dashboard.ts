export interface PeakHours {
  [hour: string]: number
}

export interface SubmissionCounts {
  month: number
  today: number
  week: number
}

export interface SubmissionSources {
  [url: string]: number
}

export interface ContentItem {
  growth_rate: number
  peak_hours: PeakHours
  submission_counts: SubmissionCounts
  submission_sources: SubmissionSources
}

export interface MostCommonPiiTypes {
  CREDIT_CARD: number
  EMAIL: number
  PASSWORD: number
  PERSON: number
  URL: number
}

export interface MostCommonToxicityLabels {
  insult: number
  toxicity: number
}

export interface Insights {
  most_common_pii_types: MostCommonPiiTypes
  most_common_toxicity_labels: MostCommonToxicityLabels
  pii_detected_rate: number
}

export interface ModerationStatuses {
  approved: number
  flagged: number
  rejected: number
}

export interface Moderation {
  auto_flag_accuracy: number
  false_positive_rate: number
  statuses: ModerationStatuses
}

export interface DashboardData {
  content: ContentItem
  insights: Insights
  moderation: Moderation
}
