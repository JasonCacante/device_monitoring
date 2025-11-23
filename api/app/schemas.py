import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class EquipmentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


class MaintenanceBase(BaseModel):
    description: str
    date: Optional[datetime] = None
    technician: str


class MaintenanceCreate(MaintenanceBase):
    pass


class Maintenance(MaintenanceBase):
    id: int
    equipment_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class EquipmentBase(BaseModel):
    name: str
    serial: str
    status: EquipmentStatus = EquipmentStatus.ACTIVE
    location: str
    image_url: Optional[str] = None
    type: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    serial: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    type: Optional[str] = None


class Equipment(EquipmentBase):
    id: int
    created_at: datetime
    image_url: Optional[str] = None
    type: Optional[str] = None
    maintenances: List[Maintenance] = []

    model_config = ConfigDict(from_attributes=True)


class DashboardStats(BaseModel):
    total_equipments: int
    active_equipments: int
    inactive_equipments: int
    maintenance_equipments: int
    total_equipments_change: float
    active_equipments_change: float
    inactive_equipments_change: float
    maintenance_equipments_change: float


# Auth Schemas
class OTPRequest(BaseModel):
    email: str


class OTPVerify(BaseModel):
    email: str
    otp_code: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None


# User Schemas
class UserBase(BaseModel):
    email: str
    name: str
    avatar_url: Optional[str] = None
    role: UserRole = UserRole.STAFF


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None


class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: User
