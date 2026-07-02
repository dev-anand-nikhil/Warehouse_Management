import { useState, useEffect } from 'react'
import api from '../services/api'
import { useAuth } from '../hooks/useAuth'

type Warehouse = {
  id: number
  warehouse_name: string
  location: string
}

export default function InvoiceUploadPage() {
  const { role } = useAuth()
  const [invoiceData, setInvoiceData] = useState('')
  const [message, setMessage] = useState('')
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [warehouseId, setWarehouseId] = useState<number | ''>('')

  const fetchWarehouses = async () => {
    try {
      const response = await api.get<Warehouse[]>('/warehouses')
      setWarehouses(response.data)
    } catch {
      setMessage('Could not load warehouses')
    }
  }

  useEffect(() => {
    fetchWarehouses()
  }, [])

  const upload = async () => {
    if (!invoiceData.trim()) {
      setMessage('Please paste invoice CSV text')
      return
    }

    try {
      await api.post('/invoices/upload', {
        data: invoiceData,
        warehouse_id: warehouseId || null,
      })
      setMessage('Upload successful')
    } catch (error: any) {
      const detail = error?.response?.data?.detail || 'Upload failed'
      setMessage(detail)
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Invoice Upload</h1>
      <div className="mt-5 rounded-xl border border-slate-200 bg-white p-5">
        {role !== 'central_admin' ? (
          <p className="text-sm text-slate-600">Only Central Admin users can upload master invoices.</p>
        ) : (
          <>
            <label className="block">
              <span className="text-sm font-medium">Target Warehouse (optional)</span>
              <select
                value={warehouseId}
                onChange={(event) => setWarehouseId(event.target.value ? Number(event.target.value) : '')}
                className="mt-1 w-full rounded border px-3 py-2"
              >
                <option value="">Use Warehouse_ID from CSV</option>
                {warehouses.map((warehouse) => (
                  <option key={warehouse.id} value={warehouse.id}>
                    {warehouse.warehouse_name} — {warehouse.location}
                  </option>
                ))}
              </select>
            </label>
            <p className="mt-3 text-sm text-slate-500">If a warehouse is selected, it will be applied to all uploaded invoice rows.</p>
            <label className="block mt-4">
              <span className="text-sm font-medium">Invoice CSV Text</span>
              <textarea
                value={invoiceData}
                onChange={(event) => setInvoiceData(event.target.value)}
                rows={10}
                className="mt-1 w-full rounded border px-3 py-2"
                placeholder="Invoice_ID,Vendor_Name,Warehouse_ID,Item_SKU,Item_Name,Expected_Quantity\nINV-1001,Acme Corp,2,SKU-001,Widget A,10"
              />
            </label>
            <p className="mt-2 text-sm text-slate-500">Header row is optional; you can also paste rows directly without the first header line.</p>
            <button onClick={upload} className="mt-4 rounded bg-slate-800 px-4 py-2 text-white">Upload</button>
            {message && <p className="mt-4 text-sm text-slate-600">{message}</p>}
          </>
        )}
      </div>
    </div>
  )
}
