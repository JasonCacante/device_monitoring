import asyncio
from datetime import datetime

from app.database import SessionLocal, engine
from app.models import Equipment, EquipmentStatus, Maintenance, User, UserRole
from sqlalchemy.orm import Session


async def seed():
    db: Session = SessionLocal()
    try:
        print("Seeding database...")

        # Clear existing data (in correct order due to foreign keys)
        db.query(Maintenance).delete()
        db.query(Equipment).delete()
        db.query(User).delete()
        db.commit()

        print("Creating users...")
        # Create users
        users_data = [
            {
                "email": "admin@example.com",
                "name": "John Admin",
                "role": UserRole.ADMIN,
                "avatar_url": "https://randomuser.me/api/portraits/men/1.jpg",
            },
            {
                "email": "staff@example.com",
                "name": "Ana Staff",
                "role": UserRole.STAFF,
                "avatar_url": "https://randomuser.me/api/portraits/women/2.jpg",
            },
            {
                "email": "customer@example.com",
                "name": "Carlos Customer",
                "role": UserRole.CUSTOMER,
                "avatar_url": "https://randomuser.me/api/portraits/men/3.jpg",
            },
        ]

        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            created_users.append(user)

        db.commit()

        # Refresh to get IDs
        for user in created_users:
            db.refresh(user)

        admin_user = created_users[0]
        staff_user = created_users[1]
        customer_user = created_users[2]

        print(
            f"Created users: Admin({admin_user.id}), Staff({staff_user.id}), Customer({customer_user.id})"
        )

        print("Creating equipments...")
        # Create equipments with assignments
        equipments_data = [
            {
                "name": "Laptop A",
                "serial": "SN-LAP-A001",
                "status": EquipmentStatus.ACTIVE,
                "location": "Oficina 101",
                "image_url": "/uploads/laptop_a.jpg",
                "type": "Laptop",
                "assigned_to_id": staff_user.id,
            },
            {
                "name": "Laptop B",
                "serial": "SN-LAP-B002",
                "status": EquipmentStatus.ACTIVE,
                "location": "Oficina 102",
                "image_url": "/uploads/laptop_b.jpg",
                "type": "Laptop",
                "customer_id": customer_user.id,
            },
            {
                "name": "Servidor A",
                "serial": "SN-SRV-A001",
                "status": EquipmentStatus.MAINTENANCE,
                "location": "Data Center",
                "image_url": "/uploads/server_a.jpg",
                "type": "Servidor",
                "assigned_to_id": staff_user.id,
            },
            {
                "name": "Impresora A",
                "serial": "SN-PRT-A001",
                "status": EquipmentStatus.INACTIVE,
                "location": "Recepción",
                "image_url": "/uploads/printer_a.jpg",
                "type": "Impresora",
            },
            {
                "name": "Proyector A",
                "serial": "SN-PRO-A001",
                "status": EquipmentStatus.ACTIVE,
                "location": "Sala de Reuniones 1",
                "image_url": "/uploads/projector_a.jpg",
                "type": "Proyector",
                "customer_id": customer_user.id,
            },
        ]

        created_equipments = []
        for eq_data in equipments_data:
            equipment = Equipment(**eq_data)
            db.add(equipment)
            created_equipments.append(equipment)

        db.commit()

        # Refresh objects to get their IDs
        for equipment in created_equipments:
            db.refresh(equipment)

        # Map equipment names to their IDs
        equipment_id_map = {eq.name: eq.id for eq in created_equipments}

        print(f"Created {len(created_equipments)} equipments")

        print("Creating maintenances...")
        # Add new maintenances
        maintenances_data = [
            {
                "equipment_id": equipment_id_map["Servidor A"],
                "description": "Actualización de software y parches de seguridad",
                "technician": "Juan Pérez",
            },
            {
                "equipment_id": equipment_id_map["Impresora A"],
                "description": "Cambio de tóner y limpieza general",
                "technician": "Ana Gómez",
            },
            {
                "equipment_id": equipment_id_map["Laptop A"],
                "description": "Mantenimiento preventivo",
                "technician": "Carlos Tech",
            },
        ]

        for maint_data in maintenances_data:
            maintenance = Maintenance(**maint_data, date=datetime.utcnow())
            db.add(maintenance)

        db.commit()

        print("\n" + "=" * 60)
        print("✅ Database seeded successfully!")
        print("=" * 60)
        print("\n📧 Test Users Created:")
        print(f"   Admin:    {admin_user.email} (role: {admin_user.role.value})")
        print(f"   Staff:    {staff_user.email} (role: {staff_user.role.value})")
        print(f"   Customer: {customer_user.email} (role: {customer_user.role.value})")
        print("\n📦 Equipment Summary:")
        print(f"   Total: {len(created_equipments)}")
        print(f"   Assigned to Staff: 2")
        print(f"   Owned by Customer: 2")
        print(f"   Unassigned: 1")
        print("\n🔧 Maintenance Records: {len(maintenances_data)}")
        print("=" * 60 + "\n")

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(seed())
