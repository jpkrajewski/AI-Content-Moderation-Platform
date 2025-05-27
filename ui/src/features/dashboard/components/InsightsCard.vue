<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
      <div class="flex items-center">
        <span class="text-sm text-gray-500">{{ description }}</span>
        <span
          class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
          :class="trendClass"
        >
          {{ trend }}
        </span>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="(section, index) in sections" :key="index">
        <h4 class="font-semibold mb-2">{{ section.title }}</h4>
        <ul class="list-disc list-inside">
          <li v-for="(value, key) in section.data" :key="key">{{ key }}: {{ value }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Section } from '../types/dashboard'

defineProps<{
  title: string
  description: string
  trend: string
  trendClass: string
  sections: Section[]
}>()
</script>
