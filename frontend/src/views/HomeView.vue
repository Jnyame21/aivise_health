<script setup lang="ts">
import { computed, reactive } from "vue";
import { useRouter } from "vue-router";
import { AxiosError } from 'axios';
import { useHead } from '@vueuse/head'
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from "@/stores/elementsStore";
import { onMounted, ref } from "vue";
import { countriesData } from "@/utils/util";
import { defaultAxiosInstance } from '@/utils/axiosInstance';
const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const router = useRouter()
const passwordVisible = ref(false)
const repeatPasswordVisible = ref(false)
const customerImg = ref<File | null>(null)
const clientEmail = ref('')
const clientPassword = ref('')
const serviceItem = ref('')

useHead({
  meta: [
    {
      name: "description",
      content: "Login to Aivise Health - Your digital hub for virtual consultations, ePharmacy services, dietetic guidance, and more.",
    },
    { name: "robots", content: "index, follow" },
  ],
});

const clientData = ref({
  firstName: '',
  lastName: '',
  gender: '',
  contactOne: '',
  email: '',
  age: '',
  address: '',
  nationality: '',
  password: '',
  img: '',
  healthConditions: '',
  allergies: '',
  repeatPassword: ''
})

onMounted(()=>{
  localStorage.removeItem('activePage')
})

const enterService = (service: string) => {
  if (!userAuthStore.isAuthenticated){
    showOverlay('ClientRegistrationOverlay')
    return;
  }
  if (service === 'cassandra'){
    elementsStore.activePage = 'Cassandra'
  }
  else {
    elementsStore.activePage = 'ClientConsultations'
  }
  router.push('/client')
}

const register = async () => {
  if (clientData.value.password !== clientData.value.repeatPassword) {
    elementsStore.ShowOverlay('Passwords do not match', 'red')
    return;
  }
  if (Number(clientData.value.age) <= 0) {
    elementsStore.ShowOverlay('Age must be greater than 0', 'red')
    return;
  }
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('dataObject', JSON.stringify(clientData.value))
  formData.append('img', customerImg.value ? customerImg.value : '')
  
  try {
    const response = await defaultAxiosInstance.post('client/registration', formData)
    const data = response.data
    await userAuthStore.userLogin(data['username'], data['password'], 'client')
    await userAuthStore.getClientData()
    closeOverlay('ClientRegistrationOverlay')
    serviceItem.value.toLowerCase() === 'consultation' ? elementsStore.activePage = 'ClientConsultations' : null
    await router.push('/client')
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        } else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const login = async () => {
  elementsStore.ShowLoadingOverlay()
  try {
    await userAuthStore.userLogin(clientEmail.value, clientPassword.value, 'client')
    await userAuthStore.getClientData()
    closeOverlay('ClientLoginOverlay')
    serviceItem.value.toLowerCase() === 'consultation' ? elementsStore.activePage = 'ClientConsultations' : null
    await router.push('/client')
    elementsStore.HideLoadingOverlay()
  }
  catch (error) {
    elementsStore.HideLoadingOverlay()
    if (error instanceof AxiosError) {
      if (error.response) {
        if (error.response.status === 401) {
          elementsStore.ShowOverlay("Invalid credentials", 'red')
        }
        else if (error.response.status === 400 && error.response.data.message) {
          elementsStore.ShowOverlay(error.response.data.message, 'red')
        }
        else {
          elementsStore.ShowOverlay('Oops! something went wrong. Try again later', 'red')
        }
      }
      else if (!error.response && (error.code === 'ECONNABORTED' || !navigator.onLine)) {
        elementsStore.ShowOverlay('A network error occurred! Please check you internet connection', 'red')
      }
      else {
        elementsStore.ShowOverlay('An unexpected error occurred!', 'red')
      }
    }
  }
}

const showOverlay = (element: string, overlay_to_close:string='') => {
  if (overlay_to_close){
    closeOverlay(overlay_to_close)
  }
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string, overlay_to_show:string='') => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
  if (overlay_to_show){
    showOverlay(overlay_to_show)
  }
}

</script>

