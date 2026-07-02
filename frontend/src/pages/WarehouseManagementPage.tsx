import { useState, useEffect } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

type Warehouse = {
  id: number
  warehouse_name: string
  location: string
}

export default function WarehouseManagementPage() {
  const { role } = useAuth()
  const [name, setName] = useState('')
  const [location, setLocation] = useState('')
  const [message, setMessage] = useState('')
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])

  const fetchWarehouses = async () => {
    try {
      const response = await api.get<Warehouse[]>('/warehouses')
      setWarehouses(response.data)
    } catch {
      setMessage('Failed to load warehouses')
    }
  }

  useEffect(() => {
    fetchWarehouses()
  }, [])

  const createWarehouse = async () => {
    try {
      await api.post('/warehouses', { warehouse_name: name, location })
      setName('')
      setLocation('')
      setMessage('Warehouse created')
      fetchWarehouses()
    } catch {
      setMessage('Create failed')
    }
  }

  const deleteWarehouse = async (warehouseId: number) => {
    try {
      await api.delete(`/warehouses/${warehouseId}`)
      setMessage('Warehouse deleted')
      fetchWarehouses()
    } catch {
      setMessage('Delete failed')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Warehouse Management</h1>
      <div className="mt-5 grid gap-6 md:grid-cols-[1fr_2fr]">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="mb-4 text-xl font-semibold">Add Warehouse</h2>
          {role === 'central_admin' ? (
            <>
              <label className="block">
                <span className="text-sm font-medium">Name</span>
                <input value={name} onChange={(event) => setName(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
              </label>
              <label className="mt-4 block">
                <span className="text-sm font-medium">Location</span>
                <input value={location} onChange={(event) => setLocation(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
              </label>
              <button onClick={createWarehouse} className="mt-6 rounded bg-slate-800 px-4 py-2 text-white">
                Create Warehouse
              </button>
            </>
          ) : (
            <p className="text-sm text-slate-600">Only Central Admin users can create warehouses.</p>
          )}
          {message && <p className="mt-4 text-sm text-slate-600">{message}</p>}
        </div>
        <div className="rounded-xl bg-white p-6 shadow">
          <h2 className="mb-4 text-xl font-semibold">Warehouse List</h2>
          {warehouses.length === 0 ? (
            <p className="text-sm text-slate-600">No warehouses found.</p>
          ) : (
            <div className="space-y-3">
              {warehouses.map((warehouse) => (
                <div key={warehouse.id} className="flex items-center justify-between rounded border px-4 py-3">
                  <div>
                    <p className="font-semibold">{warehouse.warehouse_name}</p>
                    <p className="text-sm text-slate-500">{warehouse.location}</p>
                  </div>
                  {role === 'central_admin' ? (
                    <button onClick={() => deleteWarehouse(warehouse.id)} className="rounded border border-red-300 px-3 py-1 text-sm text-red-700 hover:bg-red-50">
                      Delete
                    </button>
                  ) : null}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
