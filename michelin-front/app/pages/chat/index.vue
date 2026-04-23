<template>
  <div class="flex flex-col h-screen bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-black rounded-full flex items-center justify-center">
          <span class="text-white text-sm font-bold">M</span>
        </div>
        <span class="font-semibold text-gray-900">Michelin Guide</span>
      </div>
      <UButton icon="i-heroicons-plus" size="sm" variant="ghost" color="gray" />
    </div>

    <!-- Chat Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto">
      <div class="max-w-3xl mx-auto px-4 py-6">
        <!-- Empty State -->
        <div v-if="messages.length === 1" class="mt-20 text-center">
          <div class="w-16 h-16 bg-black rounded-full flex items-center justify-center mx-auto mb-6">
            <span class="text-white text-2xl font-bold">M</span>
          </div>
          <h2 class="text-2xl font-semibold text-gray-900 mb-8">How can I help you today?</h2>
          <div class="grid grid-cols-2 gap-3 max-w-xl mx-auto">
            <button
              v-for="suggestion in suggestions"
              :key="suggestion"
              :disabled="isLoading"
              @click="form.query = suggestion; handleSubmit()"
              class="text-left p-4 rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <p class="text-sm text-gray-700">{{ suggestion }}</p>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-else class="space-y-6">
          <div v-for="(message, index) in messages" :key="index">
            <!-- User Message -->
            <div v-if="message.role === 'user'" class="flex justify-end">
              <div class="max-w-[85%] bg-gray-100 rounded-3xl px-4 py-3">
                <p class="text-gray-900 whitespace-pre-wrap">{{ message.content }}</p>
              </div>
            </div>

            <!-- Assistant Message -->
            <div v-else class="flex gap-4">
              <div class="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span class="text-white text-xs font-bold">M</span>
              </div>
              <div class="flex-1 min-w-0">
                <!-- Query Analysis Chips -->
                <div v-if="message.queryAnalysis" class="flex flex-wrap gap-2 mb-3">
                  <span v-if="message.queryAnalysis.detected_location" class="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-700 rounded-md text-xs">
                    <UIcon name="i-heroicons-map-pin" class="w-3 h-3" />
                    {{ message.queryAnalysis.detected_location }}
                  </span>
                  <span v-if="message.queryAnalysis.detected_cuisine" class="inline-flex items-center gap-1 px-2 py-1 bg-orange-50 text-orange-700 rounded-md text-xs">
                    <UIcon name="i-heroicons-utensils" class="w-3 h-3" />
                    {{ message.queryAnalysis.detected_cuisine }}
                  </span>
                  <span v-if="message.queryAnalysis.detected_award" class="inline-flex items-center gap-1 px-2 py-1 bg-yellow-50 text-yellow-700 rounded-md text-xs">
                    <UIcon name="i-heroicons-star" class="w-3 h-3" />
                    {{ message.queryAnalysis.detected_award }}
                  </span>
                </div>

                <!-- Progress -->
                <div v-if="message.progress && message.progress.value < 1" class="mb-3">
                  <div class="flex items-center gap-2 text-gray-500 text-sm">
                    <div class="w-4 h-4 border-2 border-gray-300 border-t-black rounded-full animate-spin" />
                    <span>{{ message.progress.message }}</span>
                  </div>
                </div>

                <!-- Restaurant Cards -->
                <div v-if="message.restaurantCards && message.restaurantCards.length > 0" class="space-y-3 mb-4">
                  <div
                    v-for="card in message.restaurantCards"
                    :key="card.id"
                    class="p-4 rounded-xl border border-gray-200 hover:border-gray-300 transition-colors"
                  >
                    <div class="flex items-start justify-between gap-3 mb-2">
                      <h3 class="font-semibold text-gray-900">{{ card.name }}</h3>
                      <span v-if="card.badge_text" class="px-2 py-0.5 text-xs font-medium rounded-full"
                        :class="{
                          'bg-yellow-100 text-yellow-800': card.badge_color === 'yellow',
                          'bg-orange-100 text-orange-800': card.badge_color === 'orange',
                          'bg-amber-100 text-amber-800': card.badge_color === 'amber',
                          'bg-red-100 text-red-800': card.badge_color === 'red',
                          'bg-green-100 text-green-800': card.badge_color === 'green',
                        }">
                        {{ card.badge_text }}
                      </span>
                    </div>
                    <p v-if="card.cuisine" class="text-sm text-gray-600 mb-1">{{ card.cuisine }}</p>
                    <p v-if="card.distance_km" class="text-sm text-gray-500 mb-2">
                      <UIcon name="i-heroicons-map-pin" class="w-3 h-3 inline mr-1" />
                      {{ card.distance_km.toFixed(1) }} km away
                    </p>
                    <p v-if="card.description" class="text-sm text-gray-700 mb-2">{{ card.description }}</p>
                    <p v-if="card.signature_dish" class="text-sm text-red-600">
                      <UIcon name="i-heroicons-sparkles" class="w-3 h-3 inline mr-1" />
                      {{ card.signature_dish }}
                    </p>
                  </div>
                </div>

                <!-- Streaming Text with Markdown -->
                <div v-if="message.content" class="prose prose-sm max-w-none text-gray-800" v-html="renderMarkdown(message.content)"></div>

                <!-- Loading State -->
                <div v-if="message.loading" class="flex items-center gap-2 text-gray-400">
                  <div class="w-4 h-4 border-2 border-gray-300 border-t-gray-500 rounded-full animate-spin" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-gray-200 bg-white">
      <div class="max-w-3xl mx-auto p-4">
        <div class="relative flex items-center">
          <UInput
            v-model="form.query"
            placeholder="Message Michelin Guide..."
            size="lg"
            :disabled="isLoading"
            class="flex-1"
            @keydown.enter.exact.prevent="handleSubmit"
            :ui="{ wrapper: 'w-full', base: 'pr-12' }"
          />
          <UButton
            icon="i-heroicons-arrow-up"
            :loading="isLoading"
            :disabled="!form.query.trim()"
            @click="handleSubmit"
            color="black"
            size="md"
            class="absolute right-2"
            :class="form.query.trim() ? 'bg-black text-white' : 'bg-gray-200 text-gray-400'"
          />
        </div>
        <p class="text-xs text-gray-500 text-center mt-2">Michelin Guide can make mistakes. Check important info.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useChatStream, type QueryAnalysisData, type RestaurantCardData } from '~/composables/useChatStream'

