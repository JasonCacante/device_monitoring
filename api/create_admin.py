"""
Script para crear el primer usuario administrador
Ejecutar con: python -m api.create_admin
"""

import sys

from app.database import SessionLocal, engine
from app.models import Base, User, UserRole
from sqlalchemy.orm import Session


def create_admin_user():
    """Crea el primer usuario administrador"""
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Verificar si ya existe un admin
        admin = db.query(User).filter(User.role == UserRole.ADMIN).first()

        if admin:
            print(f"\n✅ Ya existe un usuario administrador: {admin.email}")
            print(f"   Nombre: {admin.name}")
            print(f"   ID: {admin.id}")
            return

        # Solicitar datos del administrador
        print("\n" + "=" * 60)
        print("  CREAR USUARIO ADMINISTRADOR")
        print("=" * 60 + "\n")

        email = input("Email del administrador: ").strip()
        if not email:
            print("❌ Error: El email es obligatorio")
            return

        # Verificar si el email ya existe
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"❌ Error: Ya existe un usuario con el email {email}")
            return

        name = input("Nombre completo: ").strip()
        if not name:
            name = email.split("@")[0].title()

        avatar_url = input(
            "URL del avatar (opcional, presiona Enter para omitir): "
        ).strip()
        if not avatar_url:
            avatar_url = None

        # Crear el usuario administrador
        admin = User(email=email, name=name, role=UserRole.ADMIN, avatar_url=avatar_url)

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\n" + "=" * 60)
        print("  ✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\n  ID:     {admin.id}")
        print(f"  Email:  {admin.email}")
        print(f"  Nombre: {admin.name}")
        print(f"  Rol:    {admin.role.value}")
        print(f"\n" + "=" * 60)
        print("\n📧 Para iniciar sesión:")
        print(f"   1. Ve a http://localhost:5173/login")
        print(f"   2. Ingresa el email: {admin.email}")
        print(f"   3. Solicita un código OTP")
        print(f"   4. Revisa la consola del backend para obtener el código")
        print(f"   5. Ingresa el código para acceder\n")

    except Exception as e:
        print(f"\n❌ Error al crear el usuario: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
