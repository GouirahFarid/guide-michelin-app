<template>
  <div class="chat-widget-container">
    <!-- Floating Toggle Button -->
    <button
      class="chat-toggle-btn fixed z-[9999] shadow-lg rounded-full flex items-center justify-center transition-all duration-300"
      :class="[
        props.buttonClass,
        isOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100'
      ]"
      aria-label="Open chat"
      @click="toggleChat"
    >
      <UIcon name="i-heroicons-chat-bubble-oval-ellipsis" class="w-6 h-6 text-white" />
    </button>

    <!-- Chat Overlay/Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="fixed inset-0 bg-black/50 z-[9998]"
          @click="closeChat"
        />
      </Transition>

      <Transition
        enter-active-class="transition-all duration-300"
        :enter-from-class="isMobile ? 'translate-y-full' : 'scale-95 opacity-0'"
        :enter-to-class="isMobile ? 'translate-y-0' : 'scale-100 opacity-100'"
        leave-active-class="transition-all duration-300"
        :leave-from-class="isMobile ? 'translate-y-0' : 'scale-100 opacity-100'"
        :leave-to-class="isMobile ? 'translate-y-full' : 'scale-95 opacity-0'"
      >
        <div
          v-if="isOpen"
          class="fixed z-[9999] bg-white shadow-2xl flex flex-col"
          :class="[
            isMobile
              ? 'inset-0 rounded-none'
              : 'bottom-4 right-4 w-[400px] h-[600px] rounded-2xl'
          ]"
        >
          <!-- Header -->
          <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200 shrink-0">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-black rounded-full flex items-center justify-center">
                <span class="text-white text-xs font-bold">M</span>
              </div>
              <div>
                <p class="font-semibold text-sm text-gray-900">Michelin Guide</p>
                <p class="text-xs text-gray-500">AI Assistant</p>
              </div>
            </div>
            <button
              class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
              @click="closeChat"
            >
              <UIcon name="i-heroicons-x-mark" class="w-5 h-5 text-gray-600" />
            </button>
          </div>

          <!-- Messages -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto">
            <div class="p-4">
              <!-- Empty State -->
              <div v-if="messages.length === 1" class="text-center py-8">
                <div class="w-12 h-12 bg-black rounded-full flex items-center justify-center mx-auto mb-4">
                  <span class="text-white text-lg font-bold">M</span>
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">Hi there!</h3>
                <p class="text-sm text-gray-600 mb-6">Ask me about Michelin restaurants anywhere</p>
                <div class="grid grid-cols-1 gap-2">
                  <button
                    v-for="suggestion in suggestions"
                    :key="suggestion"
                    :disabled="isLoading"
                    @click="form.query = suggestion; handleSubmit()"
                    class="text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-sm text-gray-700"
                  >
                    {{ suggestion }}
                  </button>
                </div>
              </div>

              <!-- Messages -->
              <div v-else class="space-y-4">
                <div v-for="(message, index) in messages" :key="index">
                  <!-- User Message -->
                  <div v-if="message.role === 'user'" class="flex justify-end">
                    <div class="max-w-[85%] bg-gray-100 rounded-2xl px-3 py-2">
                      <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ message.content }}</p>
                    </div>
                  </div>

                  <!-- Assistant Message -->
                  <div v-else class="flex gap-3">
                    <div class="w-7 h-7 bg-black rounded-full flex items-center justify-center flex-shrink-0">
                      <span class="text-white text-xs font-bold">M</span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <!-- Query Analysis Chips -->
                      <div v-if="message.queryAnalysis" class="flex flex-wrap gap-1.5 mb-2">
                        <span v-if="message.queryAnalysis.detected_location" class="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-50 text-blue-700 rounded-md text-xs">
                          <UIcon name="i-heroicons-map-pin" class="w-3 h-3" />
                          {{ message.queryAnalysis.detected_location }}
                        </span>
                        <span v-if="message.queryAnalysis.detected_cuisine" class="inline-flex items-center gap-1 px-2 py-0.5 bg-orange-50 text-orange-700 rounded-md text-xs">
                          <UIcon name="i-heroicons-utensils" class="w-3 h-3" />
                          {{ message.queryAnalysis.detected_cuisine }}
                        </span>
                        <span v-if="message.queryAnalysis.detected_award" class="inline-flex items-center gap-1 px-2 py-0.5 bg-yellow-50 text-yellow-700 rounded-md text-xs">
                          <UIcon name="i-heroicons-star" class="w-3 h-3" />
                          {{ message.queryAnalysis.detected_award }}
                        </span>
                      </div>

                      <!-- Progress -->
                      <div v-if="message.progress && message.progress.value < 1" class="mb-2">
                        <div class="flex items-center gap-2 text-gray-500 text-xs">
                          <div class="w-3 h-3 border-2 border-gray-300 border-t-black rounded-full animate-spin" />
                          <span>{{ message.progress.message }}</span>
                        </div>
                      </div>

                      <!-- Restaurant Cards -->
                      <div v-if="message.restaurantCards && message.restaurantCards.length > 0" class="space-y-2 mb-3">
                        <div
                          v-for="card in message.restaurantCards"
                          :key="card.id"
                          class="p-3 rounded-lg border border-gray-200"
                        >
                          <div class="flex items-start justify-between gap-2 mb-1">
                            <h3 class="font-semibold text-sm text-gray-900">{{ card.name }}</h3>
                            <span v-if="card.badge_text" class="px-1.5 py-0.5 text-xs font-medium rounded-full shrink-0"
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
                          <p v-if="card.cuisine" class="text-xs text-gray-600 mb-1">{{ card.cuisine }}</p>
                          <p v-if="card.distance_km" class="text-xs text-gray-500 mb-1">
                            <UIcon name="i-heroicons-map-pin" class="w-3 h-3 inline mr-0.5" />
                            {{ card.distance_km.toFixed(1) }} km
                          </p>
                          <p v-if="card.description" class="text-xs text-gray-700 mb-1 line-clamp-2">{{ card.description }}</p>
                        </div>
                      </div>

                      <!-- Streaming Text with Markdown -->
                      <div v-if="message.content" class="prose prose-sm max-w-none text-xs text-gray-800" v-html="renderMarkdown(message.content)"></div>

                      <!-- Loading State -->
                      <div v-if="message.loading" class="flex items-center gap-2 text-gray-400">
                        <div class="w-3 h-3 border-2 border-gray-300 border-t-gray-500 rounded-full animate-spin" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input -->
          <div class="border-t border-gray-200 p-3 shrink-0">
            <div class="relative flex items-center">
              <UInput
                v-model="form.query"
                placeholder="Ask about restaurants..."
                size="md"
                :disabled="isLoading"
                class="flex-1"
                @keydown.enter.exact.prevent="handleSubmit"
                :ui="{ wrapper: 'w-full', base: 'pr-10' }"
              />
              <UButton
                icon="i-heroicons-arrow-up"
                :loading="isLoading"
                :disabled="!form.query.trim()"
                @click="handleSubmit"
                size="sm"
                class="absolute right-1.5"
                :class="form.query.trim() ? 'bg-black text-white' : 'bg-gray-200 text-gray-400'"
              />
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useChatStream, type QueryAnalysisData, type RestaurantCardData } from '~/composables/useChatStream'

