# =============================================================================
#  ventana_actualizacion.py
#  Rifa Navideña — Programación II · Universidad Tecnológica de Pereira
#
#  Ventana para modificar el valor pagado y el estado de pago de una compra.
#  Muestra todos los registros en una tabla y permite editar el seleccionado.
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox

from configuracion import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_DORADO,
    COLOR_TEXTO_CLARO, COLOR_FORMULARIO, COLOR_TEXTO_FORM,
    COLOR_BOTON_PPAL, COLOR_BOTON_SEC, COLOR_EXITO, COLOR_ADVERTENCIA,
    FUENTE_NORMAL, FUENTE_LABEL, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_PEQUEÑA,
)
from manejador_datos import ManejadorDatos


class VentanaActualizacion:
    """
    Ventana de actualización de datos.

    Muestra una tabla con todos los compradores registrados.
    Al seleccionar una fila, se habilita un formulario para modificar
    únicamente el valor pagado y el estado del pago (completo/parcial).
    """

    def __init__(self, raiz: tk.Tk):
        self.raiz     = raiz
        self.manejador = ManejadorDatos()

        # Guarda el índice CSV y el total del registro que está siendo editado
        self._indice_seleccionado    = None
        self._total_del_seleccionado = 0

        self.raiz.title("Rifa Navideña · Actualización de datos")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.resizable(True, True)
        self.raiz.minsize(730, 520)

        self._configurar_estilos_ttk()
        self._crear_interfaz()
        self._cargar_registros()
        self._centrar_ventana()

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
        """Personaliza el aspecto del Treeview y los Combobox."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=COLOR_FORMULARIO,
            foreground=COLOR_TEXTO_FORM,
            fieldbackground=COLOR_FORMULARIO,
            rowheight=28,
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
        # Quitar el borde de focus del Treeview
        estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    def _crear_campo_entrada(self, padre, ancho=20):
        """Campo de texto con borde de color de acento."""
        contenedor = tk.Frame(padre, bg=COLOR_ACENTO, padx=1, pady=1)
        campo = tk.Entry(
            contenedor,
            font=FUENTE_NORMAL,
            bg=COLOR_FORMULARIO,
            fg=COLOR_TEXTO_FORM,
            relief="flat",
            bd=4,
            insertbackground=COLOR_ACENTO,
            width=ancho,
        )
        campo.pack(fill="x")
        return contenedor, campo

    # ------------------------------------------------------------------ #
    #  Construcción de la interfaz                                        #
    # ------------------------------------------------------------------ #

    def _crear_interfaz(self):
        self._crear_encabezado()
        self._crear_seccion_tabla()
        self._crear_seccion_edicion()
        self._crear_barra_botones()

    def _crear_encabezado(self):
        marco = tk.Frame(self.raiz, bg=COLOR_BOTON_SEC, pady=14)
        marco.pack(fill="x")

        tk.Label(
            marco,
            text="✎  ACTUALIZACIÓN DE DATOS",
            font=FUENTE_TITULO,
            bg=COLOR_BOTON_SEC,
            fg="white",
        ).pack()

        tk.Label(
            marco,
            text="Selecciona un registro de la tabla para modificar su información de pago",
            font=FUENTE_PEQUEÑA,
            bg=COLOR_BOTON_SEC,
            fg="#A8C8F0",
        ).pack()

    def _crear_seccion_tabla(self):
        """Tabla (Treeview) con todos los registros del CSV."""
        marco = tk.LabelFrame(
            self.raiz,
            text="  Registros guardados  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=14,
            pady=10,
        )
        marco.pack(fill="both", expand=True, padx=16, pady=(12, 6))
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        # ── Columnas de la tabla ──────────────────────────────────────────
        columnas = ("nombre", "boletas", "total", "pagado", "estado")

        self._tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        encabezados = {
            "nombre":  ("Comprador",      180),
            "boletas": ("Nros. boletas",  130),
            "total":   ("Total a pagar",  110),
            "pagado":  ("Valor pagado",   110),
            "estado":  ("Estado",          90),
        }
        for col, (titulo, ancho) in encabezados.items():
            self._tabla.heading(col, text=titulo, anchor="w")
            self._tabla.column(col, width=ancho, minwidth=60, anchor="w")

        # ── Scrollbars ────────────────────────────────────────────────────
        scroll_v = tk.Scrollbar(marco, orient="vertical",   command=self._tabla.yview)
        scroll_h = tk.Scrollbar(marco, orient="horizontal", command=self._tabla.xview)
        self._tabla.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)

        self._tabla.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")

        self._tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

        # Mensaje cuando no hay registros
        self._label_sin_datos = tk.Label(
            marco,
            text="Aún no hay compras registradas.",
            font=FUENTE_NORMAL,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_CLARO,
        )

    def _crear_seccion_edicion(self):
        """Formulario de edición: solo se pueden cambiar valor_pagado y pago_completo."""
        marco = tk.LabelFrame(
            self.raiz,
            text="  Editar registro seleccionado  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=16,
            pady=12,
        )
        marco.pack(fill="x", padx=16, pady=(0, 6))

        # ── Indicador del comprador seleccionado ─────────────────────────
        fila_indicador = tk.Frame(marco, bg=COLOR_PANEL)
        fila_indicador.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        tk.Label(
            fila_indicador,
            text="Comprador seleccionado:",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).pack(side="left")

        self._label_comprador = tk.Label(
            fila_indicador,
            text="← Haz clic en una fila de la tabla",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_ACENTO,
        )
        self._label_comprador.pack(side="left", padx=(10, 0))

        # ── Nuevo valor pagado ────────────────────────────────────────────
        tk.Label(
            marco, text="Nuevo valor pagado ($):",
            font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=1, column=0, sticky="w")

        contenedor_pago, self._entry_nuevo_valor = self._crear_campo_entrada(marco, ancho=18)
        contenedor_pago.grid(row=1, column=1, padx=(10, 40), ipady=2)

        # ── Nuevo estado de pago ──────────────────────────────────────────
        tk.Label(
            marco, text="Estado del pago:",
            font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=1, column=2, sticky="w", padx=(0, 10))

        self._var_pago_completo = tk.BooleanVar()
        self._var_pago_parcial  = tk.BooleanVar()

        tk.Checkbutton(
            marco,
            text=" Pago completo",
            variable=self._var_pago_completo,
            font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_EXITO,
            selectcolor=COLOR_FONDO,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_EXITO,
            command=self._al_marcar_completo,
        ).grid(row=1, column=3, padx=(0, 16))

        tk.Checkbutton(
            marco,
            text=" Pago parcial",
            variable=self._var_pago_parcial,
            font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_ADVERTENCIA,
            selectcolor=COLOR_FONDO,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_ADVERTENCIA,
            command=self._al_marcar_parcial,
        ).grid(row=1, column=4)

        # Desactivar el formulario hasta que se seleccione una fila
        self._entry_nuevo_valor.config(state="disabled")

    def _crear_barra_botones(self):
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=16, pady=10)
        marco.pack(fill="x")

        tk.Button(
            marco,
            text="✔  Guardar cambios",
            command=self._guardar_cambios,
            font=FUENTE_SUBTITULO,
            bg=COLOR_BOTON_PPAL, fg="white",
            activebackground="#C73652", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=22, pady=10, bd=0,
        ).pack(side="left", padx=(0, 14))

        tk.Button(
            marco,
            text="← Volver al registro",
            command=self._volver,
            font=FUENTE_NORMAL,
            bg=COLOR_BOTON_SEC, fg=COLOR_TEXTO_CLARO,
            activebackground="#1A4A80", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=16, pady=10, bd=0,
        ).pack(side="left")

    # ------------------------------------------------------------------ #
    #  Carga y actualización de la tabla                                  #
    # ------------------------------------------------------------------ #

    def _cargar_registros(self):
        """Lee el CSV y llena la tabla con todos los registros."""
        # Limpiar tabla
        for item in self._tabla.get_children():
            self._tabla.delete(item)

        compras = self.manejador.leer_todas_las_compras()

        if not compras:
            self._label_sin_datos.place(relx=0.5, rely=0.5, anchor="center")
            return

        self._label_sin_datos.place_forget()

        for indice, compra in enumerate(compras):
            total   = int(compra.get("total_a_pagar", 0))
            pagado  = int(compra.get("valor_pagado",  0))
            estado  = "Completo" if compra.get("pago_completo") == "Si" else "Parcial"
            boletas = compra.get("numeros_boletas", "").replace("-", " · #")

            self._tabla.insert(
                "",
                "end",
                iid=str(indice),   # El IID es el índice en el CSV
                values=(
                    compra.get("nombre", ""),
                    f"#{boletas}",
                    f"${total:,}",
                    f"${pagado:,}",
                    estado,
                ),
            )

        # Alternar color de filas para mejor legibilidad
        self._tabla.tag_configure("par",   background="#F0F4F8")
        self._tabla.tag_configure("impar", background=COLOR_FORMULARIO)
        for i, item in enumerate(self._tabla.get_children()):
            tag = "par" if i % 2 == 0 else "impar"
            self._tabla.item(item, tags=(tag,))

    # ------------------------------------------------------------------ #
    #  Lógica de la sección de edición                                    #
    # ------------------------------------------------------------------ #

    def _al_seleccionar_fila(self, evento=None):
        """Al hacer clic en una fila: carga los datos de ese registro en el formulario."""
        seleccion = self._tabla.selection()
        if not seleccion:
            return

        self._indice_seleccionado = int(seleccion[0])

        # Leer el registro completo del CSV
        compras = self.manejador.leer_todas_las_compras()
        compra  = compras[self._indice_seleccionado]

        nombre  = compra.get("nombre", "")
        pagado  = compra.get("valor_pagado", "0")
        estado  = compra.get("pago_completo", "No")

        self._total_del_seleccionado = int(compra.get("total_a_pagar", 0))

        # Mostrar el nombre del comprador seleccionado
        self._label_comprador.config(text=nombre, fg=COLOR_DORADO)

        # Habilitar y llenar el campo de valor pagado
        self._entry_nuevo_valor.config(state="normal")
        self._entry_nuevo_valor.delete(0, "end")
        self._entry_nuevo_valor.insert(0, pagado)

        # Reflejar el estado actual en los checkbuttons
        if estado == "Si":
            self._var_pago_completo.set(True)
            self._var_pago_parcial.set(False)
            self._entry_nuevo_valor.config(state="readonly")
        else:
            self._var_pago_completo.set(False)
            self._var_pago_parcial.set(True)
            self._entry_nuevo_valor.config(state="normal")

    def _al_marcar_completo(self):
        """Al marcar 'Pago completo': desactiva parcial y llena con el total del registro."""
        if self._var_pago_completo.get():
            self._var_pago_parcial.set(False)
            self._entry_nuevo_valor.config(state="normal")
            self._entry_nuevo_valor.delete(0, "end")
            self._entry_nuevo_valor.insert(0, str(self._total_del_seleccionado))
            self._entry_nuevo_valor.config(state="readonly")
        else:
            self._entry_nuevo_valor.config(state="normal")
            self._entry_nuevo_valor.delete(0, "end")

    def _al_marcar_parcial(self):
        """Al marcar 'Pago parcial': desactiva completo y habilita el campo."""
        if self._var_pago_parcial.get():
            self._var_pago_completo.set(False)
            self._entry_nuevo_valor.config(state="normal")
            self._entry_nuevo_valor.delete(0, "end")

    # ------------------------------------------------------------------ #
    #  Guardar cambios                                                    #
    # ------------------------------------------------------------------ #

    def _guardar_cambios(self):
        """Valida el formulario y actualiza el registro en el CSV."""

        # ── Verificar que haya un registro seleccionado ───────────────────
        if self._indice_seleccionado is None:
            messagebox.showwarning(
                "Sin selección",
                "Primero debes hacer clic en un registro de la tabla para editarlo.",
            )
            return

        # ── Verificar estado de pago ──────────────────────────────────────
        if not self._var_pago_completo.get() and not self._var_pago_parcial.get():
            messagebox.showwarning(
                "Campo requerido",
                "Indica si el pago es completo o parcial.",
            )
            return

        # ── Verificar y convertir el valor pagado ─────────────────────────
        valor_texto = self._entry_nuevo_valor.get().strip()
        if not valor_texto:
            messagebox.showwarning(
                "Campo requerido",
                "El campo de valor pagado no puede estar vacío.",
            )
            self._entry_nuevo_valor.focus()
            return

        try:
            nuevo_valor = int(valor_texto)
            if nuevo_valor < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Valor inválido",
                "El valor pagado debe ser un número entero positivo\n(sin puntos ni comas).",
            )
            return

        # ── Guardar en el CSV ─────────────────────────────────────────────
        nuevo_estado = "Si" if self._var_pago_completo.get() else "No"

        self.manejador.actualizar_compra(
            self._indice_seleccionado,
            str(nuevo_valor),
            nuevo_estado,
        )

        messagebox.showinfo(
            "Cambios guardados",
            f"El registro fue actualizado correctamente.\n\n"
            f"Nuevo valor pagado : ${nuevo_valor:,}\n"
            f"Estado del pago    : {'Completo' if nuevo_estado == 'Si' else 'Parcial'}",
        )

        # Refrescar la tabla y deseleccionar
        self._indice_seleccionado = None
        self._label_comprador.config(
            text="← Haz clic en una fila de la tabla", fg=COLOR_ACENTO,
        )
        self._entry_nuevo_valor.config(state="normal")
        self._entry_nuevo_valor.delete(0, "end")
        self._entry_nuevo_valor.config(state="disabled")
        self._var_pago_completo.set(False)
        self._var_pago_parcial.set(False)

        self._cargar_registros()

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
