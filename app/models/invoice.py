import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class InvoiceStatus(str, enum.Enum):
    pending = "PENDING"
    in_progress = "IN_PROGRESS"
    completed = "COMPLETED"
    over_received = "OVER_RECEIVED"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String(128), unique=True, nullable=False, index=True)
    vendor_name = Column(String(256), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    warehouse = relationship("Warehouse", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="invoice")
