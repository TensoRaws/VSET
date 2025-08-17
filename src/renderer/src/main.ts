import ElementPlus from 'element-plus'

import naive from 'naive-ui'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'

import './assets/main.css'

import 'element-plus/dist/index.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(naive)

app.use(pinia)
app.use(ElementPlus)
app.use(router)

app.mount('#app')
