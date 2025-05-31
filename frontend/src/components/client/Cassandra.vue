<script setup lang="ts">
import { AxiosError } from 'axios';
import { computed, ref, watch, nextTick } from 'vue';
import axiosInstance from '@/utils/axiosInstance';
import { useUserAuthStore } from '@/stores/userAuthStore';
import { useElementsStore } from '@/stores/elementsStore';
import TheLoader from '@/components/TheLoader.vue';
import type { Message } from '@/utils/types_utils';
import type { VNodeRef } from 'vue';
import Vue3MarkdownIt from 'vue3-markdown-it'

const userAuthStore = useUserAuthStore()
const elementsStore = useElementsStore()
const clientMessage = ref('')
const messageHistory = ref('')
const loading = ref(false)
const typedElement = ref<VNodeRef | null>(null)
const chatMessagesRef = ref<HTMLElement | null>(null)
const itemData = computed(() => {
  return userAuthStore.messages
})

watch(()=> userAuthStore.messages, (newValue, oldValue) => {
  if (newValue) {
    const newItems = newValue.filter(item => !oldValue?.some(oldItem => oldItem.id === item.id))
    newItems.forEach(item=>{
      const promptMessage = item.sender === 'user' ? `user: ${item.message}` : `cassandra: ${item.message}`
      messageHistory.value += `\n${promptMessage}`
    })
  }
}, {immediate: true, deep: 1})

watch(() => userAuthStore.messages.length, () => {
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
    else {
    }
  })
}, {immediate: true})

const sendMessage = async () => {
  loading.value = true
  const formData = new FormData()
  formData.append('type', 'sendMessage')
  formData.append('history', messageHistory.value)
  formData.append('clientData', JSON.stringify(userAuthStore.userData) || '')
  formData.append('message', clientMessage.value)

  try {
    const response = await axiosInstance.post('client/data', formData)
    const data: Message[] = response.data
    userAuthStore.messages.push(data[0])
    userAuthStore.messages.push(data[1])
    clientMessage.value = ''
    
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
  finally {
    loading.value = false
  }
}


</script>

<template>
  <div class="content-wrapper" v-show="elementsStore.activePage === 'Cassandra'" :class="{ 'is-active-page': elementsStore.activePage === 'Cassandra' }">

    <TheLoader v-if="!userAuthStore.fetchedDataLoaded" :func="userAuthStore.getClientData" />
    <div class="chat-container">
      <div class="chat-messages" id="chatMessages" ref="chatMessagesRef">
        <div class="chat-message message-assistant">Hi! How can I help you today?</div>
        <div class="chat-message" v-for="(msg, index) in itemData" :key="msg.id" :ref="index === itemData.length - 1 ? typedElement : undefined" :class="{'message-user': msg.sender === 'user', 'message-assistant': msg.sender === 'cassandra'}">
          <vue3-markdown-it :source="msg.message" />
        </div>
      </div>
      <div class="chat-input-area">
        <v-text-field class="chat-input" @keydown.enter="sendMessage" :disabled="loading" v-model="clientMessage" variant="outlined" clearable placeholder="ask cassandra anything" />
        <v-btn class="send-btn" @click="sendMessage()" variant="flat" :disabled="!clientMessage" :loading="loading " :size="elementsStore.btnSize2" >Send</v-btn>
      </div>
    </div>
  </div>
</template>

<style scoped>

.chat-container {
  width: 100%;
  height: 100%;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.chat-message {
  max-width: 70%;
  padding: 10px 30px !important;
  margin-bottom: 10px;
  border-radius: 16px;
  line-height: 1.4;
}

.message-user {
  align-self: flex-end;
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-assistant {
  align-self: flex-start;
  background-color: #e9ecef;
  color: #333;
  border-bottom-left-radius: 4px;
}

.chat-input-area {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #fafafa;
  height: 80px;
}

.chat-input {
  font-size: 14px;
  height: 100% !important;
}

.send-btn {
  margin-left: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-btn:hover {
  background-color: #0056b3;
}
</style>
