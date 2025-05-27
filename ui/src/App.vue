<template>
  <div>
    <router-view />
    <NotificationToast />
  </div>
</template>

<script setup lang="ts">
import NotificationToast from '@/components/common/NotificationToast.vue'
</script>
