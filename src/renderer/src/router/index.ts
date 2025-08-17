import type { RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'
import EnhancePage from '../components/EnhancePage.vue'
import FilterPage from '../components/FilterPage.vue'
import HomePage from '../components/HomePage.vue'
import InputPage from '../components/InputPage.vue'
import OutputPage from '../components/OutputPage.vue'
import RendingPage from '../components/RendingPage.vue'
import SettingPage from '../components/SettingPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/input',
    name: 'InputPage',
    component: InputPage,
  },
  {
    path: '/enhance',
    name: 'EnhancePage',
    component: EnhancePage,
  },
  {
    path: '/filter',
    name: 'FilterPage',
    component: FilterPage,
  },
  {
    path: '/output',
    name: 'OutputPage',
    component: OutputPage,
  },
  {
    path: '/rending',
    name: 'RendingPage',
    component: RendingPage,
  },
  {
    path: '/setting',
    name: 'SettingPage',
    component: SettingPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
