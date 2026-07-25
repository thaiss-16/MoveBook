import sqlite3

#INIT DE LAS BASES DE DATOS
def init_db():
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id_tarea INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                inicio TEXT NOT NULL,
                fin TEXT NOT NULL,
                color_fondo TEXT NOT NULL,
                id_usuario INTEGER REFERENCES usuarios(id_usuario)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listas (
                id_lista INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                texto TEXT,
                usuario TEXT NOT NULL,
                id_usuario INTEGER REFERENCES usuarios(id_usuario)
            )
        ''')
        
        conn.commit()


#LOGIN Y REGISTRO
def agregar_usuario(usuario, contrasena):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena))
        conn.commit()

def verificar_usuario(usuario, contrasena):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, usuario FROM usuarios WHERE usuario = ? AND contrasena = ?', (usuario, contrasena))
        fila= cursor.fetchone()
        return fila
    
def existe_usuario(usuario):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
        return cursor.fetchone() is not None
    

#CALENDARIO
def agregar_tarea(titulo, categoria, inicio, fin, color_fondo, id_usuario):
    """Corregido para coincidir con las columnas reales de la tabla tareas"""
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tareas (titulo, categoria, inicio, fin, color_fondo, id_usuario) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (titulo, categoria, inicio, fin, color_fondo, id_usuario))
        conn.commit()

def obtener_tareas(id_usuario):
    with sqlite3.connect('db/database.db') as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute('SELECT id_tarea, titulo, categoria, inicio, fin, color_fondo FROM tareas WHERE id_usuario = ?', (id_usuario,))

        tareas = []
        for row in cursor.fetchall():
            tareas.append({
                "id": str(row["id_tarea"]),
                "calendarId": "cal1", 
                "title": row["titulo"],
                "category": row["categoria"],
                "start": row["inicio"],    
                "end": row["fin"],
                "backgroundColor": row["color_fondo"]
            })
        return tareas
    
def eliminar_tarea(id_tarea):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tareas WHERE id_tarea = ?', (id_tarea,))
        conn.commit()

def modificar_tarea(id_tarea, nuevo_titulo, nueva_categoria, nuevo_inicio, nuevo_fin, nuevo_color):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tareas 
            SET titulo = ?, categoria = ?, inicio = ?, fin = ?, color_fondo = ? 
            WHERE id_tarea = ?
        ''', (nuevo_titulo, nueva_categoria, nuevo_inicio, nuevo_fin, nuevo_color, id_tarea))
        conn.commit()


#LISTAS
def agregar_lista(nombre, texto, usuario):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO listas (nombre, texto, usuario) VALUES (?, ?, ?)', (nombre, texto, usuario))
        conn.commit()

def obtener_lista(usuario):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_lista, nombre FROM listas WHERE usuario = ?', (usuario,))
        return cursor.fetchall()
    
def eliminar_lista(lista_id):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM listas WHERE id_lista = ?', (lista_id,))
        conn.commit()

def modificar_lista(lista_id, nuevo_nombre, nuevo_texto):
    with sqlite3.connect('db/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE listas SET nombre = ?, texto = ? WHERE id_lista = ?', (nuevo_nombre, nuevo_texto, lista_id))
        conn.commit()