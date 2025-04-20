# routes/vuelos.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Vuelo, PrioridadEnum
from tda.tda_lista_doble import ListaVuelos

router = APIRouter()
lista_vuelos = ListaVuelos()

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@router.post("/vuelos/")
def crear_vuelo(codigo: str, origen: str, destino: str, prioridad: PrioridadEnum, db: Session = Depends(get_db)):
    if db.query(Vuelo).filter(Vuelo.codigo == codigo).first():
        raise HTTPException(status_code=400, detail="El vuelo ya existe.")

    vuelo = Vuelo(codigo=codigo, origen=origen, destino=destino, prioridad=prioridad)
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)

    # Insertamos en la lista
    if prioridad == PrioridadEnum.emergencia:
        lista_vuelos.insertar_al_frente(vuelo)
    elif prioridad == PrioridadEnum.programado:
        lista_vuelos.insertar_al_final(vuelo)
    else:  # retrasado
        pos = lista_vuelos.longitud() // 2
        lista_vuelos.insertar_en_posicion(vuelo, pos)

    return vuelo


@router.get("/vuelos/primero")
def obtener_primero():
    vuelo = lista_vuelos.obtener_primero()
    if vuelo:
        return vuelo
    raise HTTPException(status_code=404, detail="Lista vacía")


@router.get("/vuelos/ultimo")
def obtener_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo:
        return vuelo
    raise HTTPException(status_code=404, detail="Lista vacía")


@router.delete("/vuelos/{pos}")
def eliminar_vuelo(pos: int):
    try:
        vuelo = lista_vuelos.extraer_de_posicion(pos)
        return vuelo
    except IndexError:
        raise HTTPException(status_code=404, detail="Posición inválida")

@router.get("/vuelos/longitud")
def obtener_longitud():
    return {"longitud": lista_vuelos.longitud()}

@router.post("/vuelos/posicion/{pos}")
def insertar_en_posicion(
    pos: int,
    codigo: str,
    origen: str,
    destino: str,
    prioridad: PrioridadEnum,
    db: Session = Depends(get_db)
):
    if pos < 0 or pos > lista_vuelos.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida.")

    if db.query(Vuelo).filter(Vuelo.codigo == codigo).first():
        raise HTTPException(status_code=400, detail="El vuelo ya existe.")

    vuelo = Vuelo(codigo=codigo, origen=origen, destino=destino, prioridad=prioridad)
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)

    lista_vuelos.insertar_en_posicion(vuelo, pos)

    return vuelo

@router.get("/vuelos/")
def listar_vuelos_en_orden():
    vuelos = []
    actual = lista_vuelos.cabeza
    while actual:
        vuelos.append({
            "id": actual.vuelo.id,
            "codigo": actual.vuelo.codigo,
            "origen": actual.vuelo.origen,
            "destino": actual.vuelo.destino,
            "prioridad": actual.vuelo.prioridad
        })
        actual = actual.siguiente
    return vuelos

