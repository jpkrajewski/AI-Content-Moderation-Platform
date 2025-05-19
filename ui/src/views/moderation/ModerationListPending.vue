<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listPendingContent } from '@/services/moderation';
import { useRouter } from 'vue-router';
import { ContentItem } from '@/models/moderation';

const router = useRouter();
const contentItems = ref<ContentItem[]>([]);
const selectedItem = ref<ContentItem | null>(null);
const loading = ref(true);
const error = ref('');

const fetchPendingContent = async () => {
  try {
    const data = await listPendingContent();
    contentItems.value = data;
  } catch {
    error.value = 'Failed to fetch moderation content.';
  } finally {
    loading.value = false;
  }
};

const openItem = (item: ContentItem) => {
  selectedItem.value = item;
};

const openItemRedirect = (item: ContentItem) => {
  router.push({ name: 'ModerationContentAnalysis', params: { contentId: item.id } });
};

const closeModal = () => {
  selectedItem.value = null;
};
onMounted(() => {
  fetchPendingContent();
});
</script>

<template>
  <div class="p-8 max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Pending Moderation</h1>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="error" class="text-red-600">{{ error }}</div>

    <!-- Summary cards -->
    <div v-else class="grid grid-cols-1 gap-6">
      <div
        v-for="item in contentItems"
        :key="item.id"
        class="bg-white border border-gray-200 rounded-xl shadow transition p-6"
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
              'bg-red-100 text-red-800': item.status === 'rejected'
            }"
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
        <div>
          <button
            @click="openItemRedirect(item)"
            class="bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium px-4 py-2 rounded mr-2"
          >
            View Analysis
          </button>
        </div>

        <div class="text-right">
          <button
            @click="openItem(item)"
            class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded"
          >
            View Details
          </button>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <div
      v-if="selectedItem"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center px-4"
    >
      <div class="bg-white max-w-3xl w-full rounded-xl shadow-xl p-6 relative overflow-y-auto max-h-[90vh]">
        <button @click="closeModal" class="absolute top-2 right-4 text-gray-600 hover:text-black text-2xl">×</button>

        <h2 class="text-xl font-bold mb-2">Content ID: {{ selectedItem.id }}</h2>
        <p class="text-sm text-gray-500 mb-2">
          Created: {{ new Date(selectedItem.created_at).toLocaleString() }}
        </p>
        <p class="mb-4 text-gray-700 whitespace-pre-wrap">{{ selectedItem.body }}</p>

        <!-- Tags -->
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

        <!-- Analysis -->
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
            <p v-if="res.automated_flag_reason"><strong>Reason:</strong> {{ res.automated_flag_reason }}</p>
            <p><strong>Model Version:</strong> {{ res.model_version }}</p>

            <!-- Metadata -->
            <div class="mt-2">
              <p class="font-medium text-gray-600">Metadata:</p>
              <pre class="bg-gray-50 p-2 rounded border border-gray-200 text-xs overflow-x-auto">
{{ JSON.stringify(res.analysis_metadata, null, 2) }}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
