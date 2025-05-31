import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '@fontsource/poppins/400.css'
import '@fontsource/poppins/700.css'
import "@fontsource/inter/400.css"
import "@fontsource/inter/700.css"
import "@fontsource/roboto/400.css"
import "@fontsource/roboto/700.css"
import "@fontsource/open-sans/400.css"
import "@fontsource/open-sans/700.css"
import "@fontsource/montserrat/400.css"
import "@fontsource/montserrat/700.css"
import "@fontsource/lato/400.css"
import "@fontsource/lato/700.css"
import { createVuetify } from 'vuetify'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'


import App from './App.vue'
import router from './router'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const app = createApp(App)
const head = createHead()

const vuetify = createVuetify({
  components,
  directives,
  defaults: {
    global: {
      style: {
        fontFamily: 'Inter',
      },
    },
  },
})

app.use(head)
app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
