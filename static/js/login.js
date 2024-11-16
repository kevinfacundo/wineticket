// Función para manejar el formulario de login
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Evita que el formulario se envíe de inmediato

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Aquí simularíamos un comportamiento para verificar si el usuario está registrado.
    // Como no tenemos una base de datos en el frontend, vamos a crear una verificación ficticia.
    var userDatabase = [
        { email: "user@example.com", password: "password123" },
        { email: "admin@example.com", password: "adminpass" }
    ];

    // Buscar al usuario por el correo electrónico
    var user = userDatabase.find(function(u) {
        return u.email === email;
    });

    // Si no encontramos al usuario, mostramos un mensaje de error
    if (!user) {
        document.getElementById("error-message").innerText = "Usuario no registrado.";
        document.getElementById("error-message").style.display = "block";
        return;  // Detenemos la ejecución
    }

    // Si el usuario existe, comprobamos la contraseña
    if (user.password !== password) {
        document.getElementById("error-message").innerText = "Correo o contraseña incorrectos.";
        document.getElementById("error-message").style.display = "block";
        return;
    }

    // Si todo está correcto, podemos enviar el formulario
    alert("¡Bienvenido!");
    // Aquí podrías redirigir al usuario, por ejemplo:
    // window.location.href = "/profile";  // Cambiar la URL según corresponda
});

// Función para mostrar u ocultar la contraseña
function togglePasswordVisibility() {
    var passwordField = document.getElementById("password");
    var eyeIcon = document.getElementById("eye-icon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}
