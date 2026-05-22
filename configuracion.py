# =============================================================================
#  configuracion.py
#  Rifa Navideña — Programación II · Universidad Tecnológica de Pereira
#
#  Aquí se definen todos los valores que controlan el comportamiento general
#  de la aplicación: precio, cantidad de boletas, colores y fuentes.
#  Si necesitas ajustar algo visual o numérico, este es el único lugar
#  donde debes hacer el cambio.
# =============================================================================

# -----------------------------------------------------------------------------
# Parámetros de la rifa
# -----------------------------------------------------------------------------

PRECIO_BOLETA = 5_000          # Valor de cada boleta en pesos colombianos
TOTAL_BOLETAS = 100            # Total de boletas disponibles en la rifa

ARCHIVO_CSV = "rifa_datos.csv" # Archivo donde se almacenan los registros


# -----------------------------------------------------------------------------
# Paleta de colores de la interfaz
# -----------------------------------------------------------------------------

COLOR_FONDO          = "#1A1A2E"  # Fondo principal de todas las ventanas
COLOR_PANEL          = "#16213E"  # Fondo de los paneles y secciones internas
COLOR_ACENTO         = "#E94560"  # Color destacado (botón principal, bordes activos)
COLOR_DORADO         = "#F5A623"  # Detalles, resaltes y encabezados
COLOR_TEXTO_CLARO    = "#EAEAEA"  # Texto sobre fondos oscuros
COLOR_FORMULARIO     = "#FFFFFF"  # Fondo de los campos de entrada
COLOR_TEXTO_FORM     = "#2C2C2C"  # Texto dentro de los campos de entrada
COLOR_BOTON_PPAL     = "#E94560"  # Fondo del botón de acción principal
COLOR_BOTON_SEC      = "#0F3460"  # Fondo de los botones secundarios
COLOR_EXITO          = "#27AE60"  # Verde para mensajes de confirmación
COLOR_ADVERTENCIA    = "#E67E22"  # Naranja para advertencias


# -----------------------------------------------------------------------------
# Tipografía
# -----------------------------------------------------------------------------

FUENTE_NORMAL      = ("Helvetica", 10)
FUENTE_LABEL       = ("Helvetica", 10, "bold")
FUENTE_TITULO      = ("Helvetica", 15, "bold")
FUENTE_SUBTITULO   = ("Helvetica", 11, "bold")
FUENTE_PEQUEÑA     = ("Helvetica", 9)
FUENTE_GRANDE      = ("Helvetica", 20, "bold")
