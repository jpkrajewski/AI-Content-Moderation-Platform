<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h3 class="text-lg font-medium mb-4 text-gray-900">Moderation Statuses</h3>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="status in statuses"
        :key="status.name"
        class="bg-gray-50 rounded-lg p-4"
        :class="status.class"
      >
        <div class="text-sm font-medium">{{ status.name }}</div>
        <div class="mt-1 text-3xl font-semibold">{{ status.count }}</div>
      </div>
    </div>
    <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="text-sm font-medium text-gray-500">Auto-Flag Accuracy</div>
        <div class="mt-1 text-2xl font-semibold text-gray-900">
          {{ (autoFlagAccuracy * 100).toFixed(1) }}%
        </div>
      </div>
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="text-sm font-medium text-gray-500">False Positive Rate</div>
        <div class="mt-1 text-2xl font-semibold text-gray-900">
          {{ (falsePositiveRate * 100).toFixed(1) }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  statuses: Array<{
    name: string
    count: number
    class: string
  }>
  autoFlagAccuracy: number
  falsePositiveRate: number
}>()
</script>
