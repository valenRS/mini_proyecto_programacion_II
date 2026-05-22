# =============================================================================
#  ventana_resumen.py
#  Rifa Navideña — Programación II · Universidad Tecnológica de Pereira
#
#  Ventana de resumen estadístico: muestra el porcentaje de boletas vendidas,
#  el dinero recaudado y el dinero pendiente por cobrar.
# =============================================================================

import tkinter as tk
from tkinter import ttk

from configuracion import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_DORADO,
    COLOR_TEXTO_CLARO, COLOR_FORMULARIO, COLOR_TEXTO_FORM,
    COLOR_BOTON_SEC, COLOR_EXITO, COLOR_ADVERTENCIA,
    FUENTE_NORMAL, FUENTE_LABEL, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_PEQUEÑA, FUENTE_GRANDE,
    TOTAL_BOLETAS,
)
from manejador_datos import ManejadorDatos


class VentanaResumen:
    """
    Ventana de resumen estadístico de la rifa.

    Calcula y presenta tres indicadores clave:
      1. Porcentaje de boletas vendidas (con barra de progreso).
      2. Total de dinero recibido hasta el momento.
      3. Total de dinero que aún está pendiente de cobro.

    También muestra una tabla con todas las compras registradas.
    """

    def __init__(self, raiz: tk.Tk):
        self.raiz      = raiz
        self.manejador = ManejadorDatos()

        self.raiz.title("Rifa Navideña · Resumen de ventas")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.resizable(True, True)
        self.raiz.minsize(760, 580)

        self._configurar_estilos_ttk()

        # Calcular todo antes de construir la interfaz
        self._datos = self._calcular_estadisticas()

        self._crear_interfaz()
        self._centrar_ventana()

    # ------------------------------------------------------------------ #
    #  Cálculo de estadísticas                                            #
    # ------------------------------------------------------------------ #

    def _calcular_estadisticas(self) -> dict:
        """
        Lee el CSV y retorna un diccionario con los tres indicadores
        requeridos por las instrucciones del proyecto.
        """
        compras          = self.manejador.leer_todas_las_compras()
        numeros_vendidos = self.manejador.obtener_numeros_vendidos()

        total_vendidas = len(numeros_vendidos)
        porcentaje     = (total_vendidas / TOTAL_BOLETAS * 100) if TOTAL_BOLETAS > 0 else 0.0

        dinero_recibido  = 0
        dinero_pendiente = 0

        for compra in compras:
            try:
                valor_pagado  = int(compra.get("valor_pagado",  0))
                total_a_pagar = int(compra.get("total_a_pagar", 0))
            except (ValueError, TypeError):
                valor_pagado  = 0
                total_a_pagar = 0

            dinero_recibido += valor_pagado

            # Solo cuenta como pendiente si el pago no está completo
            if compra.get("pago_completo") == "No":
                dinero_pendiente += total_a_pagar - valor_pagado

        return {
            "total_vendidas":    total_vendidas,
            "porcentaje":        porcentaje,
            "dinero_recibido":   dinero_recibido,
            "dinero_pendiente":  dinero_pendiente,
            "total_compradores": len(compras),
            "compras":           compras,
        }

    # ------------------------------------------------------------------ #
    #  Utilidades generales                                               #
    # ------------------------------------------------------------------ #

    def _centrar_ventana(self):
        self.raiz.update_idletasks()
        w = self.raiz.winfo_width()
        h = self.raiz.winfo_height()
        x = (self.raiz.winfo_screenwidth()  - w) // 2
        y = (self.raiz.winfo_screenheight() - h) // 2
        self.raiz.geometry(f"{w}x{h}+{x}+{y}")

    def _configurar_estilos_ttk(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=COLOR_FORMULARIO,
            foreground=COLOR_TEXTO_FORM,
            fieldbackground=COLOR_FORMULARIO,
            rowheight=26,
            font=FUENTE_NORMAL,
            borderwidth=0,
        )
        estilo.configure(
            "Treeview.Heading",
            background=COLOR_PANEL,
            foreground=COLOR_DORADO,
            font=FUENTE_LABEL,
            relief="flat",
            padding=(6, 6),
        )
        estilo.map(
            "Treeview",
            background=[("selected", COLOR_ACENTO)],
            foreground=[("selected", "white")],
        )
        estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    # ------------------------------------------------------------------ #
    #  Construcción de la interfaz                                        #
    # ------------------------------------------------------------------ #

    def _crear_interfaz(self):
        self._crear_encabezado()
        self._crear_tarjetas()
        self._crear_barra_progreso()
        self._crear_barra_botones()   # Se empaca primero para quedar siempre visible
        self._crear_tabla_compras()   # Se empaca después para expandirse en el espacio restante

    def _crear_encabezado(self):
        marco = tk.Frame(self.raiz, bg="#0D1B2A", pady=14)
        marco.pack(fill="x")

        tk.Label(
            marco,
            text="📊  RESUMEN DE LA RIFA",
            font=FUENTE_TITULO,
            bg="#0D1B2A",
            fg="white",
        ).pack()

        tk.Label(
            marco,
            text="Estado actual de ventas y recaudo",
            font=FUENTE_PEQUEÑA,
            bg="#0D1B2A",
            fg="#7090B0",
        ).pack()

    def _crear_tarjetas(self):
        """
        Tres tarjetas visuales, una por cada indicador.
        Cada una tiene una franja de color en la parte superior
        para distinguirlas de un vistazo.
        """
        marco_tarjetas = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=16, pady=14)
        marco_tarjetas.pack(fill="x")
        marco_tarjetas.columnconfigure((0, 1, 2), weight=1, uniform="tarjeta")

        datos = [
            {
                "color":    COLOR_ACENTO,
                "icono":    "🎟",
                "titulo":   "BOLETAS VENDIDAS",
                "valor":    f"{self._datos['porcentaje']:.1f}%",
                "detalle":  f"{self._datos['total_vendidas']} de {TOTAL_BOLETAS}",
            },
            {
                "color":    COLOR_EXITO,
                "icono":    "💵",
                "titulo":   "DINERO RECIBIDO",
                "valor":    f"${self._datos['dinero_recibido']:,}",
                "detalle":  "recaudado hasta ahora",
            },
            {
                "color":    COLOR_ADVERTENCIA,
                "icono":    "⏳",
                "titulo":   "PENDIENTE POR COBRAR",
                "valor":    f"${self._datos['dinero_pendiente']:,}",
                "detalle":  "aún no ha sido pagado",
            },
        ]

        for columna, info in enumerate(datos):
            self._crear_tarjeta(marco_tarjetas, info, columna)

    def _crear_tarjeta(self, padre, info: dict, columna: int):
        """Construye una sola tarjeta de estadística."""
        # Marco exterior con borde del color de la tarjeta
        marco_ext = tk.Frame(padre, bg=info["color"], padx=2, pady=2)
        marco_ext.grid(row=0, column=columna, sticky="nsew", padx=6)

        # Marco interior oscuro
        marco_int = tk.Frame(marco_ext, bg=COLOR_PANEL, padx=18, pady=16)
        marco_int.pack(fill="both", expand=True)

        # Franja de color en la parte superior
        tk.Frame(marco_int, bg=info["color"], height=4).pack(fill="x", pady=(0, 12))

        # Ícono y título
        tk.Label(
            marco_int,
            text=f"{info['icono']}  {info['titulo']}",
            font=FUENTE_PEQUEÑA,
            bg=COLOR_PANEL, fg=info["color"],
        ).pack(anchor="w")

        # Valor grande
        tk.Label(
            marco_int,
            text=info["valor"],
            font=FUENTE_GRANDE,
            bg=COLOR_PANEL, fg="white",
        ).pack(anchor="w", pady=(6, 2))

        # Detalle
        tk.Label(
            marco_int,
            text=info["detalle"],
            font=FUENTE_PEQUEÑA,
            bg=COLOR_PANEL, fg="#888899",
        ).pack(anchor="w")

    def _crear_barra_progreso(self):
        """Barra visual que representa el porcentaje de boletas vendidas."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=22)
        marco.pack(fill="x", pady=(0, 6))

        # Encabezado de la barra
        marco_enc = tk.Frame(marco, bg=COLOR_FONDO)
        marco_enc.pack(fill="x", pady=(0, 6))

        tk.Label(
            marco_enc,
            text="Progreso de ventas",
            font=FUENTE_LABEL,
            bg=COLOR_FONDO, fg=COLOR_TEXTO_CLARO,
        ).pack(side="left")

        tk.Label(
            marco_enc,
            text=f"{self._datos['total_compradores']} comprador(es) registrado(s)",
            font=FUENTE_PEQUEÑA,
            bg=COLOR_FONDO, fg="#666688",
        ).pack(side="right")

        # Contenedor de la barra (fondo oscuro)
        barra_fondo = tk.Frame(marco, bg="#2A2A4A", height=22)
        barra_fondo.pack(fill="x")
        barra_fondo.pack_propagate(False)

        # Relleno proporcional al porcentaje
        porcentaje = max(0.0, min(100.0, self._datos["porcentaje"]))

        if porcentaje > 0:
            relleno = tk.Frame(barra_fondo, bg=COLOR_ACENTO, height=22)
            relleno.place(relwidth=porcentaje / 100, relheight=1.0)

        # Etiqueta encima de la barra
        if porcentaje > 0:
            tk.Label(
                barra_fondo,
                text=f"  {porcentaje:.1f}%",
                font=FUENTE_PEQUEÑA,
                bg=COLOR_ACENTO if porcentaje >= 10 else "#2A2A4A",
                fg="white",
            ).place(x=4, y=3)

    def _crear_tabla_compras(self):
        """Tabla con el historial completo de compras registradas."""
        marco = tk.LabelFrame(
            self.raiz,
            text="  Historial de compras  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=14,
            pady=10,
        )
        marco.pack(fill="both", expand=True, padx=16, pady=(8, 6))
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        columnas = ("nombre", "fecha", "boletas", "total", "pagado", "estado")

        tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="none",
        )

        encabezados = {
            "nombre":  ("Comprador",     170),
            "fecha":   ("Fecha",         155),
            "boletas": ("Nros. boletas", 120),
            "total":   ("Total",          90),
            "pagado":  ("Pagado",         90),
            "estado":  ("Estado",         80),
        }
        for col, (titulo, ancho) in encabezados.items():
            tabla.heading(col, text=titulo, anchor="w")
            tabla.column(col, width=ancho, minwidth=50, anchor="w")

        scroll_v = tk.Scrollbar(marco, orient="vertical",   command=tabla.yview)
        scroll_h = tk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")

        # Llenar la tabla
        compras = self._datos["compras"]

        if not compras:
            tk.Label(
                marco,
                text="No hay compras registradas aún.",
                font=FUENTE_NORMAL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            ).grid(row=0, column=0)
            return

        tabla.tag_configure("par",   background="#F0F4F8")
        tabla.tag_configure("impar", background=COLOR_FORMULARIO)
        tabla.tag_configure("pend",  foreground=COLOR_ADVERTENCIA)

        for i, compra in enumerate(compras):
            try:
                total  = int(compra.get("total_a_pagar", 0))
                pagado = int(compra.get("valor_pagado",  0))
            except (ValueError, TypeError):
                total  = 0
                pagado = 0

            estado  = "Completo" if compra.get("pago_completo") == "Si" else "Parcial"
            boletas = compra.get("numeros_boletas", "").replace("-", " · #")

            tag = "par" if i % 2 == 0 else "impar"
            tags = (tag, "pend") if estado == "Parcial" else (tag,)

            tabla.insert(
                "",
                "end",
                values=(
                    compra.get("nombre", ""),
                    compra.get("fecha", ""),
                    f"#{boletas}",
                    f"${total:,}",
                    f"${pagado:,}",
                    estado,
                ),
                tags=tags,
            )

    def _crear_barra_botones(self):
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=16, pady=10)
        marco.pack(fill="x", side="bottom")

        tk.Button(
            marco,
            text="← Volver al registro",
            command=self._volver,
            font=FUENTE_NORMAL,
            bg=COLOR_BOTON_SEC, fg=COLOR_TEXTO_CLARO,
            activebackground="#1A4A80", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=18, pady=10, bd=0,
        ).pack(side="left")

    # ------------------------------------------------------------------ #
    #  Navegación entre ventanas                                          #
    # ------------------------------------------------------------------ #

    def _volver(self):
        """Cierra esta ventana y regresa al registro principal."""
        from ventana_registro import VentanaRegistro
        self.raiz.destroy()
        nueva_raiz = tk.Tk()
        VentanaRegistro(nueva_raiz)
        nueva_raiz.mainloop()
