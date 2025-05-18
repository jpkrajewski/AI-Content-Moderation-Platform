import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/UserLogin.vue';
import Test from '../views/TestTest.vue';
import Register from '../views/UserRegister.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/test',
      name: 'Test',
      component: Test,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
  ],
})

export default router
