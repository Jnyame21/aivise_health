import {createRouter,createWebHistory,type NavigationGuardNext} from 'vue-router'
import { useUserAuthStore } from '@/stores/userAuthStore'

const checkAuth = async (role:string) => {
  const userAuthStore = useUserAuthStore()
  if (!userAuthStore.isAuthenticated) {
    try {
      await userAuthStore.UpdateToken()
      await userAuthStore.getUserData(role)
      userAuthStore.isAuthenticated = true
    }
    catch (e){
      if (role === 'staff') return Promise.reject(e)
    }
  }
}

const checkClient = async (to: any, from: any, next: NavigationGuardNext) => {
  const userAuthStore = useUserAuthStore()
  try{
    await checkAuth('client')
  }
  catch (e:any){
    if (e?.response?.status === 401)
    return next('/')
  }
  if (userAuthStore.isAuthenticated && !userAuthStore.fetchedDataLoaded){
    userAuthStore.getClientData()
  }

  next()
}


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ()=> import('@/views/HomeView.vue'),
    },
    {
      path: '/client',
      name: 'client',
      props: true,
      component: ()=> import('@/views/ClientView.vue'),
      beforeEnter: async (to, from, next) => {
        await checkClient(to, from, next)
      },
    },
  ],
})

export default router
