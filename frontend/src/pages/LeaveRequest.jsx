import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LeaveRequest() {
  const { api } = useAuth()
  const navigate = useNavigate()
  const [leaveTypes, setLeaveTypes] = useState([])
  const [leaveTypeId, setLeaveTypeId] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [reason, setReason] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    api('/leave-types')
      .then(setLeaveTypes)
      .catch(() => setError('Failed to load leave types'))
  }, [api])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await api('/leave-requests', {
        method: 'POST',
        body: JSON.stringify({
          leave_type_id: Number(leaveTypeId),
          start_date: startDate,
          end_date: endDate,
          reason: reason || null,
        }),
      })
      navigate('/history')
    } catch (err) {
      setError(err.message || 'Failed to submit')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">Request Leave</h1>
      <form onSubmit={handleSubmit} className="max-w-md space-y-4">
        {error && (
          <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
        )}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Leave type</label>
          <select
            value={leaveTypeId}
            onChange={(e) => setLeaveTypeId(e.target.value)}
            required
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 focus:ring-2 focus:ring-amber-500"
          >
            <option value="">Select type</option>
            {leaveTypes.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} ({t.code})
              </option>
            ))}
          </select>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Start date</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-2 focus:ring-amber-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">End date</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-2 focus:ring-amber-500"
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Reason (optional)</label>
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            rows={3}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-2 focus:ring-amber-500"
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="rounded-lg bg-amber-600 text-white font-medium py-2 px-4 hover:bg-amber-700 disabled:opacity-50"
        >
          {submitting ? 'Submitting...' : 'Submit request'}
        </button>
      </form>
    </div>
  )
}
