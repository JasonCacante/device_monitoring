from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_equipments = db.query(models.Equipment).count()
    active_equipments = db.query(models.Equipment).filter(models.Equipment.status == models.EquipmentStatus.ACTIVE).count()
    inactive_equipments = db.query(models.Equipment).filter(models.Equipment.status == models.EquipmentStatus.INACTIVE).count()
    maintenance_equipments = db.query(models.Equipment).filter(models.Equipment.status == models.EquipmentStatus.MAINTENANCE).count()

    # Mock percentage changes
    total_equipments_change = 5.2
    active_equipments_change = 2.8
    inactive_equipments_change = -1.1
    maintenance_equipments_change = 1.0

    return schemas.DashboardStats(
        total_equipments=total_equipments,
        active_equipments=active_equipments,
        inactive_equipments=inactive_equipments,
        maintenance_equipments=maintenance_equipments,
        total_equipments_change=total_equipments_change,
        active_equipments_change=active_equipments_change,
        inactive_equipments_change=inactive_equipments_change,
        maintenance_equipments_change=maintenance_equipments_change,
    )

@router.get("/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    status_counts = db.query(models.Equipment.status, func.count(models.Equipment.status)).group_by(models.Equipment.status).all()
    
    # Initialize counts
    active_count = 0
    inactive_count = 0
    maintenance_count = 0

    for status, count in status_counts:
        if status == models.EquipmentStatus.ACTIVE:
            active_count = count
        elif status == models.EquipmentStatus.INACTIVE:
            inactive_count = count
        elif status == models.EquipmentStatus.MAINTENANCE:
            maintenance_count = count
            
    return {
        "active": active_count,
        "inactive": inactive_count,
        "maintenance": maintenance_count,
    }
