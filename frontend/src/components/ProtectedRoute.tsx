import { Navigate, useLocation } from 'react-router-dom'

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('freshtrack_token')
  const location = useLocation()

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return children
}
