<template>
  <div>
    <nav>
      <ul>
        <li><router-link to="/secure/dashboard/summary">Dashboard Summary</router-link></li>
        <li><router-link to="/secure/dashboard/activity-metrics">Activity Metrics</router-link></li>
        <li><router-link to="/secure/dashboard/kpi">Dashboard KPI</router-link></li>
        <li><router-link to="/secure/moderation/pending">Moderation</router-link></li>
        <li><button @click="logout">Logout</button></li>
        <li>Version: {{ version }}</li>
      </ul>
    </nav>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useJwtStore } from '@/stores/jwt';
import { useVersionStore } from '@/stores/version';

const router = useRouter();
const jwtStore = useJwtStore();
const versionStore = useVersionStore();
const version = versionStore.version;

const logout = () => {
    jwtStore.clearJwt(); // Clear JWT token
    router.push('/login'); // Redirect to login
};
</script>

<style>
/* Basic styling for navigation */
nav ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  background: #f4f4f4;
  padding: 1rem;
}

nav ul li {
  display: inline;
}

main {
  margin: 1rem;
}
</style>
