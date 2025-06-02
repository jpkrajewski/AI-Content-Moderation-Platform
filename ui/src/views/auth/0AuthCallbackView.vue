<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useJwtStore } from '@/stores/jwt'

const router = useRouter()
const route = useRoute()
const jwtStore = useJwtStore()

const token = route.query.token as string

if (token) {
  jwtStore.setJwt(token)
  router.push('/secure/dashboard/summary')
} else {
  router.push('/login')
}
</script>

<template>
  <div class="text-center mt-10 text-gray-700">Redirecting...</div>
</template>
