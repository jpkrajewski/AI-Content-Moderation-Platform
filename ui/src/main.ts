import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useVersionStore } from '@/stores/version'
import { useJwtStore } from '@/features/auth/stores/jwt'
import { authService } from '@/features/auth/services/auth'
import router from '@/router'

import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
const versionStore = useVersionStore()
versionStore.fetchVersion()

const jwtStore = useJwtStore()

async function silentRefreshIfNeeded() {
  if (jwtStore.jwt && jwtStore.refreshToken) {
    try {
      const data = await authService.refreshToken(jwtStore.refreshToken)
      jwtStore.setTokens(data.token, data.refresh)
    } catch {
      jwtStore.clearTokens()
      router.push('/login')
    }
  } else if (jwtStore.jwt && !jwtStore.refreshToken) {
    jwtStore.clearTokens()
    router.push('/login')
  }
}

silentRefreshIfNeeded().then(() => {
  app.use(router)
  app.mount('#app')
})
