import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserRole(str, enum.Enum):
    central_admin = "central_admin"
    hub_user = "hub_user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    warehouse_assignments = relationship("UserWarehouse", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
