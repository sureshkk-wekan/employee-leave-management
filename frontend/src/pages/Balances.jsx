import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'

export default function Balances() {
  const { api } = useAuth()
  const [balances, setBalances] = useState([])
  const [leaveTypes, setLeaveTypes] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api('/leave-balances'),
      api('/leave-types').then((list) => Object.fromEntries(list.map((t) => [t.id, t.name]))),
    ])
      .then(([bals, types]) => {
        setBalances(bals)
        setLeaveTypes(types)
      })
      .catch(() => setError('Failed to load balances'))
      .finally(() => setLoading(false))
  }, [api])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error) return <p className="text-red-600">{error}</p>

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">My Leave Balances</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {balances.length === 0 ? (
          <p className="text-slate-500">No balance records yet. Balances are created when you have leave types and entitlement.</p>
        ) : (
          balances.map((b) => (
            <div
              key={b.id}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <p className="text-sm font-medium text-slate-500">{leaveTypes[b.leave_type_id] ?? b.leave_type_id} • {b.year}</p>
              <p className="mt-2 text-2xl font-semibold text-slate-800">{b.remaining_days} days left</p>
              <p className="text-sm text-slate-600 mt-1">
                Entitlement: {b.entitlement_days} • Carried: {b.carried_over_days} • Used: {b.used_days}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
