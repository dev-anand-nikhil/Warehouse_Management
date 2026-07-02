from sqlalchemy.orm import Session, joinedload
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_invoice_id(self, invoice_id: str) -> Invoice | None:
        return (
            self.db.query(Invoice)
            .options(joinedload(Invoice.items))
            .filter(Invoice.invoice_id == invoice_id)
            .first()
        )

    def create(self, invoice_id: str, vendor_name: str, warehouse_id: int, items: list[dict]) -> Invoice:
        invoice = Invoice(invoice_id=invoice_id, vendor_name=vendor_name, warehouse_id=warehouse_id)
        for item in items:
            invoice.items.append(
                InvoiceItem(
                    item_sku=item["item_sku"],
                    item_name=item["item_name"],
                    expected_quantity=item["expected_quantity"],
                )
            )
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def list_by_warehouse(self, warehouse_id: int) -> list[Invoice]:
        return self.db.query(Invoice).options(joinedload(Invoice.items)).filter(Invoice.warehouse_id == warehouse_id).all()
