// ==========================================
// BOTÓN IR AL CALENDARIO 
// ==========================================
const botonIrAlCalendario = document.getElementById('btn_volver');
if (botonIrAlCalendario) {
    botonIrAlCalendario.addEventListener('click', function() {
        window.location.href = '/gestor';
    });
}

// Limpiar el formulario de nueva lista al hacer clic en el botón (+)
const btnAgregarLista = document.getElementById('btn_agregar_lista');
const formNuevaLista = document.getElementById('formNuevaLista');
if (btnAgregarLista && formNuevaLista) {
    btnAgregarLista.addEventListener('click', () => {
        formNuevaLista.reset();
    });
}

// ==========================================
// GUARDAR NUEVA LISTA
// ==========================================
if (formNuevaLista) {
    formNuevaLista.addEventListener('submit', function(e) {
        e.preventDefault();

        const datosLista = {
            nombre: document.getElementById('titulo_lista').value,
            texto: document.getElementById('contenido_lista').value
        };

        fetch('/api/listas/guardar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datosLista)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('¡Lista creada con éxito!');
                window.location.reload(); 
            } else {
                alert('Error al guardar: ' + data.message);
            }
        })
        .catch(error => console.error('Error en la petición de listas:', error));
    });
}

// ==========================================
// VER, EDITAR Y ELIMINAR DETALLES VIA ID
// ==========================================
const btnEditarOpcion = document.getElementById('btn_editar_opcion');
const btnEliminarOpcion = document.getElementById('btn_eliminar_opcion');

const inputId = document.getElementById('ver_id_lista');
const inputTitulo = document.getElementById('ver_titulo_lista');
const inputContenido = document.getElementById('ver_contenido_lista');

// Interceptamos clics usando la delegación de eventos buscando el ID de la nota
document.addEventListener('click', function (e) {
    // Buscamos el elemento o el botón más cercano que contenga un ID
    const botonNota = e.target.closest('button');
    
    // Verificamos si existe el botón y si su ID empieza con "nota-"
    if (botonNota && botonNota.id && botonNota.id.startsWith('nota-')) {
        const idLista = botonNota.getAttribute('data-id');
        
        inputId.value = idLista;
        inputTitulo.value = botonNota.innerText.trim();
        inputContenido.value = "Cargando contenido...";

        fetch(`/api/listas/obtener/${idLista}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    inputContenido.value = data.texto;

                    // Bloquear campos para el modo lectura inicial
                    inputTitulo.setAttribute('readonly', true);
                    inputContenido.setAttribute('readonly', true);
                    
                    if (btnEditarOpcion) {
                        btnEditarOpcion.innerText = "Editar Lista";
                        btnEditarOpcion.style.backgroundColor = ""; 
                    }
                    
                    // 🛠️ REMOCIÓN TOTAL DE RESIDUOS: Borramos cualquier backdrop fantasma antes de abrir
                    document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';

                    // Inicializamos y abrimos el modal de manera manual y limpia
                    const elementoModal = document.getElementById('modalVerLista');
                    let modalBootstrap = bootstrap.Modal.getInstance(elementoModal);
                    if (!modalBootstrap) {
                        modalBootstrap = new bootstrap.Modal(elementoModal);
                    }
                    modalBootstrap.show();

                } else {
                    alert('Error al cargar la lista: ' + data.message);
                }
            })
            .catch(error => console.error('Error al obtener la lista:', error));
    }
});

// Mecanismo de edición dentro del modal
if (btnEditarOpcion) {
    btnEditarOpcion.addEventListener('click', function() {
        if (inputTitulo.hasAttribute('readonly')) {
            inputTitulo.removeAttribute('readonly');
            inputContenido.removeAttribute('readonly');
            this.innerText = "Guardar Cambios";
            this.style.backgroundColor = "#2ecc71"; 
            inputTitulo.focus();
        } else {
            const datosActualizados = {
                id: inputId.value,
                nombre: inputTitulo.value,
                texto: inputContenido.value
            };

            fetch('/api/listas/modificar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosActualizados)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('¡Lista actualizada con éxito!');
                    window.location.reload();
                } else {
                    alert('Error al modificar: ' + data.message);
                }
            })
            .catch(error => console.error('Error en la petición de modificar:', error));
        }
    });
}

// Mecanismo para eliminar la lista
if (btnEliminarOpcion) {
    btnEliminarOpcion.addEventListener('click', function() {
        if (confirm('¿Estás seguro de que deseas eliminar esta lista por completo?')) {
            fetch('/api/listas/eliminar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: inputId.value })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Lista eliminada correctamente.');
                    window.location.reload();
                } else {
                    alert('Error al eliminar: ' + data.message);
                }
            })
            .catch(error => console.error('Error en la petición de eliminar:', error));
        }
    });
}