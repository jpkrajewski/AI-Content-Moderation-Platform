import { createRouter, createWebHistory } from 'vue-router'
import { useJwtStore } from '@/stores/jwt'
import GlobalLayout from '../components/layout/GlobalLayout.vue'

import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'

import DashboardSummary from '../views/dashboard/DashboardSummary.vue'
import DashboardActivityMetrics from '../views/dashboard/DashboardActivityMetrics.vue'
import DashboardKPI from '../views/dashboard/DashboardKPI.vue'

import ModerationListPending from '../views/moderation/ModerationListPending.vue'
import ModerationContentAnalysis from '../views/moderation/ModerationContentAnalysis.vue'
import ContentSubmissionView from '../views/content/ContentSubmissionView.vue'

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
          path: 'secure/dashboard/activity-metrics',
          name: 'DashboardActivityMetrics',
          component: DashboardActivityMetrics,
        },
        {
          path: 'secure/dashboard/kpi',
          name: 'DashboardKPI',
          component: DashboardKPI,
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
