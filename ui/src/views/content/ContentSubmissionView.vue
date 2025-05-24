<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '@/services/interceptor.ts';
import endpoints from '@/services/endpoints.ts';

const title = ref('Example');
const body = ref('');
const tags = ref('');
const source = ref('');
const localization = ref('en');
const loading = ref(false);
const error = ref('');
const success = ref('');
const userId = ref('06826a12-e7e5-47a7-bbcd-61b31b897ccd')
const username = ref('admin')

const API_KEY = 'sk_test_51NxYz2KJ8L9mP4qR3vW7tB2cF5hM8n';

const localizations = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'pl', label: 'Polish' }
];

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  success.value = '';

  try {
    const tagArray = tags.value
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0);

    const sourceArray = source.value
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('body', body.value);
    formData.append('tags', JSON.stringify(tagArray));
    formData.append('source', sourceArray.join(','));
    formData.append('localization', localization.value);
    formData.append('user_id', userId.value);
    formData.append('username', username.value);
    formData.append('timestamp', new Date().toISOString());

    await axiosInstance.post(endpoints.moderation.submitContent, formData, {
      headers: {
        'X-API-Key': API_KEY,
      },
    });

    success.value = 'Content submitted successfully! It will appear in the moderation queue.';
    
    body.value = '';
    tags.value = '';
    source.value = '';
    localization.value = 'en';

  } catch (e) {
    error.value = 'Failed to submit content. Please try again.';
    console.error('Content submission error:', e);
  } finally {
    loading.value = false;
  }
};

</script>

<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="bg-white rounded-2xl shadow-xl p-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Submit Content for Moderation</h1>
        <p class="mt-2 text-gray-600">
          Use this form to submit content for testing the moderation system. Your submission will appear in the moderation queue.
        </p>
      </div>

      <div v-if="error" class="mb-6 bg-red-50 text-red-600 p-4 rounded-lg">
        {{ error }}
      </div>

      <div v-if="success" class="mb-6 bg-green-50 text-green-600 p-4 rounded-lg">
        {{ success }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="body" class="block text-sm font-medium text-gray-700 mb-1">
            Content
          </label>
          <textarea
            id="content"
            v-model="body"
            rows="6"
            required
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Enter your text content here... You can include text, image URLs, and video URLs in your post."
          ></textarea>
        </div>

        <div>
          <label for="tags" class="block text-sm font-medium text-gray-700 mb-1">
            Tags (comma-separated)
          </label>
          <input
            id="tags"
            v-model="tags"
            type="text"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="e.g., news, politics, sports"
          />
        </div>

        <div>
          <label for="source" class="block text-sm font-medium text-gray-700 mb-1">
            Source
          </label>
          <input
            id="source"
            v-model="source"
            type="text"
            required
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="e.g., website name, social media platform"
          />
        </div>

        <div>
          <label for="localization" class="block text-sm font-medium text-gray-700 mb-1">
            Language
          </label>
          <select
            id="localization"
            v-model="localization"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option v-for="lang in localizations" :key="lang.value" :value="lang.value">
              {{ lang.label }}
            </option>
          </select>
        </div>

        <div class="pt-4">
          <button
            type="submit"
            :disabled="loading || !body"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Content</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template> 