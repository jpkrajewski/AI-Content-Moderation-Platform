import { createRouter, createWebHistory } from 'vue-router';
import { useJwtStore } from '@/stores/jwt'; // Import the authentication utility

import Login from '../views/UserLogin.vue';
import Register from '../views/UserRegister.vue';
import GlobalLayout from '../layouts/GlobalLayout.vue';

import DashboardSummary from '../views/dashboard/DashboardSummary.vue';
import DashboardActivityMetrics from '../views/dashboard/DashboardActivityMetrics.vue';
import DashboardKPI from '../views/dashboard/DashboardKPI.vue';
import ModerationListPending from '../views/moderation/ModerationListPending.vue';
import ModerationContentAnalysis from '../views/moderation/ModerationContentAnalysis.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Public routes
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false }, // No authentication required
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: { requiresAuth: false }, // No authentication required
    },

    // Protected routes (wrapped in GlobalLayout)
    {
      path: '/secure',
      component: GlobalLayout, // Use global layout for authenticated routes
      meta: { requiresAuth: true }, // Authentication required
      children: [
        {
          path: 'dashboard/summary',
          name: 'DashboardSummary',
          component: DashboardSummary,
        },
        {
          path: 'dashboard/activity-metrics',
          name: 'DashboardActivityMetrics',
          component: DashboardActivityMetrics,
        },
        {
          path: 'dashboard/kpi',
          name: 'DashboardKPI',
          component: DashboardKPI,
        },
        {
          path: 'moderation/pending',
          name: 'ModerationListPending',
          component: ModerationListPending,
        },
        {
          path: 'moderation/content-analysis/:contentId',
          name: 'ModerationContentAnalysis',
          component: ModerationContentAnalysis,
          props: true, // Pass route params as props
        },
      ],
    },
  ],
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const jwtStore = useJwtStore();

  if (requiresAuth && !jwtStore.isLoggedIn) {
    // Redirect to login if the user is not authenticated
    next({ path: '/login' });
  } else if (!requiresAuth && jwtStore.isLoggedIn && to.path === '/login') {
    // Redirect to dashboard if the user is already logged in
    next({ path: '/dashboard/summary' });
  } else {
    next(); // Proceed as normal
  }
});

export default router;
