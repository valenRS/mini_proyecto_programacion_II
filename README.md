# Rifa Navideña — Gestión de boletas

**Universidad Tecnológica de Pereira · Ingeniería Electrónica · Programación II**

Aplicación de escritorio en Python/Tkinter para registrar la venta de boletas de una rifa. Cada boleta vale **$5.000** y el premio es una ancheta navideña. Toda la información se guarda en un archivo `.csv` que persiste aunque el programa se cierre.

---

## Cómo ejecutar

```bash
python main.py
```

> Requiere Python 3 con Tkinter (incluido por defecto en la mayoría de instalaciones).

---

## Flujo del programa

El programa tiene **tres ventanas** que se abren y cierran entre sí:

```
┌─────────────────────────────────────────────────────────┐
│  1. REGISTRO (ventana principal)                        │
│                                                         │
│  Llena el formulario con los datos del comprador:       │
│  nombre, teléfono, correo, fecha, cuántas boletas       │
│  quiere y cuáles números elige (de las disponibles).    │
│  El total a pagar se calcula solo. Indica si el pago    │
│  fue completo o parcial y escribe el valor pagado.      │
│  Pulsa "Registrar compra" → se guarda en el CSV.        │
│                                                         │
│  Desde aquí puedes ir a:                               │
│    ┌──────────────────┐   ┌──────────────────┐         │
│    │  2. ACTUALIZAR   │   │   3. RESUMEN     │         │
│    └──────────────────┘   └──────────────────┘         │
└─────────────────────────────────────────────────────────┘

2. ACTUALIZAR
   Muestra la tabla con todos los compradores registrados.
   Haz clic en una fila → edita el valor pagado y/o cambia
   el estado a "completo". Pulsa "Guardar cambios".

3. RESUMEN
   Muestra tres indicadores calculados desde el CSV:
     • Porcentaje de boletas vendidas (con barra de progreso)
     • Total de dinero recibido hasta ahora
     • Total de dinero pendiente por cobrar
   También muestra el historial completo de compras.
```

En todas las ventanas hay un botón para volver al registro. **Al abrir una ventana nueva, la anterior se cierra automáticamente.**

---

## Cómo cambiar el número de boletas

Abre el archivo **`configuracion.py`** y cambia el valor de `TOTAL_BOLETAS`:

```python
# configuracion.py

PRECIO_BOLETA = 5_000   # Precio por boleta en pesos
TOTAL_BOLETAS = 100     # ← cambia este número
```

Por ejemplo, para una rifa de 50 boletas:

```python
TOTAL_BOLETAS = 50
```

Guarda el archivo y vuelve a ejecutar `python main.py`. El sistema ajusta automáticamente los números disponibles, el Combobox de cantidad y los cálculos del resumen.

---

## Estructura del proyecto

```
miniproyecto_programacion_II/
├── main.py                  → punto de entrada (ejecutar este archivo)
├── configuracion.py         → precio, total de boletas, colores y fuentes
├── manejador_datos.py       → toda la lectura/escritura del archivo CSV
├── ventana_registro.py      → formulario de registro de compradores
├── ventana_actualizacion.py → tabla para modificar pagos existentes
└── ventana_resumen.py       → estadísticas generales de la rifa
```

> El archivo `rifa_datos.csv` se crea automáticamente en la misma carpeta la primera vez que se registra una compra.
