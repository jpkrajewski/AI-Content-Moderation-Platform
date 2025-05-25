<script setup lang="ts">
import { ref } from 'vue';
import axiosInstance from '@/services/interceptor.ts';
import endpoints from '@/services/endpoints.ts';

const title = ref('');
const body = ref('');
const tags = ref('');
const source = ref('');
const localization = ref('en');
const images = ref<File[]>([]);
const documents = ref<File[]>([]);

const loading = ref(false);
const error = ref('');
const success = ref('');
const userId = ref('06826a12-e7e5-47a7-bbcd-61b31b897ccd');
const username = ref('admin');

const API_KEY = 'JRGnmGwJ!)KShUUgDv5dz1uOl&2';

const localizations = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'pl', label: 'Polish' }
];

const handleFileChange = (event: Event, target: typeof images | typeof documents) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    target.value = Array.from(input.files);
  }
};

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

    images.value.forEach(file => {
      formData.append('images', file);
    });

    documents.value.forEach(file => {
      formData.append('documents', file);
    });

    await axiosInstance.post(endpoints.moderation.submitContent, formData, {
      headers: {
        'X-API-Key': API_KEY,
        'content-type': 'multipart-data'
      },
    });

    success.value = 'Content submitted successfully!';
    // Clear form
    title.value = '';
    body.value = '';
    tags.value = '';
    source.value = '';
    localization.value = 'en';
    images.value = [];
    documents.value = [];

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
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Submit Content for Moderation</h1>
      <p class="mb-6 text-gray-600">Submit text, tags, files, and metadata for moderation processing.</p>

      <div v-if="error" class="mb-6 bg-red-50 text-red-600 p-4 rounded-lg">{{ error }}</div>
      <div v-if="success" class="mb-6 bg-green-50 text-green-600 p-4 rounded-lg">{{ success }}</div>

      <form @submit.prevent="handleSubmit" class="space-y-6">

        <div>
          <label class="block mb-1 font-medium text-gray-700">Title</label>
          <input v-model="title" type="text" required placeholder="Post title"
                 class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500" />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Content</label>
          <textarea v-model="body" rows="5" required
                    placeholder="Enter your content..."
                    class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"></textarea>
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Tags (comma-separated)</label>
          <input v-model="tags" type="text"
                 placeholder="e.g., news, politics"
                 class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500" />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Source</label>
          <input v-model="source" type="text" required
                 placeholder="e.g., acme_corp"
                 class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500" />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Language</label>
          <select v-model="localization" class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500">
            <option v-for="lang in localizations" :key="lang.value" :value="lang.value">{{ lang.label }}</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Upload Images</label>
          <label class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700">
            Choose Images
            <input type="file" accept="image/*" multiple @change="e => handleFileChange(e, images)" class="hidden" />
          </label>
        </div>

        <div class="mt-4">
          <label class="block mb-1 font-medium text-gray-700">Upload Documents</label>
          <label class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700">
            Choose Documents
            <input type="file" accept=".pdf,.doc,.docx" multiple @change="e => handleFileChange(e, documents)" class="hidden" />
          </label>
        </div>

        <div>
          <button type="submit" :disabled="loading || !body || !title || !source"
                  class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            <span v-if="loading">Submitting...</span>
            <span v-else>Submit Content</span>
          </button>
        </div>

      </form>
    </div>
  </div>
</template>
