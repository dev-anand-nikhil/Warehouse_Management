import { useState } from 'react'
import api from '../services/api'

type ScanResult = {
  invoice_id: string
  sku: string
  received_quantity: number
  expected_quantity: number
  status: string
  remaining: number
  completion_percent: number
}

export default function ScanPage() {
  const [invoiceId, setInvoiceId] = useState('')
  const [barcode, setBarcode] = useState('')
  const [message, setMessage] = useState('')
  const [result, setResult] = useState<ScanResult | null>(null)

  const scan = async () => {
    try {
      const response = await api.post<ScanResult>('/scan', { invoice_id: invoiceId, barcode })
      setResult(response.data)
      setMessage('Scan successful')
    } catch {
      setResult(null)
      setMessage('Scan failed')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Scan</h1>
      <div className="mt-5 rounded-xl border border-slate-200 bg-white p-5">
        <label className="block">
          <span className="text-sm font-medium">Invoice ID</span>
          <input value={invoiceId} onChange={(event) => setInvoiceId(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
        </label>
        <label className="mt-4 block">
          <span className="text-sm font-medium">Barcode</span>
          <input value={barcode} onChange={(event) => setBarcode(event.target.value)} className="mt-1 w-full rounded border px-3 py-2" />
        </label>
        <button onClick={scan} className="mt-4 rounded bg-slate-800 px-4 py-2 text-white">Scan</button>
        {message && <p className="mt-4 text-sm text-slate-600">{message}</p>}
        {result && (
          <div className="mt-4 rounded-xl border bg-slate-50 p-4 text-sm">
            <p><strong>Invoice:</strong> {result.invoice_id}</p>
            <p><strong>SKU:</strong> {result.sku}</p>
            <p><strong>Status:</strong> {result.status}</p>
            <p><strong>Received:</strong> {result.received_quantity}</p>
            <p><strong>Expected:</strong> {result.expected_quantity}</p>
            <p><strong>Remaining:</strong> {result.remaining}</p>
            <p><strong>Completion:</strong> {result.completion_percent.toFixed(1)}%</p>
          </div>
        )}
      </div>
    </div>
  )
}
