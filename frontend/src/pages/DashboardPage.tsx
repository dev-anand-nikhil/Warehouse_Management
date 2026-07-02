import { Link } from 'react-router-dom'

export default function DashboardPage() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-semibold">Dashboard</h1>
      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <Link to="/upload" className="rounded-xl border border-slate-200 bg-white p-5 text-slate-900 transition hover:border-slate-300 hover:bg-slate-50">
          <h2 className="text-xl font-semibold">Invoice Upload</h2>
          <p className="mt-2 text-sm text-slate-600">Upload CSV invoices directly to the warehouse system.</p>
        </Link>
        <Link to="/warehouses" className="rounded-xl border border-slate-200 bg-white p-5 text-slate-900 transition hover:border-slate-300 hover:bg-slate-50">
          <h2 className="text-xl font-semibold">Warehouse Management</h2>
          <p className="mt-2 text-sm text-slate-600">Create, view, and delete warehouse records.</p>
        </Link>
        <Link to="/reports" className="rounded-xl border border-slate-200 bg-white p-5 text-slate-900 transition hover:border-slate-300 hover:bg-slate-50">
          <h2 className="text-xl font-semibold">Reports</h2>
          <p className="mt-2 text-sm text-slate-600">Generate reconciliation reports for inbound invoices.</p>
        </Link>
      </div>
    </div>
  )
}