<template>
  <v-container class="h-100 card-container" fluid style="overflow-y: auto;">

    <div id="ClientLoginOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('ClientLoginOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <v-chip :size="elementsStore.btnSize2" color="blue">
            Don't have an account yet? <a @click="closeOverlay('ClientLoginOverlay', 'ClientRegistrationOverlay')" class="signup-link"> Sign Up</a>
          </v-chip>
        </div>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="clientEmail"
            label="EMAIL" hint="Enter your email address" density="comfortable" type="email" clearable
            prepend-inner-icon="mdi-email">
          </v-text-field>
          <v-text-field class="input-field"
            :append-inner-icon="passwordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
            @click:append-inner="passwordVisible = !passwordVisible" :type="passwordVisible ? 'text' : 'password'"
            clearable density="comfortable" v-model="clientPassword" label="PASSWORD" hint="Enter your password"
            prepend-inner-icon="mdi-lock-outline" 
          />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="login" :disabled="!(clientPassword && clientEmail)"
            :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            LOGIN
          </v-btn>
        </div>
      </div>
    </div>

    <div id="ClientRegistrationOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('ClientRegistrationOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <v-chip :size="elementsStore.btnSize2" color="red">NB: Fields with [*] are mandatory.</v-chip>
          <v-chip :size="elementsStore.btnSize2" color="red">
            Already have an account? <a @click="closeOverlay('ClientRegistrationOverlay', 'ClientLoginOverlay')" class="signup-link"> Login</a>
          </v-chip>
        </div>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="clientData.firstName" label="FIRST NAME [*]" clearable variant="solo-filled"
            density="comfortable" placeholder="Eg. Cassandra" hint="Enter your first name" persistent-hint
          />
          <v-text-field class="input-field" v-model="clientData.lastName" label="LAST NAME (MIDDLE NAME + SURNAME)[*]" clearable variant="solo-filled"
            density="comfortable" placeholder="Eg. Akua Afriyie" persistent-hint hint="Enter your last name (middle name + surname)"
          />
          <v-select class="select" :items="['Male', 'Female', 'Other']" label="GENDER [*]" v-model="clientData.gender" variant="solo-filled" density="comfortable" clearable/>
          <v-select class="select" :items="countriesData.sort((a, b) => a.nationality.localeCompare(b.nationality))" label="NATIONALITY [*]" v-model="clientData.nationality"
            clearable item-title="nationality" item-value="nationality" variant="solo-filled" density="comfortable" persistent-hint hint="Select your nationality">
            <template v-slot:item="{ props: itemProps, item }">
              <v-list-item v-bind="itemProps" :subtitle="item.raw.name"></v-list-item>
            </template>
          </v-select>
          <v-text-field class="input-field" v-model="clientData.age" label="AGE [*]" type="number" variant="solo-filled" density="comfortable" clearable
            persistent-hint hint="Enter your age"
          />
          <v-text-field class="input-field" v-model="clientData.contactOne" label="PRIMARY MOBILE NUMBER [*]" variant="solo-filled" density="comfortable" placeholder="Eg. +233596021383" clearable
            persistent-hint hint="Enter your primary mobile number"
          />
          <v-text-field class="input-field" v-model="clientData.email" label="EMAIL [*]" type="email" variant="solo-filled"
            density="comfortable" persistent-hint hint="Enter your email address" placeholder="Eg. nyamejustice2000@gmail.com" clearable
          />
          <v-text-field class="input-field"
            :append-inner-icon="passwordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
            @click:append-inner="passwordVisible = !passwordVisible" :type="passwordVisible ? 'text' : 'password'"
            clearable density="comfortable" v-model="clientData.password" label="PASSWORD" hint="Enter a password"
            prepend-inner-icon="mdi-lock-outline" 
          />
          <v-text-field class="input-field"
            :append-inner-icon="repeatPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
            @click:append-inner="repeatPasswordVisible = !repeatPasswordVisible"
            :type="repeatPasswordVisible ? 'text' : 'password'" clearable density="comfortable" v-model="clientData.repeatPassword"
            label="REPEAT PASSWORD" hint="Repeat the password" prepend-inner-icon="mdi-lock-outline"
          />
          <v-text-field class="input-field" v-model="clientData.healthConditions" label="HEALTH CONDITIONS"  variant="solo-filled" density="comfortable" placeholder="Eg. Diabetes, Heart Disease" clearable
            persistent-hint hint="Enter any health conditions you have. Seperate each condition with a comma"
          />
          <v-text-field class="input-field" v-model="clientData.allergies" label="ALLERGIES"  variant="solo-filled" density="comfortable" placeholder="Eg. Milk, Eggs" clearable
            persistent-hint hint="Enter any allergies you have. Seperate each with a comma"
          />
          <v-text-field class="input-field" v-model="clientData.address" label="RESIDENTIAL ADDRESS" type="address" variant="solo-filled" density="comfortable" placeholder="Eg. Ak-509-1066, Kotei, Kumasi" clearable
            persistent-hint hint="Enter your residential address"
          />
          <v-file-input @update:model-value="(file:any)=> clientData.img = file" clearable show-size class="select" v-model="customerImg"
            label="PHOTO" density="comfortable" variant="solo-filled" chips accept="image/*" prepend-icon="mdi-file-image-outline" persistent-hint hint="Upload your photo">
          </v-file-input>
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="register" :disabled="!(clientData.password && clientData.repeatPassword && clientData.firstName && clientData.lastName && clientData.nationality && clientData.gender && clientData.contactOne && clientData.email && clientData.age)"
            :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            REGISTER
          </v-btn>
        </div>
      </div>
    </div>

    <div class="landing-page flex-all-c" style="overflow-x: hidden;">
    <!-- Hero Section -->
    <section class="hero bg-white text-center py-16 px-4">
      <h1 class="text-4xl font-bold mb-4 text-gray-800">Welcome to Aivise Health</h1>
      <p class="text-lg text-gray-600 mb-6">Empowering health with AI-driven consultations, pharmacy, and wellness services across Ghana.</p>
      <v-btn color="primary" size="large" @click="enterService('consultation')" class="rounded-full">Get Started</v-btn>
    </section>

    <!-- About Section -->
    <section class="about bg-gray-100 py-14 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-semibold mb-4">About Aivise Health</h2>
        <p class="text-gray-700 text-lg leading-relaxed">
          Aivise Health is a digital healthcare platform providing in-person consultations, e-pharmacy services,
          dietary guidance, psychological support, and herbal medicine insights. We use AI to connect patients with
          the best available doctors and make health more accessible, personalized, and efficient.
        </p>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services py-16 px-6 bg-gray-50">
      <h2 class="text-3xl font-bold text-center mb-10">Our Services</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 max-w-6xl mx-auto" style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap;">
        <div class="service-card text-center p-4 border rounded-lg shadow-sm bg-white" style="max-width: 300px; margin: 10px">
          <img src="/app_background_img_2.png" style="max-width: 300px;" alt="Consultation" class="mx-auto mb-2 h-20 w-20 object-cover rounded-full">
          <h3 class="text-sm font-semibold mb-1">Consultation</h3>
          <p class="text-xs text-gray-600">Book in-person sessions with the best doctor matched by AI.</p>
        </div>
        <div class="service-card text-center p-4 border rounded-lg shadow-sm bg-white" style="max-width: 300px; margin: 10px">
          <img src="/e_pharm_img.webp" style="max-width: 300px;" alt="E-Pharmacy" class="mx-auto mb-2 h-20 w-20 object-cover rounded-full">
          <h3 class="text-sm font-semibold mb-1">E-Pharmacy</h3>
          <p class="text-xs text-gray-600">Order medications online and ask Cassandra for symptom help.</p>
        </div>
        <div class="service-card text-center p-4 border rounded-lg shadow-sm bg-white" style="max-width: 300px; margin: 10px">
          <img src="/dietetics_img.webp" style="max-width: 300px;" alt="Dietetics" class="mx-auto mb-2 h-20 w-20 object-cover rounded-full">
          <h3 class="text-sm font-semibold mb-1">Dietetics</h3>
          <p class="text-xs text-gray-600">Get customized nutrition advice from qualified dietitians.</p>
        </div>
        <div class="service-card text-center p-4 border rounded-lg shadow-sm bg-white" style="max-width: 300px; margin: 10px">
          <img src="/mental_health_img.webp" style="max-width: 300px;" alt="Mental Health" class="mx-auto mb-2 h-20 w-20 object-cover rounded-full">
          <h3 class="text-sm font-semibold mb-1">Mental Health</h3>
          <p class="text-xs text-gray-600">Chat with Cassandra for mental wellness support and tips.</p>
        </div>
        <div class="service-card text-center p-4 border rounded-lg shadow-sm bg-white" style="max-width: 300px; margin: 10px">
          <img src="/herbal_medicine_img.webp" style="max-width: 300px;" alt="Herbal Medicine" class="mx-auto mb-2 h-20 w-20 object-cover rounded-full">
          <h3 class="text-sm font-semibold mb-1">Herbal Medicine</h3>
          <p class="text-xs text-gray-600">Discover herbal remedies. Ask Cassandra what can help you.</p>
        </div>
      </div>
    </section>

    <!-- AI Assistant Section -->
    <section class="ai-assistant bg-blue-50 py-14 px-4 text-center">
      <h2 class="text-3xl font-semibold mb-4">Meet Cassandra, Your AI Health Assistant</h2>
      <p class="text-gray-700 max-w-3xl mx-auto text-lg mb-6">
        Cassandra is your smart health companion, available 24/7 to answer medical questions, recommend medications, and help you understand your symptoms. She's designed to make your health journey smoother and more informed.
      </p>
      <v-btn color="secondary" size="large" @click="enterService('cassandra')" class="rounded-full">Chat with Cassandra</v-btn>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-8 px-6">
      <div class="max-w-5xl mx-auto text-center">
        <h3 class="text-xl font-bold mb-2">Aivise Health</h3>
        <p class="text-gray-400 mb-4">Revolutionizing healthcare with AI in Ghana. © {{ new Date().getFullYear() }}</p>
        <div class="space-x-4">
          <a href="#" class="text-gray-400 hover:text-white">Privacy</a>
          <a href="#" class="text-gray-400 hover:text-white">Terms</a>
          <a href="#" class="text-gray-400 hover:text-white">Contact</a>
        </div>
      </div>
    </footer>
  </div>

  </v-container>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}

.header-text{
  font-weight: bold;
  font-family: 'Inter';
  font-size: 2rem;
  color: white
}
.sub-text{
  font-family: 'Inter';
  font-size: 1.1rem;
  color: white
}
.hover-card {
  transition: 0.3s ease;
}
.hover-card:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer !important;
}
.signup-link{
  color: blue;
  margin-left: 1em;
  font-weight: bold;
}
.signup-link:hover{
  text-decoration: underline;
  cursor: pointer;
}
.footer {
  background-color: black;
  color: yellow;
  text-align: center;
  padding: 1em;
}


</style>
