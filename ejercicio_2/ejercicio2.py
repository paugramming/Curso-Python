"""Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia (EcoTech Solutions)."""

import json
from pathlib import Path


class StockInvalidoError(Exception):
    """Se intenta asignar un stock inválido (negativo o no entero)."""


class DispositivoEcológico:
    """Clase base de los productos ecológicos del catálogo."""

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock  # pasa por el setter: valida desde el constructor

    # --- Encapsulamiento explícito del stock -------------------------------
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError(f"El stock debe ser un entero, se recibió: {valor!r}")
        if valor < 0:
            raise StockInvalidoError(f"El stock no puede ser negativo (recibido: {valor}).")
        self.__stock = valor

    # --- Polimorfismo --------------------------------------------------------
    def ficha_tecnica(self):
        return (
            f"Dispositivo: {self.nombre}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Stock: {self.stock} unidades"
        )

    def a_diccionario(self):
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


# Alias sin tilde por comodidad.
DispositivoEcologico = DispositivoEcológico


class PanelSolar(DispositivoEcológico):
    """Panel solar: agrega potencia y eficiencia."""

    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  # porcentaje, ej. 21.5

    def ficha_tecnica(self):
        return (
            "=== FICHA TÉCNICA - PANEL SOLAR ===\n"
            f"Modelo: {self.nombre}\n"
            f"Potencia: {self.potencia_w} W\n"
            f"Eficiencia: {self.eficiencia}%\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Disponibilidad: {self.stock} unidades"
        )

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos


class GestorInventario:
    """Gestiona la persistencia del catálogo."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return ruta_archivo


if __name__ == "__main__":
    dispositivos_validos = []

    # Producto válido
    panel = PanelSolar("SunMax 450", 285000.0, 12, potencia_w=450, eficiencia=21.8)
    dispositivos_validos.append(panel)
    print(panel.ficha_tecnica())
    print()

    # Producto base válido
    dispositivos_validos.append(DispositivoEcológico("Cargador solar portátil", 45000.0, 40))

    # Intento de stock inválido en la creación
    try:
        PanelSolar("Panel defectuoso", 100000.0, -5, potencia_w=300, eficiencia=18.0)
    except StockInvalidoError as error:
        print(f"[ERROR CONTROLADO] {error}")

    # Intento de stock inválido por asignación
    try:
        panel.stock = -1
    except StockInvalidoError as error:
        print(f"[ERROR CONTROLADO] {error}")
    print(f"Stock del panel sin cambios: {panel.stock}")

    ruta = Path(__file__).resolve().parent / "catalogo_ecotech.json"
    GestorInventario().guardar_catalogo_json(dispositivos_validos, ruta)
    print(f"\nCatálogo exportado correctamente a: {ruta.name}")
