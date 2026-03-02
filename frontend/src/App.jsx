import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import LeaveRequest from './pages/LeaveRequest'
import LeaveHistory from './pages/LeaveHistory'
import Approvals from './pages/Approvals'
import Balances from './pages/Balances'

function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <p className="text-slate-500">Loading...</p>
      </div>
    )
  }
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="request" element={<LeaveRequest />} />
        <Route path="history" element={<LeaveHistory />} />
        <Route
          path="approvals"
          element={
            <ProtectedRoute roles={['manager', 'admin']}>
              <Approvals />
            </ProtectedRoute>
          }
        />
        <Route path="balances" element={<Balances />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
