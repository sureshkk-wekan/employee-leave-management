import { useState, useEffect } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { user, login } = useAuth()
  const navigate = useNavigate()

  // Redirect when user is set (must run before any early return to satisfy Rules of Hooks)
  useEffect(() => {
    if (user) navigate('/', { replace: true })
  }, [user, navigate])

  const sessionExpired = typeof sessionStorage !== 'undefined' && sessionStorage.getItem('session_expired')
  if (sessionExpired) sessionStorage.removeItem('session_expired')

  if (user) return <Navigate to="/" replace />

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(email, password)
      // Next tick so auth state is committed before ProtectedRoute runs
      setTimeout(() => navigate('/', { replace: true }), 0)
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
      <div className="w-full max-w-sm rounded-xl bg-white shadow-lg border border-slate-200 p-8">
        <h1 className="text-xl font-semibold text-slate-800 mb-6 text-center">
          Employee Leave Management
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {sessionExpired && (
            <p className="text-sm text-amber-700 bg-amber-50 rounded-lg px-3 py-2">Your session expired. Please log in again.</p>
          )}
          {error && (
            <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
          )}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            />
          </div>
          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-amber-600 text-white font-medium py-2 px-4 hover:bg-amber-700 disabled:opacity-50"
          >
            {submitting ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
        <div className="mt-4 text-xs text-slate-500 text-center space-y-1">
          <p className="font-medium text-slate-600">Demo — all roles use password: admin123</p>
          <p>Admin: admin@example.com</p>
          <p>Manager: manager@example.com</p>
          <p>Employee: employee@example.com</p>
        </div>
      </div>
    </div>
  )
}
