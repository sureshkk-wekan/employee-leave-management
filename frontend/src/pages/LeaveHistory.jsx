import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'

const STATUS_COLOR = {
  pending: 'bg-amber-100 text-amber-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  cancelled: 'bg-slate-100 text-slate-600',
}

export default function LeaveHistory() {
  const { api } = useAuth()
  const [requests, setRequests] = useState([])
  const [leaveTypes, setLeaveTypes] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api('/leave-requests?my_only=true'),
      api('/leave-types').then((list) => Object.fromEntries(list.map((t) => [t.id, t.name]))),
    ])
      .then(([reqs, types]) => {
        setRequests(reqs)
        setLeaveTypes(types)
      })
      .catch(() => setError('Failed to load requests'))
      .finally(() => setLoading(false))
  }, [api])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error) return <p className="text-red-600">{error}</p>

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">My Leave Requests</h1>
      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Leave type</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Start</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">End</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-slate-600 uppercase">Reason</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {requests.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                  No leave requests yet.
                </td>
              </tr>
            ) : (
              requests.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 text-slate-800">{leaveTypes[r.leave_type_id] ?? r.leave_type_id}</td>
                  <td className="px-4 py-3 text-slate-700">{r.start_date}</td>
                  <td className="px-4 py-3 text-slate-700">{r.end_date}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_COLOR[r.status] || ''}`}>
                      {r.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600 text-sm">{r.reason || '—'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
