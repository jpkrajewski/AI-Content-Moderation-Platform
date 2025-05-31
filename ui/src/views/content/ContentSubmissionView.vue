<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import axiosInstance from '@/api/interceptors/interceptor'
import { endpoints } from '@/shared/constants/endpoints'
import { authService } from '@/features/auth/services/auth'
import { useJwtStore } from '@/stores/jwt'
import type { AxiosError } from 'axios'

const title = ref('')
const body = ref('')
const tags = ref('')
const source = ref('')
const localization = ref('en')
const images = ref<File[]>([])
const documents = ref<File[]>([])
const videos = ref<File[]>([])
const audios = ref<File[]>([])

const loading = ref(false)
const error = ref('')
const success = ref('')
const uid = ref('')
const username = ref('')
const userInitialized = ref(false)

const API_KEY = import.meta.env.VITE_API_KEY

const initializeUser = async () => {
  try {
    const jwtStore = useJwtStore()

    if (!jwtStore.isLoggedIn) {
      error.value = 'You must be logged in to submit content'
      return
    }

    const user = await authService.getCurrentUser()

    if (user && user.uid && user.username) {
      uid.value = user.uid
      username.value = user.username
      userInitialized.value = true
    } else {
      console.error('Invalid user data structure:', user)
      error.value = 'Invalid user data received from server'
    }
  } catch (e) {
    const axiosError = e as AxiosError
    console.error('Failed to get current user:', axiosError)
    if (axiosError.response?.status === 401) {
      error.value = 'Your session has expired. Please log in again.'
    } else {
      error.value = 'Failed to get user information. Please try again.'
    }
  }
}

onMounted(async () => {
  await initializeUser()
})

const localizations = [
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'pl', label: 'Polish' },
]

const handleFileChange = (event: Event, target: Ref<File[]>) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const files = Array.from(input.files)
    target.value = [...target.value, ...files]
  }
}

const removeFile = (index: number, target: Ref<File[]>) => {
  target.value = target.value.filter((_, i) => i !== index)
}

const handleImageChange = (e: Event) => {
  handleFileChange(e, images)
  // Reset input value to allow selecting the same file again
  const input = e.target as HTMLInputElement
  input.value = ''
}

const handleDocumentChange = (e: Event) => {
  handleFileChange(e, documents)
  // Reset input value to allow selecting the same file again
  const input = e.target as HTMLInputElement
  input.value = ''
}

const handleVideoChange = (e: Event) => {
  handleFileChange(e, videos)
  const input = e.target as HTMLInputElement
  input.value = ''
}

const handleAudioChange = (e: Event) => {
  handleFileChange(e, audios)
  const input = e.target as HTMLInputElement
  input.value = ''
}

const handleRemoveImage = (index: number) => removeFile(index, images)
const handleRemoveDocument = (index: number) => removeFile(index, documents)
const handleRemoveVideo = (index: number) => removeFile(index, videos)
const handleRemoveAudio = (index: number) => removeFile(index, audios)

