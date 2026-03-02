import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const nav = [
    { to: '/', label: 'Dashboard' },
    { to: '/request', label: 'Request Leave' },
    { to: '/history', label: 'My Requests' },
    { to: '/balances', label: 'My Balances' },
    ...(user?.role === 'manager' || user?.role === 'admin' ? [{ to: '/approvals', label: 'Approvals' }] : []),
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-slate-800 text-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="font-semibold text-lg">Leave Management</h1>
          <nav className="flex items-center gap-6">
            {nav.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `text-sm font-medium ${isActive ? 'text-amber-400' : 'text-slate-300 hover:text-white'}`
                }
              >
                {label}
              </NavLink>
            ))}
            <span className="text-slate-400 text-sm">{user?.full_name}</span>
            <button
              type="button"
              onClick={handleLogout}
              className="text-sm text-slate-400 hover:text-white"
            >
              Logout
            </button>
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
