import { useState, useEffect } from 'react'

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

export function useAuth() {
  const [token, setToken] = useState<string | null>(null)
  const [role, setRole] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('freshtrack_token')
    setToken(storedToken)
    if (storedToken) {
      const payload = parseJwt(storedToken)
      setRole(payload?.role ?? null)
    }
  }, [])

  const login = (accessToken: string) => {
    localStorage.setItem('freshtrack_token', accessToken)
    setToken(accessToken)
    const payload = parseJwt(accessToken)
    setRole(payload?.role ?? null)
  }

  const logout = () => {
    localStorage.removeItem('freshtrack_token')
    setToken(null)
    setRole(null)
  }

  return { token, role, login, logout }
}
