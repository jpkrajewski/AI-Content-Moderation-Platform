<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { listPendingContent, getModerationInfo } from '@/features/moderation/services/moderation'
import { useRouter } from 'vue-router'
import type { ContentItem } from '@/features/moderation/types/moderation'
import { usePendingCountStore } from '@/stores/pendingCount'
import { useDebounceFn } from '@vueuse/core'

const router = useRouter()
const pendingCountStore = usePendingCountStore()
const contentItems = ref<ContentItem[]>([])
const selectedItem = ref<ContentItem | null>(null)
const loading = ref<boolean>(true)
const error = ref<string | undefined>('')
const currentPage = ref<number>(1)
const totalPages = ref<number>(0)
const PAGE_SIZE: number = 10
const MAX_RETRIES: number = 3

const contentCache = ref<Record<number, ContentItem[]>>({})
const moderationInfoCache = ref<{ pending_count: number } | null>(null)
const lastFetchTime = ref<Record<number, number>>({})
const CACHE_DURATION = 5 * 60 * 1000

const currentPageContent = computed(() => {
  const cachedContent = contentCache.value[currentPage.value]
  const lastFetch = lastFetchTime.value[currentPage.value]

  if (cachedContent && lastFetch && Date.now() - lastFetch < CACHE_DURATION) {
    return cachedContent
  }
  return null
})

const fetchPendingContent = async (retryCount = 0) => {
  try {
    loading.value = true
    error.value = ''

    const cachedContent = currentPageContent.value
    if (cachedContent) {
      contentItems.value = cachedContent
      loading.value = false
      return
    }

    if (!moderationInfoCache.value) {
      const moderationInfo = await getModerationInfo()
      moderationInfoCache.value = moderationInfo
      const total = Math.max(0, moderationInfo.pending_count)
      totalPages.value = Math.max(1, Math.ceil(total / PAGE_SIZE))
      pendingCountStore.count = moderationInfo.pending_count
    }

    const data = await listPendingContent({
      page: currentPage.value,
      page_size: PAGE_SIZE,
    })

    contentCache.value[currentPage.value] = data
    lastFetchTime.value[currentPage.value] = Date.now()
    contentItems.value = data
  } catch (err) {
    console.error('Error fetching content:', err)
    if (retryCount < MAX_RETRIES) {
      setTimeout(() => fetchPendingContent(retryCount + 1), Math.pow(2, retryCount) * 1000)
    } else {
      error.value = err instanceof Error ? err.message : 'Failed to fetch moderation content.'
      totalPages.value = 1
      contentItems.value = []
    }
  } finally {
    loading.value = false
  }
}

const debouncedFetchContent = useDebounceFn(fetchPendingContent, 300)

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    debouncedFetchContent()
  }
}

const openItem = (item: ContentItem) => {
  selectedItem.value = item
}

const openItemRedirect = (item: ContentItem) => {
  router.push({
    name: 'ModerationContentAnalysis',
    params: { contentId: item.id },
  })
}

const closeModal = () => {
  selectedItem.value = null
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    closeModal()
  }
}

