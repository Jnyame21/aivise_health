<script setup lang="ts">
import { useElementsStore } from '@/stores/elementsStore';
import { useUserAuthStore } from '@/stores/userAuthStore';


const elementsStore = useElementsStore()
const userAuthStore = useUserAuthStore()

const changePage = (page_name: any) => {
  elementsStore.activePage = page_name
  localStorage.setItem('activePage', page_name)
}


</script>


<template>
  <div class="nav-container">
    <v-list class="nav-list-container">
      <v-list-item @click="changePage('ClientConsultations')" class="nav-item nav-link" prepend-icon="mdi-stethoscope">
        CONSULTATION
      </v-list-item>
      <v-list-item @click="changePage('ClientMedicine')" class="nav-item nav-link" prepend-icon="mdi-pill">
        MEDICATION
      </v-list-item>
      <v-list-item @click="changePage('ClientOrders')" class="nav-item nav-link" prepend-icon="mdi-medical-bag">
        ORDERS
      </v-list-item>
      <v-list-item @click="changePage('ClientDietPlans')" class="nav-item nav-link" prepend-icon="mdi-silverware-fork-knife">
        DIET PLAN
      </v-list-item>
      <v-list-item @click="changePage('Cassandra')" class="nav-item nav-link" prepend-icon="mdi-robot">
        TALK TO CASSANDRA
      </v-list-item>
    </v-list>
  </div>
</template>


<style scoped>

</style>
