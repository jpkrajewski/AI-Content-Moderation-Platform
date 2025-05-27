<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <h3 class="text-lg font-medium text-gray-900">Peak Hours</h3>
      <div class="mt-4">
        <div
          v-for="hour in peakHours"
          :key="hour.hour"
          class="flex items-center justify-between py-2"
        >
          <span class="text-sm text-gray-500">{{ hour.hour }}</span>
          <div class="flex items-center">
            <div class="w-32 bg-gray-200 rounded-full h-2.5">
              <div
                class="bg-blue-600 h-2.5 rounded-full"
                :style="{ width: `${(hour.count / maxCount) * 100}%` }"
              ></div>
            </div>
            <span class="ml-2 text-sm font-medium text-gray-900">{{ hour.count }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  peakHours: Array<{ hour: string; count: number }>
}>()

const maxCount = computed(() => Math.max(...props.peakHours.map((h) => h.count)))
</script>
