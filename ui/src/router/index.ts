import { createRouter, createWebHistory } from 'vue-router';
import { useJwtStore } from '@/stores/jwt';
import GlobalLayout from '../layouts/GlobalLayout.vue';

import Login from '../views/UserLogin.vue';
import Register from '../views/UserRegister.vue';

import DashboardSummary from '../views/dashboard/DashboardSummary.vue';
import DashboardActivityMetrics from '../views/dashboard/DashboardActivityMetrics.vue';
import DashboardKPI from '../views/dashboard/DashboardKPI.vue';

import ModerationListPending from '../views/moderation/ModerationListPending.vue';
import ModerationContentAnalysis from '../views/moderation/ModerationContentAnalysis.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
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
          path: '',
          redirect: 'secure/dashboard/summary',
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const jwtStore = useJwtStore();

  if (requiresAuth && !jwtStore.isLoggedIn) {
    next({ path: '/login' });
  } else if (!requiresAuth && jwtStore.isLoggedIn && to.path === '/login') {
    next({ path: '/dashboard/summary' });
  } else {
    next();
  }
});

export default router;
