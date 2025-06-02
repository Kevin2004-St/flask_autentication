from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)

@app.route("/")
def inicio():
    if "usuario" in session:
        return f"Hola, {session['usuario']}!  <a href='/logout'>Cerrar sesión</a>"
    return "Bienvenido. <a href='/registro'>Registrarse</a> |  <a href='/login'>Iniciar sesion</a>"

@app.route("/registro")
def registro():
    return render_template('registro.html');

@app.route("/registrar", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]

    if not usuario or not contraseña:
        return 'Por favor llena todos los campos.'
    
    try:
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contraseña))
        conexion.commit()
        conexion.close()
        return f"!Usuario {usuario} registrado exitosamente!"
    except sqlite3.IntegrityError:
        return "Ese nombre de usuario ya existe."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)
