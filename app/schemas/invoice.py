from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.models.invoice import InvoiceStatus

class InvoiceItemCreate(BaseModel):
    item_sku: str
    item_name: str
    expected_quantity: int = Field(gt=0)

class InvoiceItemRead(InvoiceItemCreate):
    id: int
    received_quantity: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class InvoiceCreate(BaseModel):
    invoice_id: str
    vendor_name: str
    warehouse_id: int
    items: List[InvoiceItemCreate]

class InvoiceUploadRequest(BaseModel):
    data: str
    warehouse_id: int | None = None

class InvoiceRead(BaseModel):
    id: int
    invoice_id: str
    vendor_name: str
    warehouse_id: int
    status: InvoiceStatus
    created_at: datetime
    items: List[InvoiceItemRead]

    model_config = {
        "from_attributes": True,
    }
