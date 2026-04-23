<template>
  <div class="flex flex-col h-screen bg-white">
    <!-- Header - Michelin Guide Branding -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center shadow-md">
          <span class="text-white text-lg font-bold">M</span>
        </div>
        <div>
          <span class="font-bold text-gray-900 text-lg">Michelin Guide</span>
          <p class="text-xs text-gray-500">AI Restaurant Assistant</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <NuxtLink to="/">
          <UButton icon="i-heroicons-home" size="sm" variant="ghost" color="gray" />
        </NuxtLink>
      </div>
    </div>

    <!-- Chat Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto bg-gradient-to-b from-gray-50 to-white">
      <div class="max-w-4xl mx-auto px-4 py-6">
        <!-- Empty State -->
        <div v-if="messages.length === 1" class="mt-12 md:mt-20 text-center">
          <div class="w-20 h-20 bg-gradient-to-br from-red-600 to-red-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
            <UIcon name="i-heroicons-sparkles" class="w-10 h-10 text-white" />
          </div>
          <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-3">Discover Exceptional Dining</h2>
          <p class="text-gray-600 mb-8 max-w-md mx-auto">Explore Michelin-rated restaurants worldwide with AI-powered recommendations.</p>

          <!-- Michelin Award Guide -->
          <div class="flex flex-wrap justify-center gap-2 mb-8">
            <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-red-50 text-red-700 rounded-full text-sm font-medium">
              <span class="w-2 h-2 bg-red-600 rounded-full"></span>
              3 Stars
            </span>
            <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-orange-50 text-orange-700 rounded-full text-sm font-medium">
              <span class="w-2 h-2 bg-orange-500 rounded-full"></span>
              2 Stars
            </span>
            <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-amber-50 text-amber-700 rounded-full text-sm font-medium">
              <span class="w-2 h-2 bg-amber-500 rounded-full"></span>
              1 Star
            </span>
            <span class="inline-flex items-center gap-1 px-3 py-1.5 bg-yellow-50 text-yellow-700 rounded-full text-sm font-medium">
              <UIcon name="i-heroicons-face-smile" class="w-3 h-3" />
              Bib Gourmand
            </span>
          </div>

          <!-- Suggestion Questions -->
          <h3 class="text-sm font-medium text-gray-700 mb-3">Try asking:</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
            <button
              v-for="suggestion in suggestions"
              :key="suggestion.text"
              :disabled="isLoading"
              @click="form.query = suggestion.text; handleSubmit()"
              class="text-left p-4 rounded-xl border border-gray-200 hover:border-red-300 hover:bg-red-50/50 transition-all group"
            >
              <p class="text-sm text-gray-700 font-medium mb-1">{{ suggestion.text }}</p>
              <p class="text-xs text-gray-500">{{ suggestion.desc }}</p>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-else class="space-y-6">
          <div v-for="(message, index) in messages" :key="index">
            <!-- User Message -->
            <div v-if="message.role === 'user'" class="flex justify-end">
              <div class="max-w-[85%] bg-red-600 text-white rounded-3xl rounded-br-md px-4 py-3 shadow-sm">
                <p class="whitespace-pre-wrap">{{ message.content }}</p>
              </div>
            </div>

            <!-- Assistant Message -->
            <div v-else class="flex gap-4">
              <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center flex-shrink-0 mt-1 shadow-md">
                <span class="text-white text-sm font-bold">M</span>
              </div>
              <div class="flex-1 min-w-0">
                <!-- Query Analysis Chips -->
                <div v-if="message.queryAnalysis" class="flex flex-wrap gap-2 mb-3">
                  <span v-if="message.queryAnalysis.detected_location" class="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-md text-sm font-medium">
                    <UIcon name="i-heroicons-map-pin" class="w-4 h-4" />
                    {{ message.queryAnalysis.detected_location }}
                  </span>
                  <span v-if="message.queryAnalysis.detected_cuisine" class="inline-flex items-center gap-1 px-3 py-1.5 bg-orange-50 text-orange-700 rounded-md text-sm font-medium">
                    <UIcon name="i-heroicons-utensils" class="w-4 h-4" />
                    {{ message.queryAnalysis.detected_cuisine }}
                  </span>
                  <span v-if="message.queryAnalysis.detected_award" class="inline-flex items-center gap-1 px-3 py-1.5 bg-red-50 text-red-700 rounded-md text-sm font-medium">
                    <UIcon name="i-heroicons-star" class="w-4 h-4" />
                    {{ message.queryAnalysis.detected_award }}
                  </span>
                </div>

                <!-- Progress -->
                <div v-if="message.progress && message.progress.value < 1" class="mb-3">
                  <div class="flex items-center gap-2 text-gray-600 text-sm">
                    <div class="w-4 h-4 border-2 border-gray-300 border-t-red-600 rounded-full animate-spin" />
                    <span>{{ message.progress.message }}</span>
                  </div>
                </div>

                <!-- Restaurant Cards -->
                <div v-if="message.restaurantCards && message.restaurantCards.length > 0" class="space-y-3 mb-4">
                  <div
                    v-for="card in message.restaurantCards"
                    :key="card.id"
                    class="p-4 rounded-xl border border-gray-200 hover:border-red-200 hover:shadow-md transition-all"
                  >
                    <div class="flex items-start justify-between gap-3 mb-2">
                      <div class="flex-1">
                        <div class="flex items-center gap-2 mb-1">
                          <h3 class="font-bold text-gray-900">{{ card.name }}</h3>
                          <span v-if="card.badge_text" class="px-2 py-0.5 text-xs font-semibold rounded-full"
                            :class="{
                              'bg-red-100 text-red-800': card.badge_color === 'red',
                              'bg-orange-100 text-orange-800': card.badge_color === 'orange',
                              'bg-amber-100 text-amber-800': card.badge_color === 'amber',
                              'bg-yellow-100 text-yellow-800': card.badge_color === 'yellow',
                              'bg-green-100 text-green-800': card.badge_color === 'green',
                            }">
                            {{ card.badge_text }}
                          </span>
                        </div>
                        <p v-if="card.cuisine" class="text-sm text-gray-600">{{ card.cuisine }}</p>
                      </div>
                      <p v-if="card.distance_km" class="text-xs text-gray-500 whitespace-nowrap">
                        {{ card.distance_km.toFixed(1) }} km
                      </p>
                    </div>
                    <p v-if="card.location" class="text-sm text-gray-600 mb-2">
                      <UIcon name="i-heroicons-map-pin" class="w-3 h-3 inline mr-1" />
                      {{ card.location }}
                    </p>
                    <p v-if="card.description" class="text-sm text-gray-700 mb-2">{{ card.description }}</p>
                    <p v-if="card.signature_dish" class="text-sm text-red-600 font-medium">
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

    <!-- Floating Assist Button -->
    <div v-if="!showAssistMenu" class="fixed bottom-24 right-4 md:right-8 z-50">
      <UButton
        icon="i-heroicons-light-bulb"
        size="lg"
        color="red"
        class="rounded-full shadow-lg hover:shadow-xl transition-shadow"
        @click="showAssistMenu = true"
      >
        <span class="ml-2 hidden md:inline">Quick Assist</span>
      </UButton>
    </div>

    <!-- Assist Menu Popup -->
    <div v-if="showAssistMenu" class="fixed bottom-24 right-4 md:right-8 z-50 w-72 bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-light-bulb" class="w-5 h-5 text-red-600" />
            <span class="font-semibold text-gray-900">Quick Suggestions</span>
          </div>
          <UButton
            icon="i-heroicons-x-mark"
            size="sm"
            variant="ghost"
            color="gray"
            @click="showAssistMenu = false"
          />
        </div>
      </div>
      <div class="p-2 max-h-80 overflow-y-auto">
        <button
          v-for="suggestion in quickAssistOptions"
          :key="suggestion.text"
          @click="form.query = suggestion.text; showAssistMenu = false; handleSubmit()"
          class="w-full text-left p-3 rounded-xl hover:bg-red-50 transition-colors group"
        >
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center" :class="suggestion.color">
              <UIcon :name="suggestion.icon" class="w-4 h-4" :class="suggestion.iconColor" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ suggestion.text }}</p>
              <p class="text-xs text-gray-500">{{ suggestion.desc }}</p>
            </div>
            <UIcon name="i-heroicons-chevron-right" class="w-4 h-4 text-gray-400 group-hover:text-red-600" />
          </div>
        </button>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-gray-200 bg-white">
      <div class="max-w-4xl mx-auto p-4">
        <div class="relative flex items-center gap-2">
          <UButton
            icon="i-heroicons-microphone"
            size="md"
            variant="outline"
            color="gray"
            :disabled="isLoading"
            class="shrink-0"
          />
          <UInput
            v-model="form.query"
            placeholder="Ask about Michelin-rated restaurants..."
            size="lg"
            :disabled="isLoading"
            class="flex-1"
            @keydown.enter.exact.prevent="handleSubmit"
            :ui="{ wrapper: 'w-full', base: 'pr-12' }"
          />
          <UButton
            icon="i-heroicons-paper-airplane"
            :loading="isLoading"
            :disabled="!form.query.trim()"
            @click="handleSubmit"
            color="red"
            size="md"
            class="shrink-0"
            :class="form.query.trim() ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-gray-200 text-gray-400'"
          />
        </div>
        <div class="flex items-center justify-between mt-2">
          <p class="text-xs text-gray-500">
            Powered by Michelin Guide data
          </p>
          <button
            @click="showAssistMenu = true"
            class="text-xs text-red-600 hover:text-red-700 flex items-center gap-1"
          >
            <UIcon name="i-heroicons-light-bulb" class="w-3 h-3" />
            Need ideas?
          </button>
        </div>
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
const showAssistMenu = ref(false)

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
    content: 'Welcome! I\'m your Michelin Guide assistant. I can help you discover exceptional restaurants worldwide - from casual Bib Gourmand spots to prestigious 3-Michelin-starred establishments. Try asking me about restaurants in a specific city, cuisine type, or award level.',
  }
])

