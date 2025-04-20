# main.py

from fastapi import FastAPI
from routes import vuelos
from db.database import crear_tablas
from db.models import Vuelo

app = FastAPI()
app.include_router(vuelos.router)

# Crear tablas al iniciar (solo si aún no existen)
crear_tablas()
