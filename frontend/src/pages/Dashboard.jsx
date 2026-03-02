import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-slate-800 mb-2">Dashboard</h1>
      <p className="text-slate-600 mb-8">
        Welcome, {user?.full_name}. Use the menu to request leave, view balances, or approve requests.
      </p>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <a
          href="/request"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:border-amber-400 hover:shadow transition"
        >
          <h2 className="font-medium text-slate-800">Request Leave</h2>
          <p className="text-sm text-slate-500 mt-1">Submit a new leave request</p>
        </a>
        <a
          href="/history"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:border-amber-400 hover:shadow transition"
        >
          <h2 className="font-medium text-slate-800">My Requests</h2>
          <p className="text-sm text-slate-500 mt-1">View and track your leave requests</p>
        </a>
        <a
          href="/balances"
          className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:border-amber-400 hover:shadow transition"
        >
          <h2 className="font-medium text-slate-800">My Balances</h2>
          <p className="text-sm text-slate-500 mt-1">See leave balance by type</p>
        </a>
        {(user?.role === 'manager' || user?.role === 'admin') && (
          <a
            href="/approvals"
            className="block rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:border-amber-400 hover:shadow transition"
          >
            <h2 className="font-medium text-slate-800">Approvals</h2>
            <p className="text-sm text-slate-500 mt-1">Approve or reject pending requests</p>
          </a>
        )}
      </div>
    </div>
  )
}
