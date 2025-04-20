# db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./vuelos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def crear_tablas():
    from db.models import Vuelo  # Importación interna para evitar conflictos circulares
    Base.metadata.create_all(bind=engine)
