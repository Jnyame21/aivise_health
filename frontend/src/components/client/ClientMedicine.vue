<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, watch } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';
import type { Drug, Order, DrugStock } from '@/utils/types_utils';
import NoData from '@/components/NoData.vue';
import { formatNumberAsCurrency } from '@/utils/util';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const itemProperties = ref<Drug | null>(null)
const itemSearch = ref('')
const cartItems = ref<DrugStock[]>([])
const itemData = computed(() => {
  return userAuthStore.drugs
})

const itemHeaders = [
  { title: 'MEDICATION', key: 'name', sortable: true },
  { title: 'GENERIC NAME', key: 'generic_name', sortable: true },
  { title: 'BRAND NAME', key: 'brand', sortable: true },
  { title: 'DESCRIPTION', key: 'description', sortable: false },
  { title: 'FORM (TABLET, SYRUP, ETC.)', key: 'dosage_form', sortable: false },
  { title: "HOW IT'S TAKEN (ROUTE)", key: 'route', sortable: false },
  { title: 'USED FOR', key: 'indications', sortable: false },
  { title: 'POSSIBLE SIDE EFFECTS', key: 'side_effects', sortable: false },
  { title: 'PRECAUTIONS', key: 'precautions', sortable: false },
  { title: 'MAIN  INGREDIENTS', key: 'active_ingredients', sortable: false },
  { title: 'WARNINGS', key: 'warnings', sortable: false },
  { title: 'STORAGE', key: 'storage', sortable: false },
  { title: 'MANUFACTURER', key: 'manufacturer', sortable: true },
];

const addToCart = (item: Drug) => {
  item.stocks.forEach(stock=>{
    const existingItem = cartItems.value.find(cartItem => cartItem.id === item.id)
    existingItem ? null : cartItems.value.push(stock)
  })
}

const removeItemFromCart = (item: DrugStock) => {
  const itemIndex = cartItems.value.findIndex(cartItem => cartItem.id === item.id)
  if (itemIndex !== -1){
    cartItems.value.splice(itemIndex, 1)
  }
}

