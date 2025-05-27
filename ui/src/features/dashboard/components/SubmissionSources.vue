<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <h3 class="text-lg font-medium text-gray-900">Submission Sources</h3>
      <div class="mt-4">
        <div
          v-for="source in sources"
          :key="source.name"
          class="flex items-center justify-between py-2"
        >
          <span class="text-sm text-gray-500">{{ source.name }}</span>
          <span class="text-sm font-medium text-gray-900">{{ source.count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  sources: Array<{ name: string; count: number }>
}>()
</script>
