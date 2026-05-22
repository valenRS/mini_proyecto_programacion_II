# =============================================================================
#  ventana_registro.py
#  Rifa Navideña — Programación II · Universidad Tecnológica de Pereira
#
#  Ventana principal de la aplicación: formulario de registro de compradores.
#  Desde aquí se pueden abrir las otras dos ventanas (actualización y resumen).
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from configuracion import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_DORADO,
    COLOR_TEXTO_CLARO, COLOR_FORMULARIO, COLOR_TEXTO_FORM,
    COLOR_BOTON_PPAL, COLOR_BOTON_SEC, COLOR_EXITO, COLOR_ADVERTENCIA,
    FUENTE_NORMAL, FUENTE_LABEL, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_PEQUEÑA,
    PRECIO_BOLETA, TOTAL_BOLETAS,
)
from manejador_datos import ManejadorDatos


MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


class VentanaRegistro:
    """
    Ventana principal: registra la compra de boletas de un participante.

    Contiene cuatro secciones:
      1. Encabezado con el nombre de la rifa.
      2. Datos del comprador (nombre, teléfono, correo, fecha).
      3. Selección de boletas (cantidad, números específicos, total).
      4. Información de pago (valor pagado, estado completo/parcial).
    """

    def __init__(self, raiz: tk.Tk):
        self.raiz     = raiz
        self.manejador = ManejadorDatos()
        self._total_actual = 0       # Total a pagar como número (se actualiza al elegir cantidad)
        self._indices_bloqueados = set()  # Índices seleccionados cuando el listbox está lleno

        self.raiz.title("Rifa Navideña · Registro de compradores")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.resizable(False, False)

        self._configurar_estilos_ttk()
        self._crear_interfaz()
        self._centrar_ventana()

    # ------------------------------------------------------------------ #
    #  Utilidades generales                                               #
    # ------------------------------------------------------------------ #

    def _centrar_ventana(self):
        """Ubica la ventana en el centro de la pantalla al abrirla."""
        self.raiz.update_idletasks()
        w = self.raiz.winfo_width()
        h = self.raiz.winfo_height()
        x = (self.raiz.winfo_screenwidth()  - w) // 2
        y = (self.raiz.winfo_screenheight() - h) // 2
        self.raiz.geometry(f"{w}x{h}+{x}+{y}")

    def _configurar_estilos_ttk(self):
        """Aplica un estilo uniforme a los Combobox de la ventana."""
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "TCombobox",
            fieldbackground=COLOR_FORMULARIO,
            background=COLOR_FORMULARIO,
            foreground=COLOR_TEXTO_FORM,
            selectbackground=COLOR_ACENTO,
            selectforeground="white",
            arrowcolor=COLOR_ACENTO,
        )

    def _crear_campo_entrada(self, padre, ancho=26):
        """
        Construye un campo de texto (Entry) con un borde de color de acento.
        Retorna (contenedor, entry) para poder ubicar el contenedor con grid/pack.
        """
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

    def _solo_digitos(self, nuevo_valor: str) -> bool:
        """Validatecommand: acepta solo dígitos en el campo de valor pagado."""
        return nuevo_valor == "" or nuevo_valor.isdigit()

    # ------------------------------------------------------------------ #
    #  Construcción de la interfaz                                        #
    # ------------------------------------------------------------------ #

    def _crear_interfaz(self):
        self._crear_encabezado()

        # Marco que contiene las dos secciones superiores en columnas
        marco_central = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=16, pady=4)
        marco_central.pack(fill="both")

        self._crear_seccion_datos(marco_central)
        self._crear_seccion_boletas(marco_central)

        # Secciones inferiores ocupan todo el ancho
        self._crear_seccion_pago()
        self._crear_barra_botones()

    def _crear_encabezado(self):
        marco = tk.Frame(self.raiz, bg=COLOR_ACENTO, pady=14)
        marco.pack(fill="x")

        tk.Label(
            marco,
            text="🎟  RIFA NAVIDEÑA",
            font=FUENTE_TITULO,
            bg=COLOR_ACENTO,
            fg="white",
        ).pack()

        tk.Label(
            marco,
            text=(
                f"Premio: Ancheta navideña  ·  "
                f"Valor por boleta: ${PRECIO_BOLETA:,}  ·  "
                f"{TOTAL_BOLETAS} boletas en total"
            ),
            font=FUENTE_PEQUEÑA,
            bg=COLOR_ACENTO,
            fg="#FFD0D6",
        ).pack()

    def _crear_seccion_datos(self, contenedor):
        """Sección izquierda: nombre, teléfono, correo y fecha del comprador."""
        marco = tk.LabelFrame(
            contenedor,
            text="  Datos del comprador  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=16,
            pady=12,
        )
        marco.pack(side="left", fill="y", padx=(0, 10), pady=8)

        # ── Campos de texto ──────────────────────────────────────────────
        campos = [
            ("Nombre completo:",     "_entry_nombre"),
            ("Teléfono:",            "_entry_telefono"),
            ("Correo electrónico:",  "_entry_correo"),
        ]

        for fila, (etiqueta, nombre_attr) in enumerate(campos):
            tk.Label(
                marco, text=etiqueta, font=FUENTE_LABEL,
                bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
            ).grid(row=fila * 2, column=0, sticky="w", pady=(8, 0))

            contenedor_campo, campo = self._crear_campo_entrada(marco)
            contenedor_campo.grid(row=fila * 2 + 1, column=0, sticky="ew", pady=(3, 0))
            setattr(self, nombre_attr, campo)

        # ── Separador decorativo ─────────────────────────────────────────
        fila_sep = len(campos) * 2
        tk.Frame(marco, bg=COLOR_ACENTO, height=1).grid(
            row=fila_sep, column=0, sticky="ew", pady=12,
        )

        # ── Fecha de compra ──────────────────────────────────────────────
        fila_fecha = fila_sep + 1
        tk.Label(
            marco, text="Fecha de compra:", font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=fila_fecha, column=0, sticky="w")

        marco_fecha = tk.Frame(marco, bg=COLOR_PANEL)
        marco_fecha.grid(row=fila_fecha + 1, column=0, sticky="w", pady=(4, 0))

        año_actual = datetime.now().year

        self._combo_dia = ttk.Combobox(
            marco_fecha,
            values=[str(d) for d in range(1, 32)],
            width=4, state="readonly", font=FUENTE_NORMAL,
        )
        self._combo_dia.set(str(datetime.now().day))
        self._combo_dia.pack(side="left", padx=(0, 6))

        self._combo_mes = ttk.Combobox(
            marco_fecha,
            values=MESES,
            width=11, state="readonly", font=FUENTE_NORMAL,
        )
        self._combo_mes.set(MESES[datetime.now().month - 1])
        self._combo_mes.pack(side="left", padx=(0, 6))

        self._combo_año = ttk.Combobox(
            marco_fecha,
            values=[str(año_actual - 1), str(año_actual), str(año_actual + 1)],
            width=6, state="readonly", font=FUENTE_NORMAL,
        )
        self._combo_año.set(str(año_actual))
        self._combo_año.pack(side="left")

    def _crear_seccion_boletas(self, contenedor):
        """Sección derecha: cantidad, números de boleta disponibles y total."""
        marco = tk.LabelFrame(
            contenedor,
            text="  Selección de boletas  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=16,
            pady=12,
        )
        marco.pack(side="left", fill="both", expand=True, pady=8)

        # ── Combobox de cantidad ─────────────────────────────────────────
        tk.Label(
            marco, text="¿Cuántas boletas desea comprar?",
            font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        boletas_disponibles = self.manejador.boletas_disponibles()
        opciones_cantidad   = [str(i) for i in range(1, len(boletas_disponibles) + 1)]

        self._combo_cantidad = ttk.Combobox(
            marco, values=opciones_cantidad,
            width=6, state="readonly", font=FUENTE_NORMAL,
        )
        self._combo_cantidad.grid(row=1, column=0, sticky="w", pady=(4, 10))
        self._combo_cantidad.bind("<<ComboboxSelected>>", self._al_cambiar_cantidad)

        # ── Listbox de números ───────────────────────────────────────────
        tk.Label(
            marco,
            text="Números disponibles  (Ctrl+clic para elegir varios):",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=2, column=0, columnspan=2, sticky="w")

        marco_lista = tk.Frame(marco, bg=COLOR_ACENTO, padx=1, pady=1)
        marco_lista.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        barra_scroll = tk.Scrollbar(marco_lista, orient="vertical")
        self._listbox_numeros = tk.Listbox(
            marco_lista,
            selectmode="multiple",
            font=FUENTE_NORMAL,
            bg=COLOR_FORMULARIO,
            fg=COLOR_TEXTO_FORM,
            selectbackground=COLOR_ACENTO,
            selectforeground="white",
            relief="flat",
            bd=0,
            width=24,
            height=7,
            yscrollcommand=barra_scroll.set,
            exportselection=False,
            activestyle="none",
        )
        barra_scroll.config(command=self._listbox_numeros.yview)
        self._listbox_numeros.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")
        self._listbox_numeros.bind("<<ListboxSelect>>", self._al_seleccionar_numeros)

        self._llenar_listbox()
        self._listbox_numeros.config(state="disabled")

        # ── Contador de selección ────────────────────────────────────────
        self._label_contador = tk.Label(
            marco, text="Seleccionados: 0 / 0",
            font=FUENTE_PEQUEÑA, bg=COLOR_PANEL, fg=COLOR_DORADO,
        )
        self._label_contador.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # ── Total a pagar ────────────────────────────────────────────────
        marco_total = tk.Frame(marco, bg=COLOR_PANEL)
        marco_total.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        tk.Label(
            marco_total, text="Total a pagar:",
            font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).pack(side="left")

        self._label_total_pagar = tk.Label(
            marco_total, text="$ 0",
            font=FUENTE_SUBTITULO, bg=COLOR_PANEL, fg=COLOR_DORADO,
        )
        self._label_total_pagar.pack(side="left", padx=(10, 0))

    def _crear_seccion_pago(self):
        """Sección inferior: valor pagado y estado del pago (completo/parcial)."""
        marco = tk.LabelFrame(
            self.raiz,
            text="  Información de pago  ",
            font=FUENTE_LABEL,
            bg=COLOR_PANEL,
            fg=COLOR_DORADO,
            bd=2,
            relief="groove",
            padx=16,
            pady=12,
        )
        marco.pack(fill="x", padx=16, pady=(0, 8))

        # ── Valor pagado ─────────────────────────────────────────────────
        tk.Label(
            marco, text="Valor pagado ($):",
            font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_TEXTO_CLARO,
        ).grid(row=0, column=0, sticky="w")

        contenedor_pago, self._entry_valor_pagado = self._crear_campo_entrada(marco, ancho=18)
        contenedor_pago.grid(row=0, column=1, padx=(10, 40), ipady=2)
        vcmd = (self.raiz.register(self._solo_digitos), "%P")
        self._entry_valor_pagado.config(validate="key", validatecommand=vcmd)

        # ── Checkbuttons (mutuamente exclusivos) ─────────────────────────
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
            command=self._al_marcar_pago_completo,
        ).grid(row=0, column=2, padx=(0, 20))

        tk.Checkbutton(
            marco,
            text=" Pago parcial",
            variable=self._var_pago_parcial,
            font=FUENTE_LABEL,
            bg=COLOR_PANEL, fg=COLOR_ADVERTENCIA,
            selectcolor=COLOR_FONDO,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_ADVERTENCIA,
            command=self._al_marcar_pago_parcial,
        ).grid(row=0, column=3)

    def _crear_barra_botones(self):
        """Barra inferior con el botón principal y los de navegación."""
        marco = tk.Frame(self.raiz, bg=COLOR_FONDO, padx=16, pady=10)
        marco.pack(fill="x")

        tk.Button(
            marco,
            text="✔  Registrar compra",
            command=self._validar_y_guardar,
            font=FUENTE_SUBTITULO,
            bg=COLOR_BOTON_PPAL, fg="white",
            activebackground="#C73652", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=22, pady=10, bd=0,
        ).pack(side="left", padx=(0, 14))

        tk.Button(
            marco,
            text="✎  Actualizar datos",
            command=self._abrir_actualizacion,
            font=FUENTE_NORMAL,
            bg=COLOR_BOTON_SEC, fg=COLOR_TEXTO_CLARO,
            activebackground="#1A4A80", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=16, pady=10, bd=0,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            marco,
            text="📊  Ver resumen",
            command=self._abrir_resumen,
            font=FUENTE_NORMAL,
            bg=COLOR_BOTON_SEC, fg=COLOR_TEXTO_CLARO,
            activebackground="#1A4A80", activeforeground="white",
            relief="flat", cursor="hand2",
            padx=16, pady=10, bd=0,
        ).pack(side="left")

        # Contador de boletas disponibles (esquina derecha)
        self._label_disponibles = tk.Label(
            marco,
            text=self._texto_disponibles(),
            font=FUENTE_PEQUEÑA,
            bg=COLOR_FONDO, fg=COLOR_TEXTO_CLARO,
        )
        self._label_disponibles.pack(side="right")

    # ------------------------------------------------------------------ #
    #  Lógica: sección de boletas                                         #
    # ------------------------------------------------------------------ #

    def _llenar_listbox(self):
        """Carga los números de boleta disponibles en el Listbox."""
        self._listbox_numeros.delete(0, "end")
        for numero in self.manejador.boletas_disponibles():
            self._listbox_numeros.insert("end", f"   Boleta  # {numero:03d}")

    def _al_cambiar_cantidad(self, evento=None):
        """Se activa al cambiar la cantidad en el Combobox: limpia la selección y recalcula."""
        self._indices_bloqueados = set()
        self._resetear_colores_listbox()
        self._listbox_numeros.config(state="normal")
        self._listbox_numeros.selection_clear(0, "end")
        self._actualizar_contador()
        self._calcular_total()

    def _al_seleccionar_numeros(self, evento=None):
        """Se activa al hacer clic en el Listbox: controla el límite de selección."""
        pedidas          = self._cantidad_pedida()
        seleccion_actual = set(self._listbox_numeros.curselection())
        elegidas         = len(seleccion_actual)

        if self._indices_bloqueados:
            # Modo lleno: solo se permite deseleccionar ítems ya elegidos
            if elegidas > len(self._indices_bloqueados):
                # Intentó añadir uno nuevo → revertir al estado bloqueado
                self._listbox_numeros.selection_clear(0, "end")
                for i in self._indices_bloqueados:
                    self._listbox_numeros.selection_set(i)
            else:
                # Deseleccionó uno → desbloquear y restaurar colores
                self._indices_bloqueados = set()
                self._resetear_colores_listbox()
        else:
            # Modo normal: limitar a la cantidad pedida
            if pedidas > 0 and elegidas > pedidas:
                ultimo = self._listbox_numeros.curselection()[-1]
                self._listbox_numeros.selection_clear(ultimo)
                elegidas = pedidas

            # Al alcanzar el máximo, activar bloqueo suave con oscurecimiento visual
            if elegidas >= pedidas > 0:
                self._indices_bloqueados = set(self._listbox_numeros.curselection())
                self._aplicar_bloqueo_visual()

        self._actualizar_contador()

    def _aplicar_bloqueo_visual(self):
        """Oscurece los ítems no seleccionados para indicar que el listbox está lleno."""
        for i in range(self._listbox_numeros.size()):
            if i not in self._indices_bloqueados:
                self._listbox_numeros.itemconfigure(i, fg="#4A4A6A")

    def _resetear_colores_listbox(self):
        """Restaura el color original de todos los ítems del listbox."""
        for i in range(self._listbox_numeros.size()):
            self._listbox_numeros.itemconfigure(i, fg=COLOR_TEXTO_FORM)

    def _actualizar_contador(self):
        pedidas  = self._cantidad_pedida()
        elegidas = len(self._listbox_numeros.curselection())
        completo = elegidas == pedidas and pedidas > 0

        self._label_contador.config(
            text=f"Seleccionados: {elegidas} / {pedidas}",
            fg=COLOR_EXITO if completo else COLOR_DORADO,
        )

    def _calcular_total(self):
        self._total_actual = self._cantidad_pedida() * PRECIO_BOLETA
        self._label_total_pagar.config(text=f"$ {self._total_actual:,}")

        # Si ya estaba marcado como pago completo, actualizar el campo de valor pagado
        if self._var_pago_completo.get():
            self._entry_valor_pagado.config(state="normal")
            self._entry_valor_pagado.delete(0, "end")
            self._entry_valor_pagado.insert(0, str(self._total_actual))
            self._entry_valor_pagado.config(state="readonly")

    def _cantidad_pedida(self) -> int:
        """Retorna como número la cantidad elegida en el Combobox."""
        valor = self._combo_cantidad.get()
        return int(valor) if valor.isdigit() else 0

    def _texto_disponibles(self) -> str:
        disponibles = len(self.manejador.boletas_disponibles())
        return f"Disponibles: {disponibles} / {TOTAL_BOLETAS}"

    # ------------------------------------------------------------------ #
    #  Lógica: sección de pago                                            #
    # ------------------------------------------------------------------ #

    def _al_marcar_pago_completo(self):
        """Al marcar 'Pago completo': desactiva parcial y llena el valor pagado."""
        if self._var_pago_completo.get():
            self._var_pago_parcial.set(False)
            self._entry_valor_pagado.config(state="normal")
            self._entry_valor_pagado.delete(0, "end")
            self._entry_valor_pagado.insert(0, str(self._total_actual))
            self._entry_valor_pagado.config(state="readonly")
        else:
            # Si se desmarca manualmente, el campo queda editable y vacío
            self._entry_valor_pagado.config(state="normal")
            self._entry_valor_pagado.delete(0, "end")

    def _al_marcar_pago_parcial(self):
        """Al marcar 'Pago parcial': desactiva completo y habilita el campo para editar."""
        if self._var_pago_parcial.get():
            self._var_pago_completo.set(False)
            self._entry_valor_pagado.config(state="normal")
            self._entry_valor_pagado.delete(0, "end")

    # ------------------------------------------------------------------ #
    #  Validación y guardado del formulario                               #
    # ------------------------------------------------------------------ #

    def _validar_y_guardar(self):
        """Verifica que todos los campos estén completos y guarda la compra en el CSV."""

        # ── 1. Datos del comprador ────────────────────────────────────────
        nombre   = self._entry_nombre.get().strip()
        telefono = self._entry_telefono.get().strip()
        correo   = self._entry_correo.get().strip()

        if not nombre:
            messagebox.showwarning("Campo requerido", "El nombre del comprador es obligatorio.")
            self._entry_nombre.focus()
            return
        if not telefono:
            messagebox.showwarning("Campo requerido", "El teléfono es obligatorio.")
            self._entry_telefono.focus()
            return
        if not correo:
            messagebox.showwarning("Campo requerido", "El correo electrónico es obligatorio.")
            self._entry_correo.focus()
            return

        # ── 2. Fecha ──────────────────────────────────────────────────────
        if not self._combo_dia.get() or not self._combo_mes.get() or not self._combo_año.get():
            messagebox.showwarning("Campo requerido", "Debes seleccionar la fecha completa.")
            return
        fecha = f"{self._combo_dia.get()} de {self._combo_mes.get()} de {self._combo_año.get()}"

        # ── 3. Cantidad de boletas ────────────────────────────────────────
        cantidad = self._cantidad_pedida()
        if cantidad == 0:
            messagebox.showwarning("Campo requerido",
                                   "Debes seleccionar cuántas boletas desea comprar.")
            return

        # ── 4. Números de boleta seleccionados ───────────────────────────
        indices_elegidos = self._listbox_numeros.curselection()
        if len(indices_elegidos) != cantidad:
            messagebox.showwarning(
                "Números incompletos",
                f"Debes seleccionar exactamente {cantidad} número(s) de boleta.\n"
                f"Actualmente tienes {len(indices_elegidos)} seleccionado(s).",
            )
            return

        # ── 5. Estado de pago ─────────────────────────────────────────────
        if not self._var_pago_completo.get() and not self._var_pago_parcial.get():
            messagebox.showwarning("Campo requerido",
                                   "Indica si el pago fue completo o parcial.")
            return

        # ── 6. Valor pagado ───────────────────────────────────────────────
        valor_texto = self._entry_valor_pagado.get().strip()
        if not valor_texto:
            messagebox.showwarning("Campo requerido",
                                   "Ingresa el valor que pagó el comprador.")
            self._entry_valor_pagado.focus()
            return
        valor_pagado = int(valor_texto)  # Solo dígitos — garantizado por validatecommand
        if valor_pagado <= 0:
            messagebox.showerror(
                "Valor inválido",
                "El valor pagado debe ser mayor que cero.",
            )
            self._entry_valor_pagado.focus()
            return
        if valor_pagado > self._total_actual:
            messagebox.showerror(
                "Valor inválido",
                f"El valor pagado (${valor_pagado:,}) no puede superar\n"
                f"el total a pagar (${self._total_actual:,}).",
            )
            self._entry_valor_pagado.focus()
            return

        # ── 7. Construir el registro y guardar ────────────────────────────
        boletas_disp   = self.manejador.boletas_disponibles()
        numeros_elegidos = [boletas_disp[i] for i in indices_elegidos]
        numeros_texto    = "-".join(str(n) for n in sorted(numeros_elegidos))
        estado_pago      = "Si" if valor_pagado == self._total_actual else "No"

        datos_compra = {
            "nombre":           nombre,
            "telefono":         telefono,
            "correo":           correo,
            "fecha":            fecha,
            "cantidad_boletas": str(cantidad),
            "numeros_boletas":  numeros_texto,
            "valor_pagado":     str(valor_pagado),
            "pago_completo":    estado_pago,
            "total_a_pagar":    str(self._total_actual),
        }

        self.manejador.guardar_compra(datos_compra)

        messagebox.showinfo(
            "¡Registro exitoso!",
            f"La compra fue guardada correctamente.\n\n"
            f"Comprador : {nombre}\n"
            f"Boletas   : #{numeros_texto.replace('-', '  #')}\n"
            f"Total     : ${self._total_actual:,}\n"
            f"Pagó      : ${valor_pagado:,}",
        )

        self._limpiar_formulario()

    def _limpiar_formulario(self):
        """Deja el formulario en blanco para registrar una nueva compra."""
        self._entry_nombre.delete(0, "end")
        self._entry_telefono.delete(0, "end")
        self._entry_correo.delete(0, "end")

        # Actualizar opciones de cantidad con las boletas que quedan disponibles
        boletas_disp    = self.manejador.boletas_disponibles()
        nuevas_opciones = [str(i) for i in range(1, len(boletas_disp) + 1)]
        self._combo_cantidad["values"] = nuevas_opciones
        self._combo_cantidad.set("")

        # Recargar el Listbox
        self._llenar_listbox()
        self._listbox_numeros.config(state="disabled")

        # Reiniciar campos calculados y estados
        self._total_actual = 0
        self._label_total_pagar.config(text="$ 0")
        self._label_contador.config(text="Seleccionados: 0 / 0", fg=COLOR_DORADO)

        self._entry_valor_pagado.config(state="normal")
        self._entry_valor_pagado.delete(0, "end")
        self._var_pago_completo.set(False)
        self._var_pago_parcial.set(False)

        self._label_disponibles.config(text=self._texto_disponibles())

    # ------------------------------------------------------------------ #
    #  Navegación entre ventanas                                          #
    # ------------------------------------------------------------------ #

    def _abrir_actualizacion(self):
        """Cierra esta ventana y abre la ventana de actualización de datos."""
        from ventana_actualizacion import VentanaActualizacion
        self.raiz.destroy()
        nueva_raiz = tk.Tk()
        VentanaActualizacion(nueva_raiz)
        nueva_raiz.mainloop()

    def _abrir_resumen(self):
        """Cierra esta ventana y abre la ventana de resumen estadístico."""
        from ventana_resumen import VentanaResumen
        self.raiz.destroy()
        nueva_raiz = tk.Tk()
        VentanaResumen(nueva_raiz)
        nueva_raiz.mainloop()
