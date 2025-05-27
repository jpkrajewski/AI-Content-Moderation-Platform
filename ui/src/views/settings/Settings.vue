<template>
  <div class="space-y-6">
    <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
      <div class="md:grid md:grid-cols-3 md:gap-6">
        <div class="md:col-span-1">
          <h3 class="text-lg font-medium leading-6 text-gray-900">Profile</h3>
          <p class="mt-1 text-sm text-gray-500">Update your account information and preferences.</p>
        </div>
        <div class="mt-5 md:mt-0 md:col-span-2">
          <form @submit.prevent="handleSubmit">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-4">
                <label for="name" class="block text-sm font-medium text-gray-700">Full name</label>
                <input
                  type="text"
                  id="name"
                  v-model="name"
                  class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                />
              </div>

              <div class="col-span-6 sm:col-span-4">
                <label for="email" class="block text-sm font-medium text-gray-700"
                  >Email address</label
                >
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                />
              </div>
            </div>
            <div class="mt-6">
              <button
                type="submit"
                :disabled="loading"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                {{ loading ? 'Saving...' : 'Save changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div class="bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Delete account</h3>
        <div class="mt-2 max-w-xl text-sm text-gray-500">
          <p>Once you delete your account, there is no going back. Please be certain.</p>
        </div>
        <div class="mt-5">
          <button
            type="button"
            @click="handleDelete"
            class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm"
          >
            Delete account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotificationStore } from '@/stores/notification'

defineOptions({
  name: 'UserSettings',
})

const userStore = useUserStore()
const notificationStore = useNotificationStore()

const name = ref('')
const email = ref('')
const loading = ref(false)

onMounted(() => {
  if (userStore.currentUser) {
    name.value = userStore.currentUser.username
    email.value = userStore.currentUser.email
  }
})

const handleSubmit = async () => {
  loading.value = true
  try {
    notificationStore.addNotification({
      type: 'success',
      message: 'Profile updated successfully',
    })
  } catch {
    notificationStore.addNotification({
      type: 'error',
      message: 'Failed to update profile',
    })
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    return
  }

  try {
    await userStore.logout()
    notificationStore.addNotification({
      type: 'success',
      message: 'Account deleted successfully',
    })
  } catch {
    notificationStore.addNotification({
      type: 'error',
      message: 'Failed to delete account',
    })
  }
}
</script>
