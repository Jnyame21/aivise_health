<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, watch } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';
import { formatDate, formatNumberAsCurrency } from '@/utils/util';
import type { DietPlan } from '@/utils/types_utils';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const itemSearch = ref('')
const itemProperties = ref<DietPlan | null>(null)

const itemObj = ref({
  goal: '',
  diet_type: '',
  duration_days: 7,
  meal_types: [],
  activity_level: '',
  preferred_foods: '',
  end_date: '',
});

const itemData = computed(() => {
  return userAuthStore.dietPlans
})

const dietTypeOptions = [
  { title: 'Regular', value: 'regular' },
  { title: 'Vegetarian', value: 'vegetarian' },
  { title: 'Vegan', value: 'vegan' },
  { title: 'Keto', value: 'keto' },
];

const activityLevelOptions = [
  { title: 'Sedentary (little to no exercise)', value: 'sedentary' },
  { title: 'Lightly Active (light exercise/sports 1-3 days/week)', value: 'lightly_active' },
  { title: 'Moderately Active (moderate exercise/sports 3-5 days/week)', value: 'moderately_active' },
  { title: 'Very Active (hard exercise/sports 6-7 days/week)', value: 'very_active' },
  { title: 'Extra Active (very hard exercise/physical job)', value: 'extra_active' },
];

const itemHeaders = [
  { title: 'GOAL', key: 'goal', sortable: true },
  { title: 'DIET TYPE', key: 'diet_type', sortable: true },
  { title: 'DURATION (DAYS)', key: 'duration_days', sortable: true },
  { title: 'SCHEDULED MEALS', key: 'plans', sortable: false },
  { title: 'MEAL TYPES', key: 'meal_types', sortable: false },
  { title: 'ACTIVITY LEVEL', key: 'activity_level', sortable: true },
  { title: 'PREFERRED FOODS', key: 'preferred_foods', sortable: false },
  { title: 'END DATE', key: 'end_date', sortable: true },
  { title: '', key: 'action', sortable: false },
];

