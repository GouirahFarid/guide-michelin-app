/**
 * Composable for SSE streaming chat with MichelinBot API
 *
 * Handles Server-Sent Events connection and event parsing
 * for real-time restaurant recommendations.
 */

export interface SSEEvent<T = unknown> {
  event: string
  data: T
}

// Union type for all possible SSE event data shapes
export type SSEEventData =
  | TokenEventData
  | ProgressEventData
  | StepEventData
  | QueryAnalysisData
  | LocationData
  | RestaurantCardData
  | DoneData
  | ErrorData

interface TokenEventData {
  content: string
}

interface ProgressEventData {
  step: string
  progress: number
  message: string
  details?: Record<string, unknown>
}

interface StepEventData {
  step: string
  message: string
}

interface ErrorData {
  error: string
  step?: string
}

export interface ChatStreamOptions {
  query: string
  session_id?: string
  user_lat?: number
  user_lon?: number
  onError?: (error: string) => void
  onProgress?: (step: string, progress: number, message: string) => void
  onStep?: (step: string, status: 'start' | 'complete', message: string) => void
  onToken?: (content: string) => void
  onQueryAnalysis?: (analysis: QueryAnalysisData) => void
  onLocationDetected?: (location: LocationData) => void
  onRestaurantCard?: (card: RestaurantCardData) => void
  onDone?: (data: DoneData) => void
}

export interface QueryAnalysisData {
  original_query: string
  detected_location?: string
  detected_cuisine?: string
  detected_award?: string
  detected_price?: string
  is_geo_query: boolean
  distance_constraint?: number
  needs_user_location: boolean
}

export interface LocationData {
  location: string
  latitude: number
  longitude: number
  source: 'user_provided' | 'query_extracted' | 'city_database'
}

export interface RestaurantCardData {
  id: number
  name: string
  award?: string
  cuisine?: string
  price?: string
  location: string
  distance_km?: number
  description?: string
  signature_dish?: string
  title?: string
  subtitle?: string
  badge_text?: string
  badge_color?: string
  url?: string
  website_url?: string
}

export interface DoneData {
  session_id: string
  response_length: number
  restaurants_count?: number
  query_analysis?: {
    detected_location?: string
    detected_cuisine?: string
    detected_award?: string
  }
}

export interface ProgressData {
  step: string
  progress: number
  message: string
  details?: any
}

export interface StepData {
  step: string
  message: string
}

/**
 * Composable for SSE chat streaming
 */
export function useChatStream() {
  const API_BASE = '/api' // Uses Vite proxy to backend

  /**
   * Stream chat responses from the MichelinBot API
   */
  const streamChat = async (options: ChatStreamOptions): Promise<void> => {
    const {
      query,
      session_id,
      user_lat,
      user_lon,
      onError,
      onProgress,
      onStep,
      onToken,
      onQueryAnalysis,
      onLocationDetected,
      onRestaurantCard,
      onDone
    } = options

    // Build URL with query parameters
    const params = new URLSearchParams({ query })
    if (session_id) params.append('session_id', session_id)
    if (user_lat !== undefined) params.append('user_lat', user_lat.toString())
    if (user_lon !== undefined) params.append('user_lon', user_lon.toString())

    const url = `${API_BASE}/chat/stream?${params.toString()}`

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'text/event-stream',
        },
      })

      if (!response.ok) {
        // Try to get error details from response
        let errorDetail = `HTTP error! status: ${response.status}`
        try {
          const errorData = await response.json()
          errorDetail = errorData.detail || errorData.error || errorDetail
        } catch {
          const text = await response.text()
          if (text) errorDetail = text
        }
        throw new Error(errorDetail)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('Response body is null')
      }

      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        // Decode and add to buffer
        buffer += decoder.decode(value, { stream: true })

        // Process complete SSE messages
        const lines = buffer.split('\n')
        buffer = lines.pop() || '' // Keep incomplete line in buffer

        for (const line of lines) {
          if (!line.trim()) continue

          if (line.startsWith('event: ')) {
            const eventType = line.substring(7).trim()
            // Event type stored, next line will be data
            continue
          }

          if (line.startsWith('data: ')) {
            const dataStr = line.substring(6).trim()
            let eventData: SSEEventData

            try {
              eventData = JSON.parse(dataStr) as SSEEventData
            } catch (e) {
              console.error('Failed to parse SSE data:', dataStr)
              continue
            }

            // Route event to appropriate handler
            handleSSEEvent(eventData, {
              onProgress,
              onStep,
              onToken,
              onQueryAnalysis,
              onLocationDetected,
              onRestaurantCard,
              onDone
            })
          }
        }
      }
    } catch (error) {
      console.error('[useChatStream] Error:', error)
      const errorMessage = error instanceof Error ? error.message : String(error)
      console.error('[useChatStream] Error message:', errorMessage)
      onError?.(errorMessage)
    }
  }

  /**
   * Handle individual SSE events
   */
  function handleSSEEvent(
    data: SSEEventData,
    handlers: {
      onProgress?: (step: string, progress: number, message: string) => void
      onStep?: (step: string, status: 'start' | 'complete', message: string) => void
      onToken?: (content: string) => void
      onQueryAnalysis?: (analysis: QueryAnalysisData) => void
      onLocationDetected?: (location: LocationData) => void
      onRestaurantCard?: (card: RestaurantCardData) => void
      onDone?: (data: DoneData) => void
    }
  ) {
    const { onProgress, onStep, onToken, onQueryAnalysis, onLocationDetected, onRestaurantCard, onDone } = handlers

    // Token event (streaming text)
    if (data.content !== undefined) {
      onToken?.(data.content)
      return
    }

    // Progress event
    if (data.step !== undefined && data.progress !== undefined) {
      onProgress?.(data.step, data.progress, data.message)
      return
    }

    // Step start event
    if (data.step !== undefined && data.message !== undefined && data.content === undefined) {
      onStep?.(data.step, 'start', data.message)
      return
    }

    // Query analysis event
    if (data.original_query !== undefined) {
      onQueryAnalysis?.(data as QueryAnalysisData)
      return
    }

    // Location detected event
    if (data.location !== undefined && data.latitude !== undefined) {
      onLocationDetected?.(data as LocationData)
      return
    }

    // Restaurant card event
    if (data.id !== undefined && data.name !== undefined) {
      onRestaurantCard?.(data as RestaurantCardData)
      return
    }

    // Done event
    if (data.session_id !== undefined && data.response_length !== undefined) {
      onDone?.(data as DoneData)
      return
    }

    // Step complete event (has step and message, no content)
    if (data.step !== undefined && data.message !== undefined) {
      onStep?.(data.step, 'complete', data.message)
      return
    }

    // Error event
    if (data.error !== undefined) {
      onStep?.('error', 'complete', data.error)
      return
    }
  }

  return {
    streamChat
  }
}
