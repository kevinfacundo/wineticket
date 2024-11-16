function cambiarCantidad(cambio) {
    const inputCantidad = document.getElementById("cantidad-entradas");
    let cantidad = parseInt(inputCantidad.value) + cambio;

    // Asegura que la cantidad no sea menor que 1
    if (cantidad < 1) cantidad = 1;
    // Actualiza el valor del input
    inputCantidad.value = cantidad;

    // Llama a calcularTotal para actualizar el total
    calcularTotal();
}

function calcularTotal() {
    const cantidadEntradas = parseInt(document.getElementById("cantidad-entradas").value);
    const tipoEntrada = document.getElementById("types-tickets");
    // Obtiene el precio del atributo data-precio
    const precio = parseInt(tipoEntrada.options[tipoEntrada.selectedIndex].getAttribute('data-precio'));
    
    // Calcula el total
    const total = cantidadEntradas * precio;
    
    // Actualiza el total en el HTML
    document.getElementById("total").innerText = total;
}

// Inicializa el total al cargar la página
window.onload = function() {
    calcularTotal();
};
