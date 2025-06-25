import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useJwtStore = defineStore('jwt', () => {
  const jwt = ref(localStorage.getItem('jwt') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')

  const isLoggedIn = computed(() => !!jwt.value)

  const setJwt = (token: string) => {
    jwt.value = token
    localStorage.setItem('jwt', token)
  }

  const setRefreshToken = (token: string) => {
    refreshToken.value = token
    localStorage.setItem('refresh_token', token)
  }

  const setTokens = (access: string, refresh: string) => {
    setJwt(access)
    setRefreshToken(refresh)
  }

  const clearJwt = () => {
    jwt.value = ''
    localStorage.removeItem('jwt')
  }

  const clearRefreshToken = () => {
    refreshToken.value = ''
    localStorage.removeItem('refresh_token')
  }

  const clearTokens = () => {
    clearJwt()
    clearRefreshToken()
  }

  return {
    jwt,
    refreshToken,
    isLoggedIn,
    setJwt,
    setRefreshToken,
    setTokens,
    clearJwt,
    clearRefreshToken,
    clearTokens,
  }
})