const form = reactive({
  query: ''
})

const suggestions = [
  { text: '3-star restaurants in Paris', desc: 'Find the finest dining experiences' },
  { text: 'Romantic dinner in Tokyo', desc: 'Intimate settings for two' },
  { text: 'Bib Gourmand in London', desc: 'Great food at moderate prices' },
  { text: 'Best sushi in New York', desc: 'Top-rated Japanese cuisine' },
]

const quickAssistOptions = [
  { text: '3-star restaurants near me', desc: 'Exceptional dining nearby', icon: 'i-heroicons-star', color: 'bg-red-100', iconColor: 'text-red-600' },
  { text: 'Romantic dinner spots', desc: 'Intimate settings for two', icon: 'i-heroicons-heart', color: 'bg-pink-100', iconColor: 'text-pink-600' },
  { text: 'Bib Gourmand recommendations', desc: 'Great value dining', icon: 'i-heroicons-face-smile', color: 'bg-yellow-100', iconColor: 'text-yellow-600' },
  { text: 'Best Italian restaurants', desc: 'Authentic cuisine', icon: 'i-heroicons-globe-alt', color: 'bg-green-100', iconColor: 'text-green-600' },
  { text: 'Michelin Guide in Paris', desc: 'French excellence', icon: 'i-heroicons-map-pin', color: 'bg-blue-100', iconColor: 'text-blue-600' },
  { text: 'Vegetarian fine dining', desc: 'Plant-based gourmet', icon: 'i-heroicons-leaf', color: 'bg-emerald-100', iconColor: 'text-emerald-600' },
  { text: 'Seafood specialties', desc: 'Fresh catch', icon: 'i-heroicons-fish', color: 'bg-cyan-100', iconColor: 'text-cyan-600' },
  { text: 'Wine cellar restaurants', desc: 'Perfect pairings', icon: 'i-heroicons-wine', color: 'bg-purple-100', iconColor: 'text-purple-600' },
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
