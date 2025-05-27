import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useJwtStore = defineStore('jwt', () => {
  const jwt = ref(localStorage.getItem('jwt') || '')

  const isLoggedIn = computed(() => !!jwt.value)

  const setJwt = (token: string) => {
    jwt.value = token
    localStorage.setItem('jwt', token)
  }

  const clearJwt = () => {
    jwt.value = ''
    localStorage.removeItem('jwt')
  }

  return { jwt, isLoggedIn, setJwt, clearJwt }
})
