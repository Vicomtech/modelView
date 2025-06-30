import { createRouter, createWebHistory } from 'vue-router'
import ModelView from '../views/ModelView.vue'
import ImageSelectionView from '@/views/ImageSelectionView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: ImageSelectionView,
      name: 'home'
    },
    {
      path: '/mv',
      component: ModelView,
      name: 'modelview',
      beforeEnter: (to, from) => {
        if (from.name !== 'home') {
          return { name: 'home' }
        }
        else return true
      },
    }
  ]
})

export default router
