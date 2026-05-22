Mini proyecto - Programación II
Universidad Tecnológica de Pereira – Programa de ingeniería electrónica
MSc. Yurley Tatiana Tovar Martínez

Diseñar una aplicación en Tkinter, la cual permita gestionar la venta de boletas de una rifa cuyo valor de cada una es de $5.000 pesos y el premio es una ancheta navideña. La interfaz debe permitir registrar a los participantes, verificar las boletas disponibles y generar un informe detallado del proceso. El programa debe funcionar de la siguiente manera:
La ventana principal de la aplicación debe estar diseñada para gestionar el registro de compradores de la rifa. Los datos por almacenar son los siguientes: Nombre, teléfono, correo, fecha, total de boletas a comprar (menú Combobox validando que no se exceda la cantidad disponible) junto a sus correspondientes números, valor pagado, si fue parcial o completo (checkbuttons) y total a pagar que debe ser calculado de manera automática. Tenga en cuenta que todos los datos deben ser ingresados o seleccionados obligatoriamente (1.0).
La interfaz debe garantizar el almacenamiento de un número indeterminado de compras en un archivo con extensión “.csv”. La información no debe sobrescribirse ni eliminarse, aunque la aplicación se cierre por algún motivo (1.0).
Esta ventana debe tener dos botones adicionales, cuya funcionalidad consiste en abrir interfaces externas las cuales tienen los siguientes objetivos: Actualización de datos y resumen de la información. Tenga en cuenta que al generar la apertura de una nueva interfaz se debe cerrar la anterior (1.0).
La sección de actualización debe permitir modificar la base de datos en función del valor pagado por el usuario y el campo de si es parcial o completo, es decir, en el archivo con extensión “.csv” (1.0).
Finalmente, el resumen de la información se basa en los siguientes datos: (1.0)
❖ Porcentaje de boletas vendidas.
❖ Total de dinero recibido.
❖ Total de dinero que los usuarios aún no han pagado y deben pagar.
Nota: La interfaz implementada se debe poder ejecutar a partir de una cabecera y es obligatorio utilizar programación orientada a objetos, de lo contrario se calificará sobre 2.5.
