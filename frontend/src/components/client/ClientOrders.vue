<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, watch } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';
import { formatDate, formatNumberAsCurrency } from '@/utils/util';

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()

const itemData = computed(() => {
  return userAuthStore.clientOrders
})

const itemHeaders = [
  { title: 'DATE', key: 'date', sortable: true },
  { title: 'TOTAL PRICE', key: 'total_price', sortable: true },
  { title: 'STATUS', key: 'status', sortable: true },
  { title: 'ITEMS', key: 'items', sortable: false },
  { title: 'ADDRESS', key: 'address', sortable: true },
  { title: '', key: 'action', sortable: false },
];

const deleteItem = async (item_id: number) => {
  elementsStore.ShowLoadingOverlay()
  const formData = new FormData()
  formData.append('type', 'deleteOrder')
  formData.append('itemId', item_id.toString())

  try {
    await axiosInstance.post('client/data', formData)
    const itemToDelete = userAuthStore.clientOrders.find(item => item.id === item_id)
    if (itemToDelete) {
      itemToDelete.items.forEach(item=> {
        const drugItemObj = userAuthStore.drugs.find(subItem=> subItem.stocks.some(stock=> stock.id === item.drug.id))
        if (drugItemObj) {
          const stockItemObj = drugItemObj.stocks.find(stock=> stock.id === item.drug.id)
          stockItemObj ? stockItemObj.quantity = Number(stockItemObj.quantity) + Number(item.quantity) : null
        }
        
      })
      const itemtoDeleteIndex = userAuthStore.clientOrders.indexOf(itemToDelete)
      itemtoDeleteIndex !== -1 ? userAuthStore.clientOrders.splice(itemtoDeleteIndex, 1) : null
    }
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

</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'ClientOrders'" :class="{ 'is-active-page': elementsStore.activePage === 'ClientOrders' }">

    <TheLoader v-if="!userAuthStore.fetchedDataLoaded" :func="userAuthStore.getClientData" />
    <div class="content-header" v-if="userAuthStore.fetchedDataLoaded">
      <h4 class="content-header-title">ORDERS</h4>
    </div>
    <v-data-table-virtual class="table" v-if="userAuthStore.fetchedDataLoaded" :headers="itemHeaders.filter(item=> item.key !== 'data-table-expand')" :items="itemData" fixed-header multi-sort>
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
      <template #item.date="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ formatDate(item.date, 'short') }}</v-chip>
        </div>
      </template>
      <template #item.total_price="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">GHS {{ formatNumberAsCurrency(item.total_price) }}</v-chip>
        </div>
      </template>
      <template #item.status="{ item }">
        <div class="flex-all">
          <v-icon size="x-small" :color="item.status.toLowerCase() === 'delivered' ? 'green' : 'yellow'" icon="mdi-circle" />
          <v-chip class="ml-2" size="x-small">{{ item.status.toUpperCase() }}</v-chip>
        </div>
      </template>
      <template #item.items="{ internalItem, isExpanded, toggleExpand }">
        <v-chip class="chip-link" @click="toggleExpand(internalItem)" :size="elementsStore.btnSize1" color="blue">{{ isExpanded(internalItem) ? 'hide' : 'show' }}</v-chip>
      </template>
      <template v-slot:expanded-row="{ columns, item }">
        <tr>
          <td :colspan="columns.length">
            <v-sheet class="mb-10" rounded="lg">
              <v-table style="max-width: 800px;" density="compact">
                <thead class="bg-surface-light">
                  <tr>
                    <th class="table-head">MEDICATION</th>
                    <th class="table-head">QUANTITY</th>
                    <th class="table-head">COST PER UNIT</th>
                    <th class="table-head">TOTAL PRICE</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="_item_ in item.items">
                    <td class="table-data">
                      <v-chip :size="elementsStore.btnSize1">{{ _item_.drug.name }}</v-chip>
                    </td>
                    <td class="table-data">
                      <v-chip :size="elementsStore.btnSize1">{{ _item_.quantity }}</v-chip>
                    </td>
                    <td class="table-data">
                      <v-chip :size="elementsStore.btnSize1">GHS {{formatNumberAsCurrency(_item_.price) }}</v-chip>
                    </td>
                    <td class="table-data">
                      <v-chip :size="elementsStore.btnSize1">GHS {{formatNumberAsCurrency(_item_.total_price) }}</v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-sheet>
          </td>
        </tr>
      </template>
      <template #item.address="{ item }">
        <div class="flex-all">
          <v-chip :size="elementsStore.btnSize1">{{ item.address }}</v-chip>
        </div>
      </template>
      <template #item.action="{ item }">
        <div class="flex-all">
          <v-btn class="mx-1" v-if="item.status?.toLowerCase() === 'processing'" color="red" size="x-small" icon="mdi-delete" variant="flat"
            @click="elementsStore.ShowDeletionOverlay(() => deleteItem(item.id), 'Are you sure you want to cancel this order?')"
          />
        </div>
      </template>
      <template #item.data-table-expand="{ item }"></template>
    </v-data-table-virtual>
  </div>
</template>

<style scoped>


</style>
