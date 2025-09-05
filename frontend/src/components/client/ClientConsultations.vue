<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, onUpdated } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';
import type { ConsultationOne } from '@/utils/types_utils';
import { formatDate, formatTime, isWeekend, hasTimePassed, isWithinWorkingHours } from '@/utils/util';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const itemProperties = ref<ConsultationOne | null>(null)
const itemSearch = ref('')
const itemObj = ref({
  date: '',
  time: '',
  purpose: '',
});

const itemData = computed(() => {
  return userAuthStore.clientConsultations
})

const itemHeaders = [
  {title: 'CONSULTATION', key: 'name', sortable: false},
  {title: 'DATE', key: 'date', sortable: true},
  {title: 'TIME', key: 'time', sortable: true},
  {title: 'PURPOSE', key: 'purpose', sortable: false},
  {title: 'ASSIGNED PHYSICIAN', key: 'staff', sortable: false},
  {title: '', key: 'actions', sortable: false},
]

const createItem = async () => {
  if (isWeekend(itemObj.value.date)){
    elementsStore.ShowOverlay("We don't accept consultations on weekends!", 'red')
    return;
  }
  if (new Date(itemObj.value.date) < new Date(userAuthStore.currentDate)){
    elementsStore.ShowOverlay('The date you selected has already passed!', 'red')
    return;
  }
  if (new Date(itemObj.value.date) === new Date(userAuthStore.currentDate) && hasTimePassed(itemObj.value.time)){
    elementsStore.ShowOverlay('The time you selected has already passed!', 'red')
    return;
  }
  if (!isWithinWorkingHours(itemObj.value.time)){
    elementsStore.ShowOverlay('The time you selected is outside of our working hours!', 'red')
    return;
  }
  const formData = new FormData()
  formData.append('type', 'createConsultation')
  formData.append('dataObj', JSON.stringify(itemObj.value))

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('client/data', formData)
    const data: ConsultationOne = response.data
    userAuthStore.clientConsultations.unshift(data)
    elementsStore.HideLoadingOverlay()
    const inPersonMessage = "Your consultation has been successfully booked!\nPlease arrive at our facility 10-15 minutes early. Don't forget to bring any relevant documents"
    closeOverlay('BookConsultationOverlay')
    elementsStore.ShowOverlay(inPersonMessage, 'green')
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

const deleteItem = async (item_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteConsultation')
  formData.append('itemId', item_id.toString())

  try {
    await axiosInstance.post('client/data', formData)
    const itemToDeleteIndex = userAuthStore.clientConsultations.findIndex(item => item.id === item_id)
    itemToDeleteIndex !== -1 ? userAuthStore.clientConsultations.splice(itemToDeleteIndex, 1) : null
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

const showOverlay = (element: string, item_properties: ConsultationOne | null = null) => {
  itemProperties.value = item_properties
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}

const closeOverlay = (element: string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'none'
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'ClientConsultations'" :class="{ 'is-active-page': elementsStore.activePage === 'ClientConsultations' }">

    <!-- Item staff info Overlay -->
    <div id="ConsultationStaffInfoOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('ConsultationStaffInfoOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          <v-card class="pa-4 elevation-1 rounded-lg" color="#f9f9f9">
            <v-row>
              <v-col cols="12" sm="4" class="text-center">
                <v-avatar size="120" class="mx-auto"><v-img :src="typeof itemProperties.staff.img === 'string' ? itemProperties.staff.img : itemProperties.staff.img.url" cover></v-img></v-avatar>
                <div class="mt-2 font-weight-medium text-lg text-primary">{{ itemProperties.staff.specialization }}</div>
              </v-col>
              <v-col cols="12" sm="8">
                <div class="text-h6 font-weight-bold mb-2">{{ itemProperties.staff.user }}</div>
                <div class="d-flex flex-wrap">
                  <v-chip class="ma-1" color="blue-grey" variant="flat" size="small">{{ itemProperties.staff.gender }}, {{ itemProperties.staff.age }} yrs</v-chip>
                  <v-chip class="ma-1" color="green" variant="flat" size="small">{{ itemProperties.staff.nationality }}</v-chip>
                  <v-chip class="ma-1" color="purple" variant="flat" size="small" v-if="itemProperties.staff.years_of_experience">{{ itemProperties.staff.years_of_experience }} yrs exp</v-chip>
                  <v-chip v-for="lang in itemProperties.staff.languages" :key="lang" class="ma-1" color="deep-orange" variant="flat" size="small">{{ lang }}</v-chip>
                </div>
                <div class="mt-3 text-body-2"><strong>Bio:</strong> {{ itemProperties.staff.bio || 'No bio available' }}</div>
                <div class="mt-2 text-body-2 font-weight-medium"><strong>Contact:</strong> {{ itemProperties.staff.contact_one }}</div>
              </v-col>
            </v-row>
          </v-card>
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Add item Overlay -->
    <div id="BookConsultationOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('BookConsultationOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <v-chip :size="elementsStore.btnSize2" color="red">NB: Fields with [*] are mandatory.</v-chip>
        </div>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="itemObj.date" label="DATE [*]" type="date" clearable variant="solo-filled" density="comfortable" hint="Select a date for your appointment." prepend-icon="mdi-calendar" persistent-hint />
          <v-text-field class="input-field" v-model="itemObj.time" label="TIME [*]" type="time" clearable variant="solo-filled" density="comfortable" hint="Select a time for your appointment." prepend-icon="mdi-clock" persistent-hint />
          <v-textarea col="5" v-model="itemObj.purpose" label="PURPOSE [*]" clearable variant="solo-filled" hint="Briefly describe the reason for your visit (e.g. Annual check-up, post-op follow-up, or vaccination.)" density="comfortable" persistent-hint />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createItem()" :disabled="!(itemObj.date && itemObj.time && itemObj.purpose)" :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">BOOK</v-btn>
        </div>
      </div>
    </div>

    <TheLoader v-if="!userAuthStore.fetchedDataLoaded" :func="userAuthStore.getClientData" />
    <div class="content-header" v-if="userAuthStore.fetchedDataLoaded">
      <h4 class="content-header-title">CONSULTATIONS</h4>
    </div>
    <v-data-table-virtual class="table" v-if="userAuthStore.fetchedDataLoaded" :headers="itemHeaders.filter(item=> item.key !== 'data-table-expand')" :items="itemData" :search="itemSearch" show-expand fixed-header multi-sort>
      <template v-slot:top>
        <v-toolbar color="#333333">
          <v-spacer></v-spacer>
          <v-btn class="bg-blue mr-3" @click="showOverlay('BookConsultationOverlay')" :size="elementsStore.btnSize1" prepend-icon="mdi-plus">BOOK A CONSULTATION</v-btn>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort, sortBy }">
        <tr>
          <template v-for="col in columns" :key="col.key">
            <th class="table-head">{{ col.title }}
              <v-icon v-if="col.sortable" @click="toggleSort(col)" :icon="getSortIcon(col)" color="medium-emphasis" />
              <span v-if="isSorted(col) && col.sortable">{{ sortBy.findIndex(s => s.key === col.key) + 1 }}</span>
            </th>
          </template>
        </tr>
      </template>
      <template #item.name="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.name }}</v-chip>
        </div>
      </template>
      <template #item.date="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ formatDate(item.date, 'short') }}</v-chip>
        </div>
      </template>
      <template #item.time="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ formatTime(item.time) }}</v-chip>
        </div>
      </template>
      <template #item.purpose="{ internalItem, isExpanded, toggleExpand }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="toggleExpand(internalItem)" color="blue" :size="elementsStore.btnSize1">{{ isExpanded(internalItem) ? 'hide' : 'show' }}</v-chip>
        </div>
      </template>
      <template v-slot:expanded-row="{ columns, item }">
        <tr>
          <td class="table-data" :colspan="columns.length">{{ item.purpose }} </td>
        </tr>
      </template>
      <template #item.staff="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('ConsultationStaffInfoOverlay', item)" :size="elementsStore.btnSize1" color="blue">show</v-chip>
        </div>
      </template>
      <template #item.actions="{ item }">
        <div class="flex-all">
          <v-btn class="ml-2" v-if="new Date(item.date) >= new Date(userAuthStore.currentDate)" color="red" size="x-small" icon="mdi-delete" variant="flat" 
            @click="elementsStore.ShowDeletionOverlay(()=> deleteItem(item.id), 'Are you sure you want to cancel this consultation?')">
          </v-btn>
        </div>
      </template>
      <template #item.data-table-expand="{ item }"></template>
    </v-data-table-virtual>
  </div>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}


</style>
