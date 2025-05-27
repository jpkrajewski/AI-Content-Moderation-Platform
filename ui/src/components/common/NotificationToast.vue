<template>
  <div class="fixed top-4 right-4 z-50 space-y-4">
    <TransitionGroup name="notification">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="bg-white rounded-lg shadow-lg transform transition-all duration-300 ease-in-out"
        :class="{
          'border-l-4 border-green-400': notification.type === 'success',
          'border-l-4 border-red-400': notification.type === 'error',
          'border-l-4 border-yellow-400': notification.type === 'warning',
          'border-l-4 border-blue-400': notification.type === 'info',
        }"
      >
        <div class="flex items-center p-4">
          <div class="flex-shrink-0">
            <component
              :is="iconForType(notification.type)"
              class="w-6 h-6"
              :class="{
                'text-green-400': notification.type === 'success',
                'text-red-400': notification.type === 'error',
                'text-yellow-400': notification.type === 'warning',
                'text-blue-400': notification.type === 'info',
              }"
            />
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-900">
              {{ notification.message }}
            </p>
          </div>
          <button
            @click="removeNotification(notification.id)"
            class="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-500 focus:outline-none"
          >
            <span class="sr-only">Close</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/stores/notification'
import type { NotificationType } from '@/shared/types/notification'
import { computed } from 'vue'

defineOptions({
  name: 'NotificationToast',
})

const notificationStore = useNotificationStore()
const notifications = computed(() => notificationStore.notifications)
const removeNotification = notificationStore.removeNotification

const iconForType = (type: NotificationType) => {
  switch (type) {
    case 'success':
      return 'CheckCircleIcon'
    case 'error':
      return 'XCircleIcon'
    case 'warning':
      return 'ExclamationCircleIcon'
    case 'info':
      return 'InformationCircleIcon'
    default:
      return 'InformationCircleIcon'
  }
}
</script>

<style>
.notification-enter-active,
.notification-leave-active {
  @apply transition-all duration-300 ease-in-out;
}

.notification-enter-from {
  @apply opacity-0 translate-x-8;
}

.notification-leave-to {
  @apply opacity-0 translate-x-8;
}
</style>
