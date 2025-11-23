import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/equipos",
    tags=["equipos"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Equipment)
def create_equipment(
    equipment: schemas.EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(models.UserRole.ADMIN)),
):
    """Create equipment (Admin only)"""
    db_equipment = models.Equipment(
        name=equipment.name,
        serial=equipment.serial,
        status=equipment.status,
        location=equipment.location,
        image_url=equipment.image_url,
        type=equipment.type,
    )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.get("/", response_model=List[schemas.Equipment])
def read_equipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Get equipment list filtered by user role:
    - Admin: All equipment
    - Staff: Only equipment assigned to them
    - Customer: Only equipment they own
    """
    query = db.query(models.Equipment)

    if current_user.role == models.UserRole.STAFF:
        # Staff only sees equipment assigned to them
        query = query.filter(models.Equipment.assigned_to_id == current_user.id)
    elif current_user.role == models.UserRole.CUSTOMER:
        # Customers only see equipment they own
        query = query.filter(models.Equipment.customer_id == current_user.id)
    # Admin sees everything (no filter)

    equipments = query.offset(skip).limit(limit).all()
    return equipments


@router.get("/{equipment_id}", response_model=schemas.Equipment)
def read_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get equipment details with role-based access control"""
    equipment = (
        db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    )
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    # Check access permissions
    if current_user.role == models.UserRole.STAFF:
        if equipment.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Access denied: Equipment not assigned to you"
            )
    elif current_user.role == models.UserRole.CUSTOMER:
        if equipment.customer_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Access denied: Equipment not owned by you"
            )
    # Admin can access everything

    return equipment


@router.patch("/{equipment_id}", response_model=schemas.Equipment)
def update_equipment(
    equipment_id: int,
    equipment_update: schemas.EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(models.UserRole.ADMIN)),
):
    """Update equipment (Admin only)"""
    db_equipment = (
        db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    )
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    update_data = equipment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_equipment, key, value)

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(models.UserRole.ADMIN)),
):
    """Delete equipment (Admin only)"""
    db_equipment = (
        db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    )
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db.delete(db_equipment)
    db.commit()
    return {"ok": True}


@router.post("/{equipment_id}/maintenances/", response_model=schemas.Maintenance)
def create_maintenance_for_equipment(
    equipment_id: int,
    maintenance: schemas.MaintenanceCreate,
    db: Session = Depends(get_db),
):
    db_equipment = (
        db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    )
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db_maintenance = models.Maintenance(
        **maintenance.model_dump(), equipment_id=equipment_id
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.post("/{equipment_id}/upload-image", response_model=schemas.Equipment)
async def upload_equipment_image(
    equipment_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    db_equipment = (
        db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    )
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    # Define the path to save the image
    upload_dir = "api/uploads"  # Relative to the project root
    os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
    file_location = os.path.join(upload_dir, file.filename)

    # Save the uploaded file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the image_url in the database
    db_equipment.image_url = f"/uploads/{file.filename}"  # URL path for the frontend
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return db_equipment