const placeOrder = async () => {
  if (cartItems.value.length === 0){
    elementsStore.ShowOverlay('You cart is empty. Please check your cart', 'red')
    return;
  }
  const invalueValue = cartItems.value.find(item=> !Number.isInteger(Number(item.order_quantity)) || Number(item.order_quantity) < 0)
  if (invalueValue){
    elementsStore.ShowOverlay('Item quantities must be positive whole numbers. Please check your cart', 'red')
    return;
  }
  const exceedItem = cartItems.value.find(item=> Number(item.order_quantity) > Number(item.quantity))
  if (exceedItem){
    elementsStore.ShowOverlay('Item quantities cannot exceed stock levels. Please check your cart', 'red')
    return;
  }

  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'placeOrder')
  formData.append('orderItems', JSON.stringify(cartItems.value))
  try {
    const response = await axiosInstance.post('client/data', formData)
    const data: Order = response.data
    data.items.forEach(item=>{
      const drugItem = userAuthStore.drugs.find(subItem=> subItem.stocks.some(stock=> stock.id === item.drug.id))
      if (drugItem){
        const drugStockItem = drugItem.stocks.find(subItem=> subItem.id === item.drug.id)
        if (drugStockItem){
          const newStock = Math.max(Number(drugStockItem.quantity) - Number(item.quantity), 0)
          drugStockItem.quantity = newStock
        }
      }
    })
    userAuthStore.clientOrders.unshift(data)
    cartItems.value = []
    closeOverlay('DrugCartItemsOverlay')
    elementsStore.HideLoadingOverlay()
    elementsStore.ShowOverlay('Order placed successfully', 'green')
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

const showOverlay = (element: string, item_properties: Drug | null = null) => {
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
  <div class="content-wrapper" v-show="elementsStore.activePage === 'ClientMedicine'" :class="{ 'is-active-page': elementsStore.activePage === 'ClientMedicine' }">

    <!-- Item description Overlay -->
    <div id="DrugDescriptionOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugDescriptionOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Description</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          <pre>{{ itemProperties.description }}</pre>
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Item indications Overlay -->
    <div id="DrugIndicationOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugIndicationOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Indications</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          {{ itemProperties.indications }}
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Item side effects Overlay -->
    <div id="DrugSideEffectsOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugSideEffectsOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Side effects</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          {{ itemProperties.side_effects }}
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Item precautions Overlay -->
    <div id="DrugPrecautionsOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugPrecautionsOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Precautions</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          {{ itemProperties.precautions }}
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Item warnings Overlay -->
    <div id="DrugWarningsOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugWarningsOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Warnings</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          {{ itemProperties.warnings }}
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Item storage Overlay -->
    <div id="DrugStorageOverlay" class="overlay">
      <div class="overlay-card">
        <v-btn @click="closeOverlay('DrugStorageOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-info-container" v-if="itemProperties">
          <v-chip :size="elementsStore.btnSize2" color="blue">{{itemProperties.name}}: Storage</v-chip>
        </div>
        <div class="overlay-card-content-container" v-if="itemProperties">
          {{ itemProperties.storage }}
        </div>
        <div class="overlay-card-action-btn-container"></div>
      </div>
    </div>

    <!-- Cart items Overlay -->
    <div id="DrugCartItemsOverlay" class="overlay">
      <div class="overlay-card cart-items-card">
        <v-btn @click="closeOverlay('DrugCartItemsOverlay')" color="red" size="small" variant="flat" class="close-btn">X</v-btn>
        <div class="overlay-card-content-container" style="margin-top: 3em;">
          <NoData :message="`There are no items in cart`" v-if="cartItems.length === 0" />
          <v-table fixed-header class="table" v-if="cartItems.length > 0">
            <thead>
              <tr>
                <th class="table-head">MEDICATION</th>
                <th class="table-head">QUANTITY</th>
                <th class="table-head">PRICE PER UNIT</th>
                <th class="table-head">AVAILABLE STOCK</th>
                <th class="table-head">ACTION</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="_item_ in cartItems" :key="_item_.id">
                <td class="table-data">
                  {{ _item_.name}}
                </td>
                <td class="table-data">
                  <v-text-field class="input-field" v-model="_item_.order_quantity" label="QUANTITY" type="number" clearable variant="solo-filled" density="comfortable" hint="Enter the quantity you want to order" persistent-hint />
                </td>
                <td class="table-data">
                  <v-chip :size="elementsStore.btnSize1">GHS {{ formatNumberAsCurrency(_item_.price) }}</v-chip>
                </td>
                <td class="table-data">
                  <v-chip :size="elementsStore.btnSize1">{{ _item_.quantity}}</v-chip>
                </td>
                <td class="table-data">
                  <v-btn color="red" size="x-small" variant="flat" icon="mdi-delete" @click="removeItemFromCart(_item_)" />
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
        <div class="overlay-card-action-btn-container" v-if="cartItems.length > 0">
          <v-btn @click="placeOrder"
            :ripple="false" variant="flat" type="submit" color="black" size="small" append-icon="mdi-checkbox-marked-circle">
            PLACE ORDER
          </v-btn>
        </div>
      </div>
    </div>

    <TheLoader v-if="!userAuthStore.fetchedDataLoaded" :func="userAuthStore.getClientData" />
    <div class="content-header" v-if="userAuthStore.fetchedDataLoaded">
      <h4 class="content-header-title">MEDICATIONS</h4>
    </div>
    <v-data-table-virtual class="table" v-if="userAuthStore.fetchedDataLoaded" :headers="itemHeaders.filter(item=> item.key !== 'data-table-expand')" :items="itemData" :search="itemSearch" fixed-header multi-sort>
      <template v-slot:top>
        <v-toolbar color="#333333">
          <v-text-field class="ml-2" v-model="itemSearch" label="Search" prepend-inner-icon="mdi-magnify" variant="solo-filled" density="compact" />
          <v-spacer></v-spacer>
          <v-icon @click="showOverlay('DrugCartItemsOverlay')" icon="mdi-cart-outline" size="x-large" style="position: absolute; top: 0; right: 0; margin-right: 1.4em;" />
          <v-chip @click="showOverlay('DrugCartItemsOverlay')" color="white" style="position: absolute; top: 0; right: 0; margin-right: 1em;">{{ cartItems.length }}</v-chip>
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
          <v-chip style="margin: auto" :size="elementsStore.btnSize1">{{ item.name }}</v-chip>
          <v-btn @click="addToCart(item)" color="green" size="x-small"
            :ripple="false" variant="flat">
            ADD TO CART
          </v-btn>
        </div>
      </template>
      <template #item.generic_name="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.generic_name }}</v-chip>
        </div>
      </template>
      <template #item.brand="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.brand }}</v-chip>
        </div>
      </template>
      <template #item.description="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugDescriptionOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.dosage_form="{ item }">
        <div class="flex-all">
          <v-chip class="ma-1" v-for="dosage in item.dosage_form" :size="elementsStore.btnSize1">{{ dosage }}</v-chip>
        </div>
      </template>
      <template #item.route="{ item }">
        <div class="flex-all">
          <v-chip class="ma-1" v-for="route in item.route" :size="elementsStore.btnSize1">{{ route }}</v-chip>
        </div>
      </template>
      <template #item.indications="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugIndicationOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.side_effects="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugSideEffectsOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.precautions="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugPrecautionsOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.active_ingredients="{ item }">
        <div class="flex-all-c">
          <v-chip class="ma-1" v-for="ingre in item.active_ingredients" :size="elementsStore.btnSize1">{{ ingre }}</v-chip>
        </div>
      </template>
      <template #item.warnings="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugWarningsOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.storage="{ item }">
        <div class="flex-all">
          <v-chip class="chip-link" @click="showOverlay('DrugStorageOverlay', item)" color="blue" :size="elementsStore.btnSize1">show</v-chip>
        </div>
      </template>
      <template #item.manufacturer="{ item }">
        <div class="flex-all">
          <v-chip v-if="item.manufacturer" :size="elementsStore.btnSize1">{{ item.manufacturer }}</v-chip>
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
.cart-items-card {
  max-width: 1000px !important;
}
</style>
