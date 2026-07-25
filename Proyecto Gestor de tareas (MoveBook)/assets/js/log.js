//INICIO DE SESION

const formularioLogin = document.getElementById('log');

if (formularioLogin) {
    formularioLogin.addEventListener('submit', function(event) {
        event.preventDefault(); 

        const formData = new FormData(event.target);
        const datosConvertidos = Object.fromEntries(formData.entries());

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosConvertidos)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('¡Inicio de sesión correcto!');
                window.location.href = '/gestor'; 
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error en la petición de login:', error));
    });
}


//REGISTRO

const formularioRegistro = document.getElementById('registro');

if (formularioRegistro) {
    formularioRegistro.addEventListener('submit', function(event) {
        event.preventDefault(); 

        const formData = new FormData(event.target);
        const datosConvertidos = Object.fromEntries(formData.entries());

        fetch('/api/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosConvertidos)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('¡Registro exitoso!');
                window.location.href = '/inicio_sesion'; 
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error en la petición de registro:', error));
    });
}