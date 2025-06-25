import { createRouter, createWebHistory } from 'vue-router'
import { useJwtStore } from '@/features/auth/stores/jwt'
import GlobalLayout from '../components/layout/GlobalLayout.vue'

import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import AuthCallbackView from '@/views/auth/0AuthCallbackView.vue'

import DashboardSummary from '../views/dashboard/DashboardSummary.vue'

import ModerationListPending from '../views/moderation/ModerationListPending.vue'
import ModerationContentAnalysis from '../views/moderation/ModerationContentAnalysis.vue'
import ContentSubmissionView from '../views/content/ContentSubmissionView.vue'
import ApiKeysView from '@/views/apiKeys/ApiKeysView.vue'

import { isJwtValid } from '@/shared/utils/jwt'
import { authService } from '@/features/auth/services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
      meta: { requiresAuth: false },
    },
    {
      path: '/oauth/callback',
      name: 'OAuthCallback',
      component: AuthCallbackView,
      meta: { requiresAuth: false },
    },

    {
      path: '/',
      component: GlobalLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'secure/dashboard/summary',
          name: 'DashboardSummary',
          component: DashboardSummary,
        },
        {
          path: 'secure/moderation/pending',
          name: 'ModerationListPending',
          component: ModerationListPending,
        },
        {
          path: 'secure/moderation/content-analysis/:contentId',
          name: 'ModerationContentAnalysis',
          component: ModerationContentAnalysis,
          props: true,
        },
        {
          path: 'secure/content/submit',
          name: 'ContentSubmission',
          component: ContentSubmissionView,
        },
        {
          path: 'secure/api-keys',
          name: 'ApiKeys',
          component: ApiKeysView,
        },
        {
          path: '',
          redirect: 'secure/dashboard/summary',
        },
      ],
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const jwtStore = useJwtStore()

  const jwtLocal = localStorage.getItem('jwt') || ''
  const refreshLocal = localStorage.getItem('refresh_token') || ''
  jwtStore.jwt = jwtLocal
  jwtStore.refreshToken = refreshLocal

  if (requiresAuth) {
    if (!jwtStore.jwt || !jwtStore.refreshToken || !isJwtValid(jwtStore.jwt)) {
      if (jwtStore.refreshToken) {
        try {
          const data = await authService.refreshToken(jwtStore.refreshToken)
          jwtStore.setTokens(data.token, data.refresh)
          next()
          return
        } catch {
          jwtStore.clearTokens()
          next({ path: '/login' })
          return
        }
      }
      jwtStore.clearTokens()
      next({ path: '/login' })
      return
    }
  }
  next()
})

export default router