onMounted(() => {
  fetchPendingContent()
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="p-8 max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Pending Moderation</h1>

    <div v-if="loading" class="text-gray-500" role="status" aria-live="polite">Loading...</div>
    <div v-else-if="error" class="text-red-600" role="alert">{{ error }}</div>

    <div v-else>
      <div class="grid grid-cols-1 gap-6 mb-6">
        <div
          v-for="item in contentItems"
          :key="item.id"
          class="bg-white border border-gray-200 rounded-xl shadow transition p-6 hover:shadow-lg"
        >
          <div class="flex justify-between items-center mb-2">
            <div>
              <h2 class="text-lg font-semibold text-gray-800 truncate">ID: {{ item.id }}</h2>
              <p class="text-sm text-gray-500">
                {{ new Date(item.created_at).toLocaleString() }}
              </p>
            </div>
            <span
              class="px-3 py-1 text-xs rounded-full"
              :class="{
                'bg-green-100 text-green-800': item.status === 'approved',
                'bg-yellow-100 text-yellow-800': item.status === 'pending',
                'bg-red-100 text-red-800': item.status === 'rejected',
              }"
              :aria-label="`Status: ${item.status}`"
            >
              {{ item.status }}
            </span>
          </div>

          <p class="text-sm text-gray-600 truncate mb-3">{{ item.body }}</p>

          <div class="flex flex-wrap gap-2 mb-4">
            <span
              v-for="tag in item.tags"
              :key="tag"
              class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full"
            >
              {{ tag }}
            </span>
          </div>
          <div class="flex justify-between">
            <button
              @click="openItemRedirect(item)"
              class="bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              :aria-label="`View analysis for content ${item.id}`"
            >
              View Analysis
            </button>
            <button
              @click="openItem(item)"
              class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2"
              :aria-label="`View details for content ${item.id}`"
            >
              View Details
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="totalPages > 0"
        class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6"
      >
        <div class="flex flex-1 justify-between sm:hidden">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :aria-label="`Go to previous page`"
          >
            Previous
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            :aria-label="`Go to next page`"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing
              <span class="font-medium">{{ (currentPage - 1) * PAGE_SIZE + 1 }}</span>
              to
              <span class="font-medium">{{
                Math.min(currentPage * PAGE_SIZE, totalPages * PAGE_SIZE)
              }}</span>
              of
              <span class="font-medium">{{ pendingCountStore.count }}</span>
              results
            </p>
          </div>
          <div>
            <nav
              class="isolate inline-flex -space-x-px rounded-md shadow-sm"
              aria-label="Pagination"
            >
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                :aria-label="`Go to previous page`"
              >
                <span class="sr-only">Previous</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path
                    fill-rule="evenodd"
                    d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <template v-for="page in totalPages" :key="page">
                <button
                  v-if="
                    page === 1 ||
                    page === totalPages ||
                    (page >= currentPage - 1 && page <= currentPage + 1)
                  "
                  @click="changePage(page)"
                  :class="[
                    page === currentPage
                      ? 'relative z-10 inline-flex items-center bg-blue-600 px-4 py-2 text-sm font-semibold text-white focus:z-20 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                      : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  ]"
                  :aria-label="`Go to page ${page}`"
                  :aria-current="page === currentPage ? 'page' : undefined"
                >
                  {{ page }}
                </button>
                <span
                  v-else-if="page === currentPage - 2 || page === currentPage + 2"
                  class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300 focus:outline-offset-0"
                  aria-hidden="true"
                >
                  ...
                </span>
              </template>

              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                :aria-label="`Go to next page`"
              >
                <span class="sr-only">Next</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path
                    fill-rule="evenodd"
                    d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="selectedItem"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center px-4"
      @click="closeModal"
      role="dialog"
      aria-modal="true"
      :aria-label="`Content details for ID ${selectedItem.id}`"
    >
      <div
        class="bg-white max-w-3xl w-full rounded-xl shadow-xl p-6 relative overflow-y-auto max-h-[90vh]"
        @click.stop
      >
        <button
          @click="closeModal"
          class="absolute top-2 right-4 text-gray-600 hover:text-black text-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-full p-1"
          aria-label="Close modal"
        >
          ×
        </button>

        <h2 class="text-xl font-bold mb-2">Content ID: {{ selectedItem.id }}</h2>
        <p class="text-sm text-gray-500 mb-2">
          Created: {{ new Date(selectedItem.created_at).toLocaleString() }}
        </p>
        <p class="mb-4 text-gray-700 whitespace-pre-wrap">{{ selectedItem.body }}</p>

        <div class="mb-4">
          <p class="font-medium text-gray-600">Tags:</p>
          <div class="flex flex-wrap gap-2 mt-1">
            <span
              v-for="tag in selectedItem.tags"
              :key="tag"
              class="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
            >
              {{ tag }}
            </span>
          </div>
        </div>

        <p class="text-sm text-gray-500 mb-4">
          Source: {{ selectedItem.source }} | Localization: {{ selectedItem.localization }}
        </p>

        <div v-if="selectedItem.results?.length">
          <p class="font-medium mb-2">Analysis Results:</p>
          <div
            v-for="(res, i) in selectedItem.results"
            :key="i"
            class="border-t border-gray-200 pt-3 mt-3 text-sm text-gray-700"
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

            <div class="mt-2">
              <p class="font-medium text-gray-600">Metadata:</p>
              <pre class="bg-gray-50 p-2 rounded border border-gray-200 text-xs overflow-x-auto">{{
                JSON.stringify(res.analysis_metadata, null, 2)
              }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
