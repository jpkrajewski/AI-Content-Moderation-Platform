export interface ContentItem {
  id: string
  type: 'text' | 'image' | 'video'
  content: string
  status: 'pending' | 'approved' | 'rejected'
  submittedAt: string
  moderatedAt?: string
  moderatorId?: string
  reason?: string
}

export interface ContentState {
  pendingContent: ContentItem[]
  contentHistory: ContentItem[]
  loading: boolean
  error: string | null
}