// Configure marked for better rendering
marked.setOptions({
  breaks: true,
  gfm: true,
})

const renderMarkdown = (content: string) => {
  const html = marked.parse(content) as string
  return DOMPurify.sanitize(html)
}

const messagesContainer = ref<HTMLElement>()
const isLoading = ref(false)
const sessionId = ref<string>()

interface Message {
  role: 'user' | 'assistant'
  content: string
  loading?: boolean
  progress?: { value: number; message: string }
  queryAnalysis?: QueryAnalysisData
  restaurantCards?: RestaurantCardData[]
  location?: { lat: number; lng: number; location: string }
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: 'Welcome! I\'m your Michelin Guide assistant. Ask me about restaurants anywhere in the world. Try "Best 3-star restaurants in Paris" or "Romantic dinner in Tokyo".',
  }
])

const form = reactive({
  query: ''
})

const suggestions = [
  'Best 3-star restaurants in Paris',
  'Romantic dinner recommendations',
  'Japanese fine dining in Tokyo',
  'Bib Gourmand in Munich'
]

const { streamChat } = useChatStream()

watch(() => messages.value.length, () => {
  nextTick(() => {
    messagesContainer.value?.scrollTo({
      top: messagesContainer.value.scrollHeight,
      behavior: 'smooth'
    })
  })
})

async function handleSubmit() {
  const query = form.query.trim()
  if (!query || isLoading.value) return

  messages.value.push({ role: 'user', content: query })
  form.query = ''
  isLoading.value = true

  const assistantIndex = messages.value.length
  messages.value.push({
    role: 'assistant',
    content: '',
    loading: true
  })

  const currentMessage = messages.value[assistantIndex]
  let buffer = ''

  try {
    await streamChat({
      query,
      session_id: sessionId.value,
      onStep: (step, status, message) => {
        currentMessage.loading = false
        if (step === 'error') {
          currentMessage.content = `Error: ${message}`
        }
      },
      onProgress: (step, progress, message) => {
        currentMessage.progress = { value: progress, message }
      },
      onQueryAnalysis: (analysis) => {
        currentMessage.queryAnalysis = analysis
      },
      onToken: (content) => {
        currentMessage.loading = false
        buffer += content
        currentMessage.content = buffer
      },
      onRestaurantCard: (card) => {
        if (!currentMessage.restaurantCards) {
          currentMessage.restaurantCards = []
        }
        currentMessage.restaurantCards.push(card)
      },
      onDone: (data) => {
        sessionId.value = data.session_id
        currentMessage.progress = undefined
      },
      onError: (error) => {
        currentMessage.loading = false
        currentMessage.content = `Sorry, I encountered an error: ${error}`
      }
    })
  } catch (error) {
    currentMessage.loading = false
    currentMessage.content = `Connection error. Please make sure the backend server is running.`
  } finally {
    isLoading.value = false
  }
}
</script>
