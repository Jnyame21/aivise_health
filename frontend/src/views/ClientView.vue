<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore'
import { useElementsStore } from '@/stores/elementsStore'
import TheHeader from '@/components/TheHeader.vue';
import TheFooter from '@/components/TheFooter.vue';
import ClientNavContainerDesk from '@/components/client/ClientNavContainerDesk.vue';
import ClientNavContainerMob from '@/components/client/ClientNavContainerMob.vue';
import ClientConsultations from '@/components/client/ClientConsultations.vue';
import ClientMedicine from '@/components/client/ClientMedicine.vue';
import ClientOrders from '@/components/client/ClientOrders.vue';
import Cassandra from '@/components/client/Cassandra.vue';
import ClientDietPlans from '@/components/client/ClientDietPlans.vue';
import { onMounted } from 'vue';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

onMounted(()=>{
  const activePage = localStorage.getItem('activePage')
  activePage ? elementsStore.activePage = activePage : elementsStore.activePage = 'ClientConsultations'
})


</script>

<template>

  <TheHeader v-if="userAuthStore.userData"/>
  <main class="main" v-if="userAuthStore.userData">
    <ClientNavContainerMob v-if="!elementsStore.onDesk" />
    <ClientNavContainerDesk v-if="elementsStore.onDesk" />
    <div class="pages-container">
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'ClientConsultations' }">
        <ClientConsultations/>
      </div>
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'ClientMedicine' }">
        <ClientMedicine/>
      </div>
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'ClientOrders' }">
        <ClientOrders/>
      </div>
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'Cassandra' }">
        <Cassandra/>
      </div>
      <div class="component-wrapper" :class="{ 'is-active-component': elementsStore.activePage === 'ClientDietPlans' }">
        <ClientDietPlans/>
      </div>
    </div>
  </main>
  <TheFooter v-if="userAuthStore.userData"/>
</template>

<style scoped>
.overlay-card {
  max-width: 600px !important;
}


</style>
