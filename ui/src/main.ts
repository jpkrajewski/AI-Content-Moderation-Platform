import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useVersionStore } from '@/stores/version';

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
const versionStore = useVersionStore();
versionStore.fetchVersion();
app.use(router)
app.mount('#app')
