#!/usr/bin/env python3
"""
=============================================================================
 main.py  —  Punto de entrada de la aplicación
 Rifa Navideña · Premio: Ancheta navideña

 Universidad Tecnológica de Pereira
 Programa de Ingeniería Electrónica
 Asignatura: Programación II
 Docente: MSc. Yurley Tatiana Tovar Martínez

 Integrantes:
 - Kevin Sebastian Parra Gómez
 - Valentina Rodríguez Sepúlveda.

 Descripción:
     Aplicación de escritorio desarrollada con Tkinter para gestionar
     la venta de boletas de una rifa. Permite registrar compradores,
     actualizar pagos y consultar el resumen de ventas. Toda la
     información se almacena de forma persistente en un archivo CSV.

 Uso:
     python main.py

 Módulos del proyecto:
     main.py                → este archivo (punto de entrada)
     configuracion.py       → constantes: precio, colores, fuentes
     manejador_datos.py     → lectura y escritura del archivo CSV
     ventana_registro.py    → ventana principal de registro
     ventana_actualizacion.py → ventana para actualizar pagos
     ventana_resumen.py     → ventana con estadísticas de la rifa
=============================================================================
"""

import tkinter as tk

from ventana_registro import VentanaRegistro


if __name__ == "__main__":
    raiz = tk.Tk()
    VentanaRegistro(raiz)
    raiz.mainloop()
