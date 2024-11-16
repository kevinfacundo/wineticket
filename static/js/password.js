function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('eye-icon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text'; // Cambia a tipo texto para mostrar la contraseña
        toggleIcon.classList.remove('fa-eye'); // Cambia el ícono de ojo cerrado
        toggleIcon.classList.add('fa-eye-slash'); // Cambia al ícono de ojo abierto
    } else {
        passwordInput.type = 'password'; // Cambia a tipo password para ocultar la contraseña
        toggleIcon.classList.remove('fa-eye-slash'); // Cambia el ícono de ojo abierto
        toggleIcon.classList.add('fa-eye'); // Cambia al ícono de ojo cerrado
    }
}
