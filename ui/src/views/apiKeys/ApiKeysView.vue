<template>
    <div class="min-h-screen bg-gray-50">
        <div class="px-8 py-12">
            <div class="max-w-7xl mx-auto">
                <h1 class="text-4xl font-bold text-gray-900 mb-2">API Keys</h1>
                <p class="text-gray-600 text-lg">Manage your API keys for secure access to our services</p>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-8 -mt-8">
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="flex justify-between items-center mb-8">
                    <h2 class="text-2xl font-semibold text-gray-900">Your API Keys</h2>
                    <button @click="handleCreateApiKeyClick" :disabled="loading"
                        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-all duration-200">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        <span v-if="loading">Creating...</span>
                        <span v-else>Create New API Key</span>
                    </button>
                </div>

                <div v-if="loading" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>

                <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-red-700">{{ error }}</p>
                        </div>
                    </div>
                </div>

                <div v-if="apiKeys.length > 0 && !loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="key in apiKeys" :key="key.id"
                        class="bg-white rounded-xl border border-gray-200 hover:border-blue-200 transition-all duration-200 overflow-hidden">
                        <div class="p-6">
                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center">
                                    <div class="h-10 w-10 rounded-full flex items-center justify-center" :class="{
                                        'bg-green-100 text-green-600': key.is_active,
                                        'bg-red-100 text-red-600': !key.is_active,
                                    }">
                                        <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                                            <path
                                                d="M7 5C3.1545455 5 0 8.1545455 0 12C0 15.845455 3.1545455 19 7 19C9.7749912 19 12.089412 17.314701 13.271484 15L16 15L16 18L22 18L22 15L24 15L24 9L23 9L13.287109 9C12.172597 6.6755615 9.8391582 5 7 5zM7 7C9.2802469 7 11.092512 8.4210017 11.755859 10.328125L11.988281 11L22 11L22 13L20 13L20 16L18 16L18 13L12.017578 13L11.769531 13.634766C11.010114 15.575499 9.1641026 17 7 17C4.2454545 17 2 14.754545 2 12C2 9.2454545 4.2454545 7 7 7zM7 9C5.3549904 9 4 10.35499 4 12C4 13.64501 5.3549904 15 7 15C8.6450096 15 10 13.64501 10 12C10 10.35499 8.6450096 9 7 9zM7 11C7.5641294 11 8 11.435871 8 12C8 12.564129 7.5641294 13 7 13C6.4358706 13 6 12.564129 6 12C6 11.435871 6.4358706 11 7 11z" />
                                        </svg>
                                    </div>
                                    <span class="ml-3 px-3 py-1 rounded-full text-sm font-medium" :class="{
                                        'bg-green-100 text-green-800': key.is_active,
                                        'bg-red-100 text-red-800': !key.is_active || key.status === 'deleted',
                                    }">
                                        {{ key.is_active ? 'Active' : 'Inactive' }}
                                    </span>
                                </div>
                                <div class="flex space-x-2">
                                    <button v-if="key.is_active" @click="() => handleDeactivateApiKey(key.id)"
                                        class="text-green-400 hover:text-green-600 transition-colors duration-200"
                                        title="Deactivate Key">
                                        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                                            <line x1="12" y1="2" x2="12" y2="12"></line>
                                        </svg>
                                    </button>
                                    <button v-if="!key.is_active" @click="() => handleReactivateApiKey(key.id)"
                                        class="text-red-400 hover:text-red-600 transition-colors duration-200"
                                        title="Reactivate Key">
                                        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                                            <line x1="12" y1="2" x2="12" y2="12"></line>
                                        </svg>
                                    </button>
                                    <button v-if="key.status !== 'deleted'" @click="() => handleDeleteApiKey(key.id)"
                                        class="text-red-400 hover:text-red-600 transition-colors duration-200"
                                        title="Delete Key">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </div>

                            <div class="mb-4 text-sm text-gray-700 space-y-1">
                                <p><strong>Source:</strong> {{ key.source }}</p>
                                <p><strong>Access Count:</strong> {{ key.access_count }}</p>
                                <p><strong>Scopes:</strong> {{ key.current_scope.join(', ') }}</p>
                            </div>

                            <div class="bg-gray-50 rounded-lg p-4 mb-4">
                                <div class="flex items-center justify-between">
                                    <code class="text-sm font-mono text-gray-700 break-all">{{ key.api_key }}</code>
                                    <button @click="() => copyApiKey(key.api_key)"
                                        class="ml-3 text-gray-400 hover:text-gray-600 focus:outline-none flex-shrink-0"
                                        title="Copy API Key">
                                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 002 2h2a2 2 0 002-2" />
                                        </svg>
                                    </button>
                                </div>
                            </div>

                            <div class="text-sm text-gray-500">
                                Created {{ new Date(key.created_at).toLocaleDateString() }}
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else-if="!loading && !error" class="text-center py-12">
                    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 7a2 2 0 012 2v5a2 2 0 01-2 2H9a2 2 0 01-2-2V9a2 2 0 012-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v2M9 7h6" />
                    </svg>
                    <h3 class="mt-2 text-sm font-medium text-gray-900">No API keys</h3>
                    <p class="mt-1 text-sm text-gray-500">Get started by creating a new API key.</p>
                </div>
            </div>
        </div>

        <div v-if="copied"
            class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 ease-in-out">
            <div class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Copied to clipboard!
            </div>
        </div>

        <!-- Add Modal -->
        <div v-if="showCreateModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4"
            @click="showCreateModal = false">
            <div class="bg-white rounded-lg p-8 max-w-md w-full shadow-2xl" @click.stop>
                <h3 class="text-2xl font-semibold text-gray-800 mb-6">Create New API Key</h3>

                <form @submit.prevent="handleCreateApiKey">
                    <div class="space-y-5">
                        <div>
                            <label for="source" class="block text-sm font-medium text-gray-700 mb-1">Source</label>
                            <input type="text" id="source" v-model="newApiKey.source"
                                class="block w-full rounded-md border-gray-400 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2"
                                required />
                        </div>

                        <div>
                            <label for="clientId" class="block text-sm font-medium text-gray-700 mb-1">Client ID</label>
                            <input type="text" id="clientId" v-model="newApiKey.client_id"
                                class="block w-full rounded-md border-gray-400 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2"
                                required />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Scopes</label>
                            <div class="space-y-2">
                                <label class="inline-flex items-center">
                                    <input type="checkbox" v-model="newApiKey.current_scope" value="create_content"
                                        class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
                                    <span class="ml-2 text-sm text-gray-700">Create Content</span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 flex justify-end space-x-4">
                        <button type="button" @click="showCreateModal = false"
                            class="px-5 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Cancel
                        </button>
                        <button type="submit" :disabled="loading"
                            class="px-5 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                            {{ loading ? 'Creating...' : 'Create' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiKeysService } from '@/features/apiKeys/api/apiKeysService'
