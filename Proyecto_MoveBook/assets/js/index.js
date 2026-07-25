document.addEventListener("DOMContentLoaded", function() {
    
    // Vinculamos las variables con los IDs del HTML
    const botonLogin = document.getElementById("btn-login");
    const botonRegister = document.getElementById("btn-register");

    // Redirección al hacer clic en Iniciar Sesión
    botonLogin.addEventListener("click", function() {
        window.location.href = "/inicio_sesion"; // Cambia por tu ruta real si está en otra carpeta
    });

    // Redirección al hacer clic en Registrarse
    botonRegister.addEventListener("click", function() {
        window.location.href = "/registro"; // Cambia por tu ruta real si está en otra carpeta
    });

});