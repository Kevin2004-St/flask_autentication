import sqlite3

#Conectar con la base de datos, sino existe la crea
conexion = sqlite3.connect('usuarios.db')

#Cursor para comando sql
cursor = conexion.cursor();

#Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contraseña TEXT NOT NULL
)
""")

#Guardar y cerrar
conexion.commit()
conexion.close()

print('Base de datos creada correctamente')