const handleSubmit = async () => {
  if (!userInitialized.value) {
    error.value = 'Please wait while we load your user information.'
    return
  }

  if (!uid.value || !username.value) {
    error.value = 'User information is missing. Please refresh the page and try again.'
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const tagArray = tags.value
      .split(',')
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0)

    const sourceArray = source.value
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0)

    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('body', body.value)
    formData.append('tags', JSON.stringify(tagArray))
    formData.append('source', sourceArray.join(','))
    formData.append('localization', localization.value)
    formData.append('user_id', uid.value)
    formData.append('username', username.value)
    formData.append('timestamp', Date.now().toString())
    ;[...images.value].forEach((file) => {
      formData.append('images', file)
    })
    ;[...documents.value].forEach((file) => {
      formData.append('documents', file)
    })
    ;[...videos.value].forEach((file) => {
      formData.append('videos', file)
    })
    ;[...audios.value].forEach((file) => {
      formData.append('audios', file)
    })

    const response = await axiosInstance.post(endpoints.moderation.submitContent, formData, {
      headers: {
        'X-API-Key': API_KEY,
      },
    })

    if (response.data) {
      success.value = 'Content submitted successfully!'
      title.value = ''
      body.value = ''
      tags.value = ''
      source.value = ''
      localization.value = 'en'
      images.value = []
      documents.value = []
      videos.value = []
      audios.value = []
    }
  } catch (e) {
    error.value = 'Failed to submit content. Please try again.'
    console.error('Content submission error:', e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="bg-white rounded-2xl shadow-xl p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Submit Content for Moderation</h1>
      <p class="mb-6 text-gray-600">
        Submit text, tags, files, and metadata for moderation processing.
      </p>

      <div v-if="error" class="mb-6 bg-red-50 text-red-600 p-4 rounded-lg">{{ error }}</div>
      <div v-if="success" class="mb-6 bg-green-50 text-green-600 p-4 rounded-lg">{{ success }}</div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block mb-1 font-medium text-gray-700">Title</label>
          <input
            v-model="title"
            type="text"
            required
            placeholder="Post title"
            class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Content</label>
          <textarea
            v-model="body"
            rows="5"
            required
            placeholder="Enter your content..."
            class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"
          ></textarea>
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Tags (comma-separated)</label>
          <input
            v-model="tags"
            type="text"
            placeholder="e.g., news, politics"
            class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Source</label>
          <input
            v-model="source"
            type="text"
            required
            placeholder="e.g., acme_corp"
            class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Language</label>
          <select
            v-model="localization"
            class="w-full px-4 py-2 border rounded-lg border-gray-300 focus:ring focus:ring-blue-500"
          >
            <option v-for="lang in localizations" :key="lang.value" :value="lang.value">
              {{ lang.label }}
            </option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium text-gray-700">Upload Images</label>
          <label
            class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700"
          >
            Choose Images
            <input
              type="file"
              accept="image/*"
              multiple
              @change="handleImageChange"
              class="hidden"
            />
          </label>
          <div v-if="images.length > 0" class="mt-2">
            <p class="text-sm text-gray-600 mb-2">Selected images:</p>
            <ul class="space-y-2">
              <li
                v-for="(file, index) in images"
                :key="index"
                class="flex items-center justify-between bg-gray-50 p-2 rounded"
              >
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <button
                  @click="() => handleRemoveImage(index)"
                  class="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div class="mt-4">
          <label class="block mb-1 font-medium text-gray-700">Upload Documents</label>
          <label
            class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700"
          >
            Choose Documents
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              multiple
              @change="handleDocumentChange"
              class="hidden"
            />
          </label>
          <div v-if="documents.length > 0" class="mt-2">
            <p class="text-sm text-gray-600 mb-2">Selected documents:</p>
            <ul class="space-y-2">
              <li
                v-for="(file, index) in documents"
                :key="index"
                class="flex items-center justify-between bg-gray-50 p-2 rounded"
              >
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <button
                  @click="() => handleRemoveDocument(index)"
                  class="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div class="mt-4">
          <label class="block mb-1 font-medium text-gray-700">Upload Videos</label>
          <label
            class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700"
          >
            Choose Videos
            <input
              type="file"
              accept="video/*"
              multiple
              @change="handleVideoChange"
              class="hidden"
            />
          </label>
          <div v-if="videos.length > 0" class="mt-2">
            <p class="text-sm text-gray-600 mb-2">Selected videos:</p>
            <ul class="space-y-2">
              <li
                v-for="(file, index) in videos"
                :key="index"
                class="flex items-center justify-between bg-gray-50 p-2 rounded"
              >
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <button
                  @click="() => handleRemoveVideo(index)"
                  class="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div class="mt-4">
          <label class="block mb-1 font-medium text-gray-700">Upload Audios</label>
          <label
            class="w-1/3 bg-blue-600 text-white py-3 px-4 rounded-lg inline-block text-center cursor-pointer hover:bg-blue-700"
          >
            Choose Audios
            <input
              type="file"
              accept="audio/*"
              multiple
              @change="handleAudioChange"
              class="hidden"
            />
          </label>
          <div v-if="audios.length > 0" class="mt-2">
            <p class="text-sm text-gray-600 mb-2">Selected audios:</p>
            <ul class="space-y-2">
              <li
                v-for="(file, index) in audios"
                :key="index"
                class="flex items-center justify-between bg-gray-50 p-2 rounded"
              >
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <button
                  @click="() => handleRemoveAudio(index)"
                  class="text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading || !body || !title || !source"
            class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <span v-if="loading">Submitting...</span>
            <span v-else>Submit Content</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
