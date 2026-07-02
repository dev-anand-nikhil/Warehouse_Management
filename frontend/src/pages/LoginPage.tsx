import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

function base64UrlDecode(input: string) {
  const padded = input.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((input.length + 3) % 4)
  return atob(padded)
}

function parseJwt(token: string) {
  try {
    const payload = token.split('.')[1]
    const decoded = base64UrlDecode(payload)
    return JSON.parse(decoded)
  } catch {
    return null
  }
}

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('hub_user')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [isRegister, setIsRegister] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    setMessage('')

    if (isRegister) {
      try {
        await api.post('/auth/register', { username, password, role })
        const loginResponse = await api.post('/auth/login', { username, password })
        const token = loginResponse.data.access_token
        const payload = parseJwt(token)
        if (payload?.role !== role) {
          setError('Role mismatch during registration')
          return
        }
        login(token)
        navigate('/')
      } catch (err) {
        setError('Registration failed')
      }
      return
    }

    try {
      const response = await api.post('/auth/login', { username, password })
      const token = response.data.access_token
      const payload = parseJwt(token)
      if (payload?.role !== role) {
        setError('Invalid role for this user')
        return
      }
      login(token)
      navigate('/')
    } catch (err) {
      setError('Login failed')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-6">
        <div className="mb-5 flex items-center justify-between gap-3">
          <h1 className="text-2xl font-semibold text-slate-900">FreshTrack</h1>
          <button
            type="button"
            onClick={() => {
              setIsRegister((current) => !current)
              setError('')
              setMessage('')
            }}
            className="rounded border border-slate-200 bg-slate-50 px-3 py-1 text-sm text-slate-700 hover:bg-slate-100"
          >
            {isRegister ? 'Switch to Login' : 'Create account'}
          </button>
        </div>
        <h2 className="mb-5 text-xl font-medium text-slate-800">{isRegister ? 'Register' : 'Sign in'}</h2>
        <div className="space-y-4">
          <label className="block">
            <span className="text-sm font-medium">Username</span>
            <input value={username} onChange={(event) => setUsername(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <label className="block">
            <span className="text-sm font-medium">Password</span>
            <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <div className="space-y-3">
            <span className="text-sm font-medium">Sign in as</span>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setRole('hub_user')}
                className={`rounded border px-3 py-2 text-sm ${role === 'hub_user' ? 'bg-slate-800 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'}`}
              >
                Hub User
              </button>
              <button
                type="button"
                onClick={() => setRole('central_admin')}
                className={`rounded border px-3 py-2 text-sm ${role === 'central_admin' ? 'bg-slate-800 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'}`}
              >
                Admin
              </button>
            </div>
          </div>
          {isRegister && (
            <label className="block">
              <span className="text-sm font-medium">Role</span>
              <select value={role} onChange={(event) => setRole(event.target.value)} className="mt-1 w-full rounded border px-3 py-2">
                <option value="hub_user">Hub User</option>
                <option value="central_admin">Central Admin</option>
              </select>
            </label>
          )}
          {error && <p className="text-sm text-red-600">{error}</p>}
          {message && <p className="text-sm text-slate-600">{message}</p>}
        </div>
        <button type="submit" className="mt-6 w-full rounded bg-slate-800 px-4 py-2 text-white">
          {isRegister ? 'Register and Sign in' : 'Sign in'}
        </button>
      </form>
    </div>
  )
}
