import { useState, useEffect } from 'react'
import api from '../services/api'

type Warehouse = {
  id: number
  warehouse_name: string
  location: string
}

type Invoice = {
  id: number
  invoice_id: string
  vendor_name: string
  status: string
  created_at: string
}

export default function InvoiceListPage() {
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [warehouseId, setWarehouseId] = useState<number | ''>('')
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [message, setMessage] = useState('')

  const fetchWarehouses = async () => {
    try {
      const response = await api.get<Warehouse[]>('/warehouses')
      setWarehouses(response.data)
    } catch {
      setMessage('Could not load warehouses')
    }
  }

  const fetchInvoices = async (selectedWarehouseId: number | '') => {
    if (!selectedWarehouseId) {
      setInvoices([])
      return
    }

    try {
      const response = await api.get<Invoice[]>(`/invoices/warehouse/${selectedWarehouseId}`)
      setInvoices(response.data)
      setMessage('')
    } catch {
      setInvoices([])
      setMessage('Could not load invoices for this warehouse')
    }
  }

  useEffect(() => {
    fetchWarehouses()
  }, [])

  useEffect(() => {
    fetchInvoices(warehouseId)
  }, [warehouseId])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Invoice List</h1>
      <div className="mt-5 rounded-xl border border-slate-200 bg-white p-5">
        <label className="block">
          <span className="text-sm font-medium">Warehouse</span>
          <select
            value={warehouseId}
            onChange={(event) => setWarehouseId(event.target.value ? Number(event.target.value) : '')}
            className="mt-1 w-full rounded border px-3 py-2"
          >
            <option value="">Select warehouse</option>
            {warehouses.map((warehouse) => (
              <option key={warehouse.id} value={warehouse.id}>
                {warehouse.warehouse_name} — {warehouse.location}
              </option>
            ))}
          </select>
        </label>
        {message && <p className="mt-4 text-sm text-red-600">{message}</p>}
        <div className="mt-6 space-y-4">
          {invoices.length === 0 ? (
            <p className="text-sm text-slate-600">No invoices to display.</p>
          ) : (
            invoices.map((invoice) => (
              <div key={invoice.id} className="rounded-lg border p-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="font-semibold">Invoice {invoice.invoice_id}</p>
                    <p className="text-sm text-slate-500">Vendor: {invoice.vendor_name}</p>
                  </div>
                  <div className="text-sm text-slate-700">Status: {invoice.status}</div>
                </div>
                <p className="mt-2 text-sm text-slate-500">Created: {new Date(invoice.created_at).toLocaleString()}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
