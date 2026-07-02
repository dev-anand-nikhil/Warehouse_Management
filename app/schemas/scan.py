from pydantic import BaseModel, Field

class ScanRequest(BaseModel):
    invoice_id: str
    barcode: str

class ScanResponse(BaseModel):
    invoice_id: str
    sku: str
    received_quantity: int
    expected_quantity: int
    status: str
    remaining: int
    completion_percent: float

class AdjustmentRequest(BaseModel):
    invoice_id: str
    sku: str
    delta: int | None = None
    override_quantity: int | None = None
    reason: str
