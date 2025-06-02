import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useUserStore } from '@/stores/user'

export const authGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext,
) => {
  const userStore = useUserStore()

  if (!userStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next({ name: 'dashboard' })
    return
  }

  if (to.meta.requiresModerator && !userStore.isModerator) {
    next({ name: 'dashboard' })
    return
  }

  next()
}

export const guestGuard = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext,
) => {
  const userStore = useUserStore()

  if (userStore.isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
}
