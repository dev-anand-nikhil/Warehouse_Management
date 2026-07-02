import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function NavBar() {
  const { logout } = useAuth()
  const token = localStorage.getItem('freshtrack_token')
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="flex flex-wrap items-center justify-between border-b border-slate-200 bg-transparent px-4 py-3">
      <div className="text-base font-medium text-slate-900">FreshTrack</div>
      <div className="flex flex-wrap items-center gap-3 text-sm text-slate-700">
        {token ? (
          <>
            <Link to="/" className="hover:text-slate-900">Dashboard</Link>
            <Link to="/upload" className="hover:text-slate-900">Upload</Link>
            <Link to="/warehouses" className="hover:text-slate-900">Warehouses</Link>
            <Link to="/invoices" className="hover:text-slate-900">Invoices</Link>
            <Link to="/scan" className="hover:text-slate-900">Scan</Link>
            <Link to="/reports" className="hover:text-slate-900">Reports</Link>
            <button onClick={handleLogout} className="rounded border border-slate-200 bg-white px-3 py-1 text-slate-700 hover:bg-slate-50">
              Logout
            </button>
          </>
        ) : (
          <Link to="/login" className="hover:text-slate-900">Login</Link>
        )}
      </div>
    </nav>
  )
}
