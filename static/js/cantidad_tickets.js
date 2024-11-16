function cambiarCantidad(cambio) {
    const inputCantidad = document.getElementById("cantidad-entradas");
    let cantidad = parseInt(inputCantidad.value) + cambio;
    if (cantidad < 1) cantidad = 1; // Asegura que la cantidad no sea menor que 1
    inputCantidad.value = cantidad;
    calcularTotal(); // Llama a calcularTotal para actualizar el total
}

function calcularTotal() {
    const cantidadEntradas = parseInt(document.getElementById("cantidad-entradas").value);
    const tipoEntrada = document.getElementById("types-tickets");
    const precio = parseInt(tipoEntrada.options[tipoEntrada.selectedIndex].getAttribute('data-precio'));
    
    // Calcular el total
    const total = cantidadEntradas * precio;
    
    // Actualizar el total en la página
    document.getElementById("total").innerText = total;
}

// Inicializar el total al cargar la página
window.onload = calcularTotal;