const createItem = async () => {
  if (userAuthStore.dietPlans.some(item=> new Date(item.end_date) >= new Date(userAuthStore.currentDate))){
    elementsStore.ShowOverlay('There are diet plans that have not ended yet', 'red')
    return;
  }
  if (!Number.isInteger(Number(itemObj.value.duration_days)) || Number(itemObj.value.duration_days) < 0){
    elementsStore.ShowOverlay('The duration(days) must be a positive whole number', 'red')
    return;
  }
  if (Number(itemObj.value.duration_days) > 30){
    elementsStore.ShowOverlay('The maximum duration is 30 days', 'red')
    return;
  }
  const formData = new FormData()
  formData.append('type', 'createDietPlan')
  formData.append('dataObj', JSON.stringify(itemObj.value))

  elementsStore.ShowLoadingOverlay()
  try {
    const response = await axiosInstance.post('client/data', formData)
    const data: DietPlan = response.data
    userAuthStore.dietPlans.unshift(data)
    closeOverlay('AddDietPlanOverlay')
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Your diet plan is now ready. Remember, consistency is key to achieving your goals.', 'green')
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
  formData.append('type', 'deleteDietPlan')
  formData.append('itemId', item_id.toString())

  try {
    await axiosInstance.post('client/data', formData)
    const itemtoDeleteIndex = userAuthStore.dietPlans.findIndex(item => item.id === item_id)
    itemtoDeleteIndex !== -1 ? userAuthStore.dietPlans.splice(itemtoDeleteIndex, 1) : null
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

const showOverlay = (element: string, item_properties: DietPlan | null = null) => {
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
  <div class="content-wrapper" v-show="elementsStore.activePage === 'ClientDietPlans'" :class="{ 'is-active-page': elementsStore.activePage === 'ClientDietPlans' }">

    <!-- Item Plans Overlay -->
    <div id="DietPlanDayPlanOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DietPlanDayPlanOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{ itemProperties?.goal  }}</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          <v-table class="table" fixed-header>
            <thead>
              <tr>
                <th>Day</th>
                <th>Date</th>
                <th>Meals</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in itemProperties.plans" :key="item.day">
                <td>
                  <v-chip :size="elementsStore.btnSize1">{{ item.day }}</v-chip>
                </td>
                <td>
                  <v-chip :size="elementsStore.btnSize1">{{ item.date }}</v-chip>
                </td>
                <td>
                  <div v-for="(foods, meal) in item.meals" :key="meal" style="margin-bottom: 8px;">
                    <strong>{{ String(meal).charAt(0).toUpperCase() + String(meal).slice(1) }}:</strong>
                    <ul>
                      <li v-for="food in foods" :key="food">{{ food }}</li>
                    </ul>
                  </div>
                </td>
                <td>{{ item.notes }}</td>
              </tr>
            </tbody>
          </v-table>
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Add item Overlay -->
    <div id="AddDietPlanOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('AddDietPlanOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container">
          <v-chip :size="elementsStore.btnSize2" color="red">NB: Fields with [*] are mandatory.</v-chip>
        </div>
        <div class="overlay-card-content-container">
          <v-text-field class="input-field" v-model="itemObj.goal" label="GOAL [*]" clearable variant="solo-filled" density="comfortable" hint="Main objective of the diet (e.g., weight loss)" prepend-icon="mdi-target" persistent-hint />
          <v-select class="input-field" v-model="itemObj.diet_type" label="DIET TYPE [*]" :items="dietTypeOptions" item-title="title" item-value="value" variant="solo-filled" density="comfortable" hint="Preferred dietary style" prepend-icon="mdi-food-variant" persistent-hint />
          <v-text-field class="input-field" v-model.number="itemObj.duration_days" label="DURATION (days) [*]" type="number" min="1" clearable variant="solo-filled" density="comfortable" hint="Number of days for the plan" prepend-icon="mdi-calendar-range" persistent-hint />
          <v-select class="input-field" v-model="itemObj.meal_types" label="MEAL TYPES [*]" :items="['breakfast','lunch','dinner','snacks']" multiple chips variant="solo-filled" density="comfortable" hint="Meal times to include" prepend-icon="mdi-silverware-fork-knife" persistent-hint />
          <v-select class="input-field" v-model="itemObj.activity_level" label="ACTIVITY LEVEL [*]" :items="activityLevelOptions" item-title="title" item-value="value" variant="solo-filled" density="comfortable" hint="Your daily activity level" prepend-icon="mdi-run-fast" persistent-hint />
          <v-textarea class="input-field" v-model="itemObj.preferred_foods" label="PREFERRED FOODS" no-resize clearable variant="solo-filled" density="comfortable" hint="Comma-separated favorite foods or cuisines" prepend-icon="mdi-heart" persistent-hint />
        </div>
        <div class="overlay-card-action-btn-container">
          <v-btn @click="createItem()" :disabled="!(itemObj.goal && itemObj.diet_type && itemObj.duration_days && itemObj.meal_types.length > 0 && itemObj.activity_level)" :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">PLAN</v-btn>
        </div>
      </div>
    </div>

    <TheLoader v-if="!userAuthStore.fetchedDataLoaded" :func="userAuthStore.getClientData" />
    <div class="content-header" v-if="userAuthStore.fetchedDataLoaded">
      <h4 class="content-header-title">DIET PLANS</h4>
    </div>
    <v-data-table-virtual class="table" v-if="userAuthStore.fetchedDataLoaded" :headers="itemHeaders.filter(item=> item.key !== 'data-table-expand')" :items="itemData" fixed-header multi-sort>
      <template v-slot:top>
        <v-toolbar color="#333333">
          <v-spacer></v-spacer>
          <v-btn class="bg-blue mr-3" @click="showOverlay('AddDietPlanOverlay')" :size="elementsStore.btnSize1" prepend-icon="mdi-plus">CREATE A DIET PLAN</v-btn>
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
      <template #item.goal="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.goal }}</v-chip>
        </div>
      </template>
      <template #item.diet_type="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.diet_type.toUpperCase() }}</v-chip>
        </div>
      </template>
      <template #item.duration_days="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.duration_days }} days</v-chip>
        </div>
      </template>
      <template #item.plans="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DietPlanDayPlanOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.meal_types="{ item }">
        <div class="flex-all">
          <v-chip v-for="type in item.meal_types" :size="elementsStore.btnSize1">{{ type }}</v-chip>
        </div>
      </template>
      <template #item.activity_level="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.activity_level.replace('_', ' ') }}</v-chip>
        </div>
      </template>
      <template #item.preferred_foods="{ item }">
        <div class="flex-all">
          <v-chip class="ma-1"  v-for="food in item.preferred_foods" :size="elementsStore.btnSize1" color="green">{{ food }}</v-chip>
        </div>
      </template>
      <template #item.end_date="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ formatDate(item.end_date, 'short') }}</v-chip>
        </div>
      </template>
      <template #item.action="{ item }">
        <v-btn color="red" size="x-small" icon="mdi-delete" variant="flat" @click="elementsStore.ShowDeletionOverlay(() => deleteItem(item.id), 'Are you sure you want to delete this diet plan?')" />
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
