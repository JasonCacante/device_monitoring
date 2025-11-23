from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app.routers import auth, dashboard, equipment, users

app = FastAPI(
    title="Device Monitoring API",
    description="Equipment management system with role-based authentication",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Device Monitoring API", "version": "1.0.0", "docs": "/docs"}


# Include routers
app.include_router(auth.router)
app.include_router(equipment.router)
app.include_router(dashboard.router)
app.include_router(users.router)
