<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  getContentAnalysis,
  moderateContent,
  flagContent,
} from '@/features/moderation/services/moderation'
import { useRoute } from 'vue-router'
import type { ContentItem } from '@/features/dashboard/types/dashboard'

const route = useRoute()
const contentId = route.params.contentId as string

const content = ref<ContentItem | null>(null)
const loading = ref(true)
const error = ref('')
const actionMessage = ref('')
const processing = ref(false)

const fetchContentAnalysis = async () => {
  try {
    const data = await getContentAnalysis(contentId)
    content.value = (data as unknown as ContentItem) || null
  } catch {
    error.value = 'Failed to fetch content analysis.'
  } finally {
    loading.value = false
  }
}

const handleAction = async (action: 'approve' | 'reject' | 'flag') => {
  if (!content.value) return

  processing.value = true
  actionMessage.value = ''

  try {
    switch (action) {
      case 'approve':
        await moderateContent(contentId, 'approve')
        actionMessage.value = 'Content approved.'
        content.value.status = 'approved'
        break
      case 'reject':
        await moderateContent(contentId, 'reject')
        actionMessage.value = 'Content rejected.'
        content.value.status = 'rejected'
        break
      case 'flag':
        await flagContent(contentId)
        actionMessage.value = 'Content flagged.'
        break
    }
  } catch {
    actionMessage.value = 'Action failed. Please try again.'
  } finally {
    processing.value = false
  }
}

onMounted(fetchContentAnalysis)
</script>

<template>
  <div class="max-w-5xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Content Analysis</h1>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="error" class="text-red-600">{{ error }}</div>

    <div v-else class="bg-white rounded-xl shadow p-6 border border-gray-200 space-y-4">
      <div v-if="content" class="space-y-4">
        <div class="text-sm text-gray-500">ID: {{ content.id }}</div>
        <div class="text-gray-700 whitespace-pre-wrap">{{ content.body }}</div>

        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in content.tags"
            :key="tag"
            class="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
          >
            {{ tag }}
          </span>
        </div>

        <div class="text-sm text-gray-600">
          <p>Localization: {{ content.localization }}</p>
          <p>Source: {{ content.source }}</p>
          <p>
            Status: <strong class="capitalize">{{ content.status }}</strong>
          </p>
          <p>Created: {{ new Date(content.created_at).toLocaleString() }}</p>
        </div>

        <!-- Analysis Results -->
        <div v-if="content.results?.length">
          <h2 class="text-lg font-semibold mt-4 mb-2">Analysis Results</h2>

          <div
            v-for="(res, i) in content.results"
            :key="i"
            class="border rounded-lg p-4 mb-4 bg-gray-50"
          >
            <p><strong>Content Type:</strong> {{ res.content_type }}</p>
            <p>
              <strong>Flagged:</strong>
              <span :class="res.automated_flag ? 'text-red-600 font-semibold' : 'text-green-600'">
                {{ res.automated_flag ? 'Yes' : 'No' }}
              </span>
            </p>
            <p v-if="res.automated_flag_reason">
              <strong>Reason:</strong> {{ res.automated_flag_reason }}
            </p>
            <p><strong>Model Version:</strong> {{ res.model_version }}</p>

            <!-- Metadata -->
            <div class="mt-3">
              <p class="font-medium text-gray-700">Metadata:</p>
              <pre class="bg-white border text-xs mt-1 p-2 rounded overflow-x-auto max-h-40"
                >{{ JSON.stringify(res.analysis_metadata, null, 2) }}
              </pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-4 border-t mt-6">
        <div class="flex gap-4">
          <button
            @click="handleAction('approve')"
            :disabled="processing"
            class="bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded disabled:opacity-50"
          >
            Approve
          </button>
          <button
            @click="handleAction('reject')"
            :disabled="processing"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded disabled:opacity-50"
          >
            Reject
          </button>
          <button
            @click="handleAction('flag')"
            :disabled="processing"
            class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold px-4 py-2 rounded disabled:opacity-50"
          >
            Flag
          </button>
        </div>

        <p v-if="actionMessage" class="mt-3 text-sm text-gray-700">{{ actionMessage }}</p>
      </div>
    </div>
  </div>
</template>
