from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import csv
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceItemCreate, InvoiceUploadRequest
from app.services.warehouse_service import WarehouseService
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.warehouse_repository import WarehouseRepository
from app.core.security import require_role
from app.models.user import UserRole
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_csv(csv_data: str, default_warehouse_id: int | None = None) -> list[InvoiceCreate]:
    if not csv_data.strip():
        raise HTTPException(status_code=400, detail="Invoice data must not be empty")

    lines = [line for line in csv_data.strip().splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Invoice data must not be empty")

    default_fieldnames = [
        "Invoice_ID",
        "Vendor_Name",
        "Warehouse_ID",
        "Item_SKU",
        "Item_Name",
        "Expected_Quantity",
    ]

    first_row_fields = [field.strip().lower() for field in lines[0].split(",")]
    has_header = set(first_row_fields) >= {"invoice_id", "vendor_name", "item_sku", "item_name", "expected_quantity"}

    reader = csv.DictReader(lines, fieldnames=None if has_header else default_fieldnames)
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    invoices = {}
    for row in reader:
        invoice_id = row.get("Invoice_ID")
        warehouse_id_value = row.get("Warehouse_ID")
        if not invoice_id:
            raise HTTPException(status_code=400, detail="Missing required invoice ID")
        if default_warehouse_id is not None:
            warehouse_id = default_warehouse_id
        else:
            warehouse_id = int(warehouse_id_value) if warehouse_id_value else None
        if warehouse_id is None:
            raise HTTPException(status_code=400, detail="Missing required warehouse ID")
        key = invoice_id
        if key not in invoices:
            invoices[key] = {
                "invoice_id": invoice_id,
                "vendor_name": row.get("Vendor_Name", ""),
                "warehouse_id": warehouse_id,
                "items": [],
            }
        else:
            existing_warehouse_id = invoices[key]["warehouse_id"]
            if existing_warehouse_id != warehouse_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Conflicting warehouse_id for invoice {invoice_id}: {existing_warehouse_id} vs {warehouse_id}",
                )
        invoices[key]["items"].append(
            {
                "item_sku": row.get("Item_SKU", ""),
                "item_name": row.get("Item_Name", ""),
                "expected_quantity": int(row.get("Expected_Quantity", 0)),
            }
        )

    if not invoices:
        raise HTTPException(status_code=400, detail="No invoice rows found in CSV data")

    return [InvoiceCreate(**invoice) for invoice in invoices.values()]


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_invoices(
    payload: InvoiceUploadRequest,
    current_user = Depends(require_role(UserRole.central_admin.value)),
    db: Session = Depends(get_db),
):
    invoices = parse_csv(payload.data, payload.warehouse_id)
    warehouse_repo = WarehouseRepository(db)
    invoice_repo = InvoiceRepository(db)
    results = []
    for invoice_in in invoices:
        warehouse = warehouse_repo.get(invoice_in.warehouse_id)
        if not warehouse:
            raise HTTPException(status_code=400, detail=f"Unknown warehouse {invoice_in.warehouse_id}")
        if invoice_repo.get_by_invoice_id(invoice_in.invoice_id):
            raise HTTPException(status_code=400, detail=f"Duplicate invoice {invoice_in.invoice_id}")
        if any(item.expected_quantity <= 0 for item in invoice_in.items):
            raise HTTPException(status_code=400, detail="Expected quantity must be greater than 0")
        invoice = invoice_repo.create(
            invoice_in.invoice_id,
            invoice_in.vendor_name,
            invoice_in.warehouse_id,
            [item.model_dump() for item in invoice_in.items],
        )
        results.append(invoice)
    return {"inserted": len(results)}


@router.get("/warehouse/{warehouse_id}", response_model=list[InvoiceRead])
def list_invoices_for_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = WarehouseService(db).get_warehouse(warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return InvoiceRepository(db).list_by_warehouse(warehouse_id)