import type { ApiKey } from '@/features/apiKeys/types'

const apiKeys = ref<ApiKey[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const copied = ref(false)
const showCreateModal = ref(false)
const newApiKey = ref({
    source: '',
    client_id: '',
    current_scope: [] as string[]
})

const handleFetchApiKeys = async () => {
    loading.value = true
    error.value = null
    try {
        apiKeys.value = await apiKeysService.fetchApiKeys()
    } catch (err) {
        error.value = 'Failed to fetch API keys.'
        console.error(err)
    } finally {
        loading.value = false
    }
}

const handleCreateApiKey = async () => {
    loading.value = true
    error.value = null
    try {
        await apiKeysService.createApiKey(newApiKey.value)
        showCreateModal.value = false
        // Reset form
        newApiKey.value = {
            source: '',
            client_id: '',
            current_scope: []
        }
        handleFetchApiKeys() // Refresh the list after creation
    } catch (err) {
        error.value = 'Failed to create API key.'
        console.error(err)
    } finally {
        loading.value = false
    }
}

const handleDeactivateApiKey = async (id: string) => {
    loading.value = true
    error.value = null
    try {
        await apiKeysService.deactivateApiKey(id)
        handleFetchApiKeys() // Refresh the list after deactivation
    } catch (err) {
        error.value = `Failed to deactivate API key ${id}.`
        console.error(err)
    } finally {
        loading.value = false
    }
}

const handleReactivateApiKey = async (id: string) => {
    loading.value = true
    error.value = null
    try {
        await apiKeysService.reactivateApiKey(id)
        handleFetchApiKeys() // Refresh the list after reactivation
    } catch (err) {
        error.value = `Failed to reactivate API key ${id}.`
        console.error(err)
    } finally {
        loading.value = false
    }
}

const handleDeleteApiKey = async (id: string) => {
    loading.value = true
    error.value = null
    try {
        await apiKeysService.deleteApiKey(id)
        handleFetchApiKeys() // Refresh the list after deletion
    } catch (err) {
        error.value = `Failed to delete API key ${id}.`
        console.error(err)
    } finally {
        loading.value = false
    }
}

const copyApiKey = async (apiKey: string) => {
    try {
        await navigator.clipboard.writeText(apiKey)
        copied.value = true
        setTimeout(() => {
            copied.value = false
        }, 2000) // Hide message after 2 seconds
    } catch (err) {
        console.error('Failed to copy API key:', err)
        // TODO: Display copy error message to user
    }
}

const handleCreateApiKeyClick = () => {
    showCreateModal.value = true
}

onMounted(() => {
    handleFetchApiKeys()
})
</script>
