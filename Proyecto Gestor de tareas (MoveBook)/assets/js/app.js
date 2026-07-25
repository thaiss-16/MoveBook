const contenedor = document.getElementById('calendar');

const opciones = {
  defaultView: 'week', 
  useFormPopup: true, 
  useDetailPopup: true, 
  week: {
    taskView: true,    
    eventView: ['time'], 
    hourStart: 7,    
    hourEnd: 22,       
  },
  // 🎨 Modificamos ÚNICAMENTE el color de las tareas a rosa, manteniendo su fondo interno blanco
  theme: {
    week: {
      timeGridEvent: {
        color: '#ffffff',               /* Texto blanco */
        backgroundColor: '#ff6b90',     /* El cuerpo de la tarea en rosa */
        borderLeft: '4px solid #e04d70'  /* Borde izquierdo un rosa más oscuro para dar relieve */
      }
    }
  }
};

const botonNuevaTarea = document.getElementById('btnNuevaTarea'); 

const calendar = new tui.Calendar(contenedor, opciones);

function cargarTareasDesdeBaseDeDatos() {
    fetch('/api/tareas')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                calendar.clear();
                calendar.createEvents(data.tareas);
            } else {
                console.error('Error al traer tareas:', data.message);
            }
        })
        .catch(error => console.error('Error en la petición de tareas:', error));
}

// BOTON DE AGG NUEVA TAREA
if (botonNuevaTarea) {
    botonNuevaTarea.addEventListener('click', function() {
        calendar.openFormPopup({
            start: new Date(), 
            end: new Date(Date.now() + 60 * 60 * 1000), 
        });
    });
}

calendar.on('beforeCreateEvent', function(eventData) {
    const inicioISO = new Date(eventData.start.getTime()).toISOString();
    const finISO = new Date(eventData.end.getTime()).toISOString();
    
    const nuevaTarea = {
        title: eventData.title,
        category: eventData.isAllday ? 'task' : 'time',
        start: inicioISO, 
        end: finISO,   
        backgroundColor: eventData.backgroundColor || '#ff6b90'
    };

    fetch('/api/tareas/guardar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuevaTarea)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('¡Tarea guardada en la base de datos!');
            cargarTareasDesdeBaseDeDatos(); 
            if (calendar.closePopup) { calendar.closePopup(); }
        } else {
            alert('Error al guardar: ' + data.message);
        }
    })
    .catch(error => console.error('Error en la petición de guardar:', error));
});

calendar.on('beforeUpdateEvent', function({ event, changes }) { //editar tarea
    const tareaActualizada = {
        id: event.id,
        title: changes.title || event.title,
        category: changes.isAllday ? 'task' : 'time',
        start: changes.start ? new Date(changes.start.getTime()).toISOString() : new Date(event.start.getTime()).toISOString(),
        end: changes.end ? new Date(changes.end.getTime()).toISOString() : new Date(event.end.getTime()).toISOString(),
        backgroundColor: changes.backgroundColor || event.backgroundColor || '#ff6b90'
    };

    fetch('/api/tareas/modificar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tareaActualizada)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('¡Tarea modificada correctamente!');
            cargarTareasDesdeBaseDeDatos();
        } else {
            alert('Error al modificar: ' + data.message);
        }
    })
    .catch(error => console.error('Error en la petición de modificar:', error));
});

calendar.on('beforeDeleteEvent', function(eventData) {   //eliminar tarea
    if (!confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        return;
    }

    fetch('/api/tareas/eliminar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: eventData.id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Tarea eliminada.');
            cargarTareasDesdeBaseDeDatos();
        } else {
            alert('Error al eliminar: ' + data.message);
        }
    })
    .catch(error => console.error('Error en la petición de eliminar:', error));
});

cargarTareasDesdeBaseDeDatos();

// BOTON CERRAR SESION
const cerrarSesion = document.getElementById('cerrarSesion');
if (cerrarSesion) {
    cerrarSesion.addEventListener('click', function() {
        window.location.href = '/logout';
    });
}

// BOTON IR A LISTAS 
const botonIrAListas = document.getElementById('btn_lista');
if (botonIrAListas) {
    botonIrAListas.addEventListener('click', function() {
        window.location.href = '/listas';
    });
}