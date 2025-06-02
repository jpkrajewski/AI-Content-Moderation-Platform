import { createRouter, createWebHistory } from 'vue-router'
import { useJwtStore } from '@/stores/jwt'
import GlobalLayout from '../components/layout/GlobalLayout.vue'

import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import AuthCallbackView from '@/views/auth/0AuthCallbackView.vue'

import DashboardSummary from '../views/dashboard/DashboardSummary.vue'

import ModerationListPending from '../views/moderation/ModerationListPending.vue'
import ModerationContentAnalysis from '../views/moderation/ModerationContentAnalysis.vue'
import ContentSubmissionView from '../views/content/ContentSubmissionView.vue'
import ApiKeysView from '@/views/apiKeys/ApiKeysView.vue'

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

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const jwtStore = useJwtStore()

  if (requiresAuth && !jwtStore.isLoggedIn) {
    next({ path: '/login' })
  } else if (!requiresAuth && jwtStore.isLoggedIn && to.path === '/login') {
    next({ path: '/secure/dashboard/summary' })
  } else {
    next()
  }
})

export default router
