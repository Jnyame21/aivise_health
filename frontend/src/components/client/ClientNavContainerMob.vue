<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()


const changePage = (page_name: any) => {
  elementsStore.activePage = page_name
  localStorage.setItem('activePage', page_name)
}


const showOverlay = (element:string) => {
  const overlay = document.getElementById(element)
  if (overlay) {
    overlay.style.display = 'flex'
  }
}


</script>


<template>
  <div class="nav-container-drawer" v-show="elementsStore.navDrawer">
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
      <div class="flex-all mt-15">
        <v-btn @click="showOverlay('LogoutOverlay')" color="red" size="small" prepend-icon="mdi-logout">LOGOUT</v-btn>
      </div>
    </v-list>
  </div>
</template>


<style scoped>

</style>
