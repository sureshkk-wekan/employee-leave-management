import { createContext, useContext, useState, useCallback, useEffect } from 'react'

const AuthContext = createContext(null)

const TOKEN_KEY = 'leave_mgmt_token'
const API_BASE = import.meta.env.VITE_API_URL || '/api'

async function api(endpoint, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY)
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  }
  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers })
  if (res.status === 401) {
    localStorage.removeItem(TOKEN_KEY)
    try {
      const d = await res.json()
      if (d.detail && (d.detail.includes('expired') || d.detail.includes('Invalid')))
        sessionStorage.setItem('session_expired', '1')
    } catch { /* ignore */ }
    window.dispatchEvent(new Event('auth-logout'))
    throw new Error('Unauthorized')
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || res.statusText)
  }
  if (res.status === 204 || res.headers.get('content-length') === '0') return null
  return res.json()
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadUser = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const me = await api('/auth/me')
      setUser(me)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadUser()
    const onLogout = () => {
      setUser(null)
    }
    window.addEventListener('auth-logout', onLogout)
    return () => window.removeEventListener('auth-logout', onLogout)
  }, [loadUser])

  const login = useCallback(async (email, password) => {
    const data = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    }).then((r) => {
      if (!r.ok) return r.json().then((d) => Promise.reject(new Error(d.detail || 'Login failed')))
      return r.json()
    })
    // Store token in localStorage; loadUser() sets auth state — then redirect to app (e.g. dashboard)
    localStorage.setItem(TOKEN_KEY, data.access_token)
    await loadUser()
    return data
  }, [loadUser])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setUser(null)
  }, [])

  const value = { user, loading, login, logout, loadUser, api }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

export { api }
