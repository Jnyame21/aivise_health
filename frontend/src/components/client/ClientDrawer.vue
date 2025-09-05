<script setup lang="ts">
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const drawer = document.getElementById('clientDrawer')
document.addEventListener('click', (event: MouseEvent)=>{
  if (drawer?.style.display !== 'none'){
    if (!drawer?.contains(event?.target as Node)){
      elementsStore.drawer = false
    }
  }
})


</script>


<template>
    <div id="clientDrawer" class="drawer-container" v-show="elementsStore.drawer">
      <v-list class="drawer-list">
        <div class="flex-all-c profile-image-container">
          <img class="img" v-if="userAuthStore.userData" :src="typeof userAuthStore.userData?.img ==='string' ? userAuthStore.userData.img : userAuthStore.userData?.img?.url">
        </div>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-account-outline">
          <v-list-item-title class="drawer-title">
            FIRST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.first_name }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-card-account-details-outline">
          <v-list-item-title class="drawer-title">
            LAST NAME
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.last_name }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" v-if="userAuthStore.userData && userAuthStore.userData.gender.toLowerCase() === 'male'" prepend-icon="mdi-gender-male">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.gender }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item class="drawer-item" v-if="userAuthStore.userData && userAuthStore.userData.gender.toLowerCase() === 'female'" prepend-icon="mdi-gender-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.gender }}
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item class="drawer-item" v-if="userAuthStore.userData && !['female', 'male'].includes(userAuthStore.userData.gender.toLowerCase())" prepend-icon="mdi-gender-male-female">
          <v-list-item-title class="drawer-title">
            GENDER
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.gender }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-human-child">
          <v-list-item-title class="drawer-title">
            AGE
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData?.age }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-food-variant-off">
          <v-list-item-title class="drawer-title">
            ALLERGIES
          </v-list-item-title>
          <v-list-item-subtitle v-for="allergy in userAuthStore.userData?.allergies" class="drawer-subtitle">
            {{ allergy }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item class="drawer-item" prepend-icon="mdi-heart-pulse">
          <v-list-item-title class="drawer-title">
            HEALTH CONDITIONS
          </v-list-item-title>
          <v-list-item-subtitle v-for="con in userAuthStore.userData?.health_conditions" class="drawer-subtitle">
            {{ con }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-phone-outline">
          <v-list-item-title class="drawer-title">
            PRIMARY PHONE NO.
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.contact_one }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-flag-variant-outline">
          <v-list-item-title class="drawer-title">
            NATIONALITY
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.nationality }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-home-outline">
          <v-list-item-title class="drawer-title">
            RESIDENTIAL ADDRESS
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.address }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="userAuthStore.userData" class="drawer-item" prepend-icon="mdi-email-outline">
          <v-list-item-title class="drawer-title">
            EMAIL
          </v-list-item-title>
          <v-list-item-subtitle class="drawer-subtitle">
            {{ userAuthStore.userData.email }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </div>
</template>


<style scoped>

.profile-image-container{
  width: 100%;
  padding: 10px;
  height: 190px;
}

.profile-image-container .img{
  border-radius: 30%;
  width: 150px;
  height: 150px;
}

</style>
