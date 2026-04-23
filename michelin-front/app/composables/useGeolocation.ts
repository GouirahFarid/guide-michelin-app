/**
 * Composable for browser geolocation with caching
 *
 * Silently requests user location on first access and caches
 * coordinates in localStorage with a 10-minute TTL.
 */

export interface Coords {
  latitude: number
  longitude: number
}

export interface GeolocationState {
  coords: Coords | null
  loading: boolean
}

const CACHE_KEY = 'user_location_cache'
const CACHE_TTL = 10 * 60 * 1000 // 10 minutes in milliseconds

interface CachedLocation {
  coords: Coords
  timestamp: number
}

/**
 * Get cached location from localStorage
 */
function getCachedLocation(): Coords | null {
  if (typeof window === 'undefined') return null

  try {
    const cached = localStorage.getItem(CACHE_KEY)
    if (!cached) return null

    const parsed: CachedLocation = JSON.parse(cached)
    const now = Date.now()

    // Check if cache is still valid
    if (now - parsed.timestamp < CACHE_TTL) {
      return parsed.coords
    }

    // Cache expired, remove it
    localStorage.removeItem(CACHE_KEY)
    return null
  } catch {
    return null
  }
}

/**
 * Save location to localStorage
 */
function cacheLocation(coords: Coords): void {
  if (typeof window === 'undefined') return

  try {
    const cached: CachedLocation = {
      coords,
      timestamp: Date.now()
    }
    localStorage.setItem(CACHE_KEY, JSON.stringify(cached))
  } catch (e) {
    console.warn('[useGeolocation] Failed to cache location:', e)
  }
}

/**
 * Request current position from browser
 */
function requestPosition(): Promise<Coords> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation not supported'))
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const coords: Coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
        resolve(coords)
      },
      (error) => {
        reject(error)
      },
      {
        enableHighAccuracy: false,
        timeout: 10000,
        maximumAge: 5 * 60 * 1000 // 5 minutes
      }
    )
  })
}

/**
 * Composable for geolocation
 *
 * Automatically gets user location on first call with caching.
 * No custom UI - browser shows native permission prompt.
 */
export function useGeolocation() {
  const state = ref<GeolocationState>({
    coords: null,
    loading: false
  })

  let initPromise: Promise<Coords | null> | null = null

  /**
   * Initialize location (called once on first access)
   */
  async function init(): Promise<Coords | null> {
    console.log('[useGeolocation] init() called')

    // Check cache first
    const cached = getCachedLocation()
    if (cached) {
      console.log('[useGeolocation] Using cached location:', cached)
      state.value.coords = cached
      return cached
    }

    console.log('[useGeolocation] No cache, requesting location...')

    // Already initializing
    if (initPromise) {
      return initPromise
    }

    state.value.loading = true

    initPromise = requestPosition()
      .then((coords) => {
        console.log('[useGeolocation] Location obtained:', coords)
        state.value.coords = coords
        cacheLocation(coords)
        return coords
      })
      .catch((error) => {
        // Silently fail - user can still use app without location
        console.log('[useGeolocation] Location failed:', error.message, 'code:', error.code)
        if (error.code !== 1) { // Not permission denied
          console.warn('[useGeolocation] Failed to get location:', error.message)
        }
        return null
      })
      .finally(() => {
        state.value.loading = false
        initPromise = null
      })

    return initPromise
  }

  // Auto-initialize on client-side
  if (typeof window !== 'undefined') {
    console.log('[useGeolocation] Auto-initializing on client-side')
    init()
  }

  return {
    state: readonly(state),
    init
  }
}
