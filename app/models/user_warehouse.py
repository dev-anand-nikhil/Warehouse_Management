from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserWarehouse(Base):
    __tablename__ = "user_warehouses"
    __table_args__ = (UniqueConstraint("user_id", "warehouse_id", name="uq_user_warehouse"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("User", back_populates="warehouse_assignments")
    warehouse = relationship("Warehouse", back_populates="assignments")
