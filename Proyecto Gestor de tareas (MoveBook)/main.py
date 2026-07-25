from flask import Flask, session, redirect, url_for, render_template, request, jsonify
import os
import sqlite3

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'assets'))
app.secret_key = 'clave_secreta_super_segura_>:)'

from db import db
db.init_db()

#LOGIN Y REGISTRO
def procesar_login():
    datos = request.get_json()
    usuario = datos.get('username')
    contrasena = datos.get('password')
    datos_usuario = db.verificar_usuario(usuario, contrasena)
    
    if datos_usuario:
        session['id_usuario'] = datos_usuario[0]
        session['usuario'] = datos_usuario[1]
        return jsonify({"status": "success", "message": "Bienvenido"})
    else:
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos"})
    
def procesar_registro():
    datos = request.get_json()
    usuario = datos.get('username')
    contrasena = datos.get('password')
    if hasattr(db, 'existe_usuario') and db.existe_usuario(usuario):
        return jsonify({"status": "error", "message": "Este nombre de usuario ya está en uso."})
    try:
        db.agregar_usuario(usuario, contrasena)
        return jsonify({"status": "success", "message": "Usuario registrado exitosamente"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al guardar en la base de datos: {str(e)}"})
    
@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    session.pop('usuario', None)
    return redirect(url_for('inicio_sesion'))
    

#CALENDARIO
def api_obtener_tareas():
    if 'id_usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        lista_tareas = db.obtener_tareas(session['id_usuario'])
        return jsonify({"status": "success", "tareas": lista_tareas})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
app.add_url_rule('/api/tareas', 'api_obtener_tareas', api_obtener_tareas, methods=['GET'])

def api_guardar_tarea():
    if 'id_usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        datos = request.get_json()
        titulo = datos.get('title')
        categoria = datos.get('category', 'time') 
        inicio = datos.get('start')
        fin = datos.get('end')
        color_fondo = datos.get('backgroundColor', '#ff6b90') 

        if not titulo or not inicio or not fin:
            return jsonify({"status": "error", "message": "Faltan campos obligatorios (título, inicio o fin)"})
        
        db.agregar_tarea(titulo, categoria, inicio, fin, color_fondo, session['id_usuario'])        
        return jsonify({"status": "success", "message": "Tarea guardada con éxito"})  
          
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error en el servidor: {str(e)}"})
app.add_url_rule('/api/tareas/guardar', 'api_guardar_tarea', api_guardar_tarea, methods=['POST'])

def api_eliminar_tarea():
    if 'id_usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        datos = request.get_json()
        id_tarea = datos.get('id')
        if not id_tarea:
            return jsonify({"status": "error", "message": "Falta el ID de la tarea"})
            
        db.eliminar_tarea(id_tarea)
        return jsonify({"status": "success", "message": "Tarea eliminada con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
app.add_url_rule('/api/tareas/eliminar', 'api_eliminar_tarea', api_eliminar_tarea, methods=['POST'])

def api_modificar_tarea():
    if 'id_usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        datos = request.get_json()
        id_tarea = datos.get('id')
        titulo = datos.get('title')
        categoria = datos.get('category', 'time')
        inicio = datos.get('start')
        fin = datos.get('end')
        color_fondo = datos.get('backgroundColor', '#ff6b90')

        if not id_tarea or not titulo or not inicio or not fin:
            return jsonify({"status": "error", "message": "Faltan campos obligatorios"})

        db.modificar_tarea(id_tarea, titulo, categoria, inicio, fin, color_fondo)
        return jsonify({"status": "success", "message": "Tarea modificada con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
app.add_url_rule('/api/tareas/modificar', 'api_modificar_tarea', api_modificar_tarea, methods=['POST'])

#LISTAS
def api_guardar_lista():
    if 'usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
        
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        texto = datos.get('texto')
        usuario_activo = session['usuario'] # Tomamos el usuario dueño de la sesión

        if not nombre or not texto:
            return jsonify({"status": "error", "message": "El título y el contenido son obligatorios"})

        # Guardamos usando tu función real de db.py
        db.agregar_lista(nombre, texto, usuario_activo)
        return jsonify({"status": "success", "message": "Lista guardada con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

app.add_url_rule('/api/listas/guardar', 'api_guardar_lista', api_guardar_lista, methods=['POST'])


def api_obtener_una_lista(id_lista):
    if 'usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        with sqlite3.connect('db/database.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT texto FROM listas WHERE id_lista = ?', (id_lista,))
            fila = cursor.fetchone()
            if fila:
                return jsonify({"status": "success", "texto": fila["texto"]})
            else:
                return jsonify({"status": "error", "message": "Lista no encontrada"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

app.add_url_rule('/api/listas/obtener/<int:id_lista>', 'api_obtener_una_lista', api_obtener_una_lista, methods=['GET'])


def api_eliminar_la_lista():
    if 'usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        datos = request.get_json()
        id_lista = datos.get('id')
        db.eliminar_lista(id_lista) 
        return jsonify({"status": "success", "message": "Lista eliminada con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

app.add_url_rule('/api/listas/eliminar', 'api_eliminar_la_lista', api_eliminar_la_lista, methods=['POST'])


def api_modificar_la_lista():
    if 'usuario' not in session:
        return jsonify({"status": "error", "message": "No has iniciado sesión"}), 401
    try:
        datos = request.get_json()
        id_lista = datos.get('id')
        nombre = datos.get('nombre')
        texto = datos.get('texto')
        db.modificar_lista(id_lista, nombre, texto) 
        return jsonify({"status": "success", "message": "Lista modificada con éxito"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

app.add_url_rule('/api/listas/modificar', 'api_modificar_la_lista', api_modificar_la_lista, methods=['POST'])
    
def index():
    return render_template('index.html')

def inicio_sesion():
    return render_template('inicio_sesion.html')

def registro():
    return render_template('registro.html')

def gestor():
    return render_template('gestor.html')

def listas():
    if 'usuario' not in session:
        return redirect(url_for('inicio_sesion'))
    nombre_usuario = session['usuario']
    listas_usuario = db.obtener_lista(nombre_usuario)
    return render_template('listas.html', listas=listas_usuario)

app.add_url_rule('/', 'index', index)
app.add_url_rule('/inicio_sesion', 'inicio_sesion', inicio_sesion)
app.add_url_rule('/registro', 'registro', registro)
app.add_url_rule('/gestor', 'gestor', gestor)
app.add_url_rule('/listas', 'listas', listas)

app.add_url_rule('/api/login', 'procesar_login', procesar_login, methods=['POST'])
app.add_url_rule('/api/registro', 'procesar_registro', procesar_registro, methods=['POST'])

app.run(debug=True)

