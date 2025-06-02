from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "mi_clave_secreta_para_sesiones_123"

#vista de inicio 
@app.route("/")
def inicio():
    if "usuario" in session:
        return f"Hola, {session['usuario']}!  <a href='/logout'>Cerrar sesión</a>"
    return "Bienvenido. <a href='/registro'>Registrarse</a> |  <a href='/login'>Iniciar sesion</a>"

#vista de registro
@app.route("/registro")
def registro():
    return render_template('registro.html');

#procesar registro
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

#vista de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]

    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ? ", (usuario,contraseña))
    resulado = cursor.fetchone()
    conexion.close()

    if resulado:
        session["usuario"] = usuario
        return redirect("/")
    else:
        return "Credenciales incorrectas.  <a href='/login'>Intenta de nuevo</a> "
 
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