marked.setOptions({
  breaks: true,
  gfm: true,
})

const renderMarkdown = (content: string) => {
  const html = marked.parse(content) as string
  return DOMPurify.sanitize(html)
}

interface Props {
  buttonClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  buttonClass: 'bottom-6 right-6'
})

const isOpen = ref(false)
const messagesContainer = ref<HTMLElement>()
const isLoading = ref(false)
const sessionId = ref<string>()

// Detect mobile
const isMobile = ref(true)
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

interface Message {
  role: 'user' | 'assistant'
  content: string
  loading?: boolean
  progress?: { value: number; message: string }
  queryAnalysis?: QueryAnalysisData
  restaurantCards?: RestaurantCardData[]
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: 'Hi! I\'m your Michelin Guide assistant. Ask me about restaurants anywhere in the world!',
  }
])

const form = reactive({
  query: ''
})

const suggestions = [
  'Best restaurants in Paris',
  '3 stars near me',
  'Romantic dinner spots',
  'Bib Gourmand recommendations'
]

const { streamChat } = useChatStream()

function toggleChat() {
  isOpen.value = !isOpen.value
}

function closeChat() {
  isOpen.value = false
}

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
    currentMessage.content = `Connection error. Please try again.`
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.chat-toggle-btn {
  width: 56px;
  height: 56px;
  background: #000;
}

.chat-toggle-btn:hover {
  background: #222;
  transform: scale(1.05);
}

/* Markdown prose styles */
.prose {
  line-height: 1.6;
}

.prose :deep(p) {
  margin-bottom: 0.75rem;
}

.prose :deep(p:last-child) {
  margin-bottom: 0;
}

.prose :deep(h1),
.prose :deep(h2),
.prose :deep(h3) {
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.prose :deep(h1) {
  font-size: 1.25rem;
}

.prose :deep(h2) {
  font-size: 1.125rem;
}

.prose :deep(h3) {
  font-size: 1rem;
}

.prose :deep(ul),
.prose :deep(ol) {
  padding-left: 1.25rem;
  margin-bottom: 0.75rem;
}

.prose :deep(li) {
  margin-bottom: 0.25rem;
}

.prose :deep(strong) {
  font-weight: 600;
}

.prose :deep(a) {
  color: #2563eb;
  text-decoration: underline;
}

.prose :deep(code) {
  background: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
