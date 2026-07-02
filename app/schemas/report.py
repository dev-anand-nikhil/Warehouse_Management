from datetime import date
from pydantic import BaseModel

class ReportFilter(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    warehouse_id: int | None = None
    vendor_name: str | None = None

class ReconciliationRow(BaseModel):
    invoice_id: str
    vendor_name: str
    warehouse_id: int
    sku: str
    item_name: str
    expected_quantity: int
    received_quantity: int
    variance: int

class ReconciliationReport(BaseModel):
    rows: list[ReconciliationRow]
    generated_at: date
