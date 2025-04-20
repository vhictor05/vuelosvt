# db/models.py

from sqlalchemy import Column, Integer, String, Enum
from db.database import Base
import enum

class PrioridadEnum(str, enum.Enum):
    programado = "Programado"
    emergencia = "Emergencia"
    retrasado = "Retrasado"

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    prioridad = Column(Enum(PrioridadEnum), nullable=False)
