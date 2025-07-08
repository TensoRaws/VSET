import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

import naive from 'naive-ui'

import router from "./router/index"

const app = createApp(App)
const pinia = createPinia()

app.use(naive)

app.use(pinia)
app.use(ElementPlus)
app.use(router)

app.mount('#app')
