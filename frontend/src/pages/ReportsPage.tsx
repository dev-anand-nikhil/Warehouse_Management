import { useState, useEffect } from 'react'
import api from '../services/api'

type Warehouse = {
  id: number
  warehouse_name: string
  location: string
}

type ReconciliationRow = {
  invoice_id: string
  vendor_name: string
  warehouse_id: number
  sku: string
  item_name: string
  expected_quantity: number
  received_quantity: number
  variance: number
}

type Report = {
  rows: ReconciliationRow[]
  generated_at: string
}

export default function ReportsPage() {
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [warehouseId, setWarehouseId] = useState<number | ''>('')
  const [vendorName, setVendorName] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [report, setReport] = useState<Report | null>(null)
  const [message, setMessage] = useState('')

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

  const generateReport = async () => {
    try {
      const payload: Record<string, unknown> = {}
      if (warehouseId) payload.warehouse_id = warehouseId
      if (vendorName) payload.vendor_name = vendorName
      if (dateFrom) payload.date_from = dateFrom
      if (dateTo) payload.date_to = dateTo

      const response = await api.post<Report>('/reports/reconciliation', payload)
      setReport(response.data)
      setMessage('')
    } catch {
      setReport(null)
      setMessage('Could not generate report')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Reports</h1>
      <div className="mt-5 rounded-xl border border-slate-200 bg-white p-5">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="block">
            <span className="text-sm font-medium">Warehouse</span>
            <select
              value={warehouseId}
              onChange={(event) => setWarehouseId(event.target.value ? Number(event.target.value) : '')}
              className="mt-1 w-full rounded border px-3 py-2"
            >
              <option value="">All warehouses</option>
              {warehouses.map((warehouse) => (
                <option key={warehouse.id} value={warehouse.id}>
                  {warehouse.warehouse_name} — {warehouse.location}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            <span className="text-sm font-medium">Vendor Name</span>
            <input value={vendorName} onChange={(event) => setVendorName(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <label className="block">
            <span className="text-sm font-medium">Date From</span>
            <input type="date" value={dateFrom} onChange={(event) => setDateFrom(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
          <label className="block">
            <span className="text-sm font-medium">Date To</span>
            <input type="date" value={dateTo} onChange={(event) => setDateTo(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
          </label>
        </div>
        <button onClick={generateReport} className="mt-6 rounded bg-slate-800 px-4 py-2 text-white">
          Generate Report
        </button>
        {message && <p className="mt-4 text-sm text-red-600">{message}</p>}
        {report && (
          <div className="mt-6 overflow-x-auto">
            <div className="mb-3 text-sm text-slate-500">Generated at: {new Date(report.generated_at).toLocaleString()}</div>
            <table className="min-w-full table-auto border-collapse text-left text-sm">
              <thead>
                <tr>
                  <th className="border-b px-3 py-2">Invoice</th>
                  <th className="border-b px-3 py-2">Vendor</th>
                  <th className="border-b px-3 py-2">Warehouse</th>
                  <th className="border-b px-3 py-2">SKU</th>
                  <th className="border-b px-3 py-2">Item</th>
                  <th className="border-b px-3 py-2">Expected</th>
                  <th className="border-b px-3 py-2">Received</th>
                  <th className="border-b px-3 py-2">Variance</th>
                </tr>
              </thead>
              <tbody>
                {report.rows.map((row, index) => (
                  <tr key={`${row.invoice_id}-${row.sku}-${index}`}>
                    <td className="border-b px-3 py-2">{row.invoice_id}</td>
                    <td className="border-b px-3 py-2">{row.vendor_name}</td>
                    <td className="border-b px-3 py-2">{row.warehouse_id}</td>
                    <td className="border-b px-3 py-2">{row.sku}</td>
                    <td className="border-b px-3 py-2">{row.item_name}</td>
                    <td className="border-b px-3 py-2">{row.expected_quantity}</td>
                    <td className="border-b px-3 py-2">{row.received_quantity}</td>
                    <td className="border-b px-3 py-2">{row.variance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
