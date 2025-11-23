import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class EquipmentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    avatar_url = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    otp_code = Column(String(6), nullable=True)
    otp_expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assigned_equipments = relationship(
        "Equipment",
        foreign_keys="Equipment.assigned_to_id",
        back_populates="assigned_to",
    )
    owned_equipments = relationship(
        "Equipment", foreign_keys="Equipment.customer_id", back_populates="customer"
    )


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    serial = Column(String, unique=True, index=True)
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.ACTIVE)
    location = Column(String)
    image_url = Column(String, nullable=True)
    type = Column(String, nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    maintenances = relationship("Maintenance", back_populates="equipment")
    assigned_to = relationship(
        "User", foreign_keys=[assigned_to_id], back_populates="assigned_equipments"
    )
    customer = relationship(
        "User", foreign_keys=[customer_id], back_populates="owned_equipments"
    )


class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipments.id"))
    description = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())
    technician = Column(String)

    equipment = relationship("Equipment", back_populates="maintenances")
