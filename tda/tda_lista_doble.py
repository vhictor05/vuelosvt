# tda_lista_doble.py

class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.siguiente = None
        self.anterior = None


class ListaVuelos:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.size = 0

    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.size += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion < 0 or posicion > self.size:
            raise IndexError("Posición fuera de rango")

        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.size:
            self.insertar_al_final(vuelo)
        else:
            nuevo = Nodo(vuelo)
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self.size += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.size:
            raise IndexError("Posición fuera de rango")

        if posicion == 0:
            vuelo = self.cabeza.vuelo
            self.cabeza = self.cabeza.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None
            self.size -= 1
            return vuelo

        elif posicion == self.size - 1:
            vuelo = self.cola.vuelo
            self.cola = self.cola.anterior
            if self.cola:
                self.cola.siguiente = None
            else:
                self.cabeza = None
            self.size -= 1
            return vuelo

        else:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            vuelo = actual.vuelo
            anterior = actual.anterior
            siguiente = actual.siguiente
            anterior.siguiente = siguiente
            siguiente.anterior = anterior
            self.size -= 1
            return vuelo
