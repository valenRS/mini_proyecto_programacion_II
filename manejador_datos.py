# =============================================================================
#  manejador_datos.py
#  Rifa Navideña — Programación II · Universidad Tecnológica de Pereira
#
#  Esta clase se encarga de TODA la comunicación con el archivo CSV.
#  Las ventanas nunca tocan el archivo directamente; siempre piden los datos
#  a través de esta clase. Así, si en el futuro cambia el formato de
#  almacenamiento, solo hay que modificar este archivo.
# =============================================================================

import csv
import os

from configuracion import ARCHIVO_CSV, TOTAL_BOLETAS


# Nombres exactos de las columnas del archivo CSV (el orden importa)
COLUMNAS = [
    "nombre",
    "telefono",
    "correo",
    "fecha",
    "cantidad_boletas",
    "numeros_boletas",   # Números separados por guión, ej: "3-7-42"
    "valor_pagado",
    "pago_completo",     # "Si" o "No"
    "total_a_pagar",
]


class ManejadorDatos:
    """
    Gestiona la lectura y escritura del archivo CSV de la rifa.

    Uso básico:
        manejador = ManejadorDatos()
        manejador.guardar_compra(datos_del_comprador)
        todas = manejador.leer_todas_las_compras()
    """

    def __init__(self, ruta_archivo=ARCHIVO_CSV):
        self.ruta_archivo = ruta_archivo
        self._crear_archivo_si_no_existe()

    # ------------------------------------------------------------------
    # Métodos privados (uso interno de la clase)
    # ------------------------------------------------------------------

    def _crear_archivo_si_no_existe(self):
        """Crea el archivo CSV con encabezados si todavía no existe."""
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
                escritor.writeheader()

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def guardar_compra(self, datos_compra: dict):
        """
        Agrega una nueva fila al CSV con los datos del comprador.
        Nunca borra ni sobreescribe registros anteriores.

        Parámetros:
            datos_compra: diccionario con las claves definidas en COLUMNAS.
        """
        with open(self.ruta_archivo, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
            escritor.writerow(datos_compra)

    def leer_todas_las_compras(self) -> list:
        """
        Lee el archivo CSV y retorna una lista de diccionarios,
        uno por cada compra registrada.

        Retorna lista vacía si no hay registros.
        """
        if not os.path.exists(self.ruta_archivo):
            return []

        with open(self.ruta_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)

    def actualizar_compra(self, indice: int, nuevo_valor_pagado: str, nuevo_estado_pago: str):
        """
        Modifica el valor pagado y el estado de pago de una compra existente.
        Identifica la fila por su posición (índice) en el CSV.

        Parámetros:
            indice:              Posición de la fila (0 = primera compra).
            nuevo_valor_pagado:  Nuevo monto pagado como cadena de texto.
            nuevo_estado_pago:   "Si" si ya pagó completo, "No" si es parcial.
        """
        todas_las_compras = self.leer_todas_las_compras()

        if indice < 0 or indice >= len(todas_las_compras):
            raise IndexError(f"No existe una compra en la posición {indice}.")

        todas_las_compras[indice]["valor_pagado"] = nuevo_valor_pagado
        todas_las_compras[indice]["pago_completo"] = nuevo_estado_pago

        # Reescribimos el archivo completo con los datos actualizados
        with open(self.ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
            escritor.writeheader()
            escritor.writerows(todas_las_compras)

    def obtener_numeros_vendidos(self) -> set:
        """
        Retorna un conjunto (set) con todos los números de boleta
        que ya fueron vendidos, sin importar a quién.
        """
        compras = self.leer_todas_las_compras()
        numeros_vendidos = set()

        for compra in compras:
            texto_numeros = compra.get("numeros_boletas", "").strip()
            if texto_numeros:
                for numero in texto_numeros.split("-"):
                    if numero.isdigit():
                        numeros_vendidos.add(int(numero))

        return numeros_vendidos

    def boletas_disponibles(self) -> list:
        """
        Retorna la lista de números de boleta que aún no han sido vendidos,
        ordenados de menor a mayor.
        """
        numeros_vendidos = self.obtener_numeros_vendidos()
        return [n for n in range(1, TOTAL_BOLETAS + 1) if n not in numeros_vendidos]
