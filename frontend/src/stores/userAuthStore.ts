import { defineStore } from 'pinia'
import { defaultAxiosInstance } from '@/utils/axiosInstance'
import axiosInstance from '@/utils/axiosInstance'
import { useElementsStore } from '@/stores/elementsStore'
import { AxiosError } from 'axios'
import router from '@/router'
import type { StaffUserData, ClientUserData, ConsultationOne, Order, Drug, Message, DietPlan } from '@/utils/types_utils'

export interface states {
  userData: (StaffUserData & { address?: string | null; allergies?: string[]; health_conditions?: string[] }) | ClientUserData | null
  accessToken: string;
  message: string
  isAuthenticated: boolean
  fetchedDataLoaded: boolean;
  currentYearStartDate: string;
  currentDate: string;
  currentYearEndDate: string;
  clientConsultations: ConsultationOne[];
  drugs: Drug[];
  clientOrders: Order[];
  messages: Message[];
  dietPlans: DietPlan[];
}


export const useUserAuthStore = defineStore('userAuthStore', {
  state: (): states => {
    return {
      accessToken: '',
      userData: null,
      message: '',
      isAuthenticated: false,
      fetchedDataLoaded: false,
      currentDate: '',
      currentYearStartDate: '',
      currentYearEndDate: '',
      clientConsultations: [],
      drugs: [],
      clientOrders: [],
      messages: [],
      dietPlans: [],
    }
  },

  actions: {

    async logoutUser() {
      const elementsStore = useElementsStore()
      try {
        elementsStore.ShowLoadingOverlay()
        await axiosInstance.post('logout')
        this.accessToken = ''
        this.isAuthenticated = false
        this.userData = null
        localStorage.removeItem('activePage')
        await router.push('/')
        elementsStore.HideLoadingOverlay()
        return;
      }
      catch (e) {
        elementsStore.HideLoadingOverlay()
        elementsStore.ShowOverlay('An error occurred while logging out', 'error')
        return Promise.reject(e)
      }
    },

    async getStaffData() {
      try {
        const response = await axiosInstance.get('staff/data')
        this.fetchedDataLoaded = true
      }
      catch (e) {
        return Promise.reject(e)
      }
    },

    async getClientData() {
      try {
        const response = await axiosInstance.get('client/data')
        this.clientConsultations = response.data['consultations']
        this.drugs = response.data['drugs']
        this.clientOrders = response.data['orders']
        this.messages = response.data['messages']
        this.dietPlans = response.data['diet_plans']
        this.fetchedDataLoaded = true
      }
      catch (e) {
        return Promise.reject(e)
      }
    },

    async getUserData(user_role: string) {
      try {
        const response = await axiosInstance.get('user/data', {params: {role: user_role}})
        this.userData = response.data
        this.currentYearStartDate = response.data['current_year_start_date']
        this.currentYearEndDate = response.data['current_year_end_date']
      }
      catch (error) {
        if (error instanceof AxiosError) {
          const axiosError = error as AxiosError
          if (axiosError.response) {
            if (axiosError.response.status === 401 && axiosError.response.data) {
              this.message = (axiosError.response.data as {message: string}).message
            }
            else {
              this.message = 'Oops! something went wrong. Try again later'
            }
          }
          else if (!axiosError.response && (axiosError.code === 'ECONNABORTED' || !navigator.onLine)) {
            this.message = 'A network error occurred! Please check you internet connection'
          }
          else {
            this.message = 'An unexpected error occurred!'
          }
          
        }
        return Promise.reject(error)
      }
    },

    async userLogin(username: string, password: string, role: string) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      try {
        const response = await defaultAxiosInstance.post('login', formData)
        this.accessToken = response.data['access']
        await this.getUserData(role)
        this.isAuthenticated = true
        this.message = 'Login successful'
      }
      catch (error) {
        if (error instanceof AxiosError) {
          const axiosError = error as AxiosError
          if (axiosError.response) {
            if (axiosError.response.status === 401 && axiosError.response.data) {
              this.message = 'Oops! your username or password is wrong'
            }
            else {
              this.message = 'Oops! something went wrong. Try again later'
            }
          }
          else if (!axiosError.response && (axiosError.code === 'ECONNABORTED' || !navigator.onLine)) {
            this.message = 'A network error occurred! Please check you internet connection'
          }
          else {
            this.message = 'An unexpected error occurred!'
          }
          return Promise.reject(error)
        }
      }
    },

    async UpdateToken() {
      try {
        const response = await defaultAxiosInstance.post('api/token/refresh/')
        this.accessToken = response.data.access
      }
      catch (error: any) {
        return Promise.reject(error)
      }
    },

    async getCurrentServerTime() {
      try {
        const response = await defaultAxiosInstance.get('server_time')
        return response.data
      }
      catch (error: any) {
        return Promise.reject(error)
      }
    },
  },
})


