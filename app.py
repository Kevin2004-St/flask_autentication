from flask import Flask, render_template, request, session, redirect, flash,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "mi_clave_secreta_para_sesiones_123"

#proceso de inicio 
@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect("/login")
    
    usuario = session["usuario"]
    return render_template('dashboard.html', usuario= usuario )


#vista de registro
@app.route("/registro", methods=["GET"])
def registro():
    return render_template('registro.html');

#procesar registro
@app.route("/registrar", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]

    if not usuario or not contraseña:
        flash("Por favor llena todos los campos.")
        return redirect(url_for('registro'))
    
    try:
        with sqlite3.connect("usuarios.db") as conexion:          
         cursor = conexion.cursor()
         cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contraseña))
         conexion.commit()

        flash(f"¡Usuario {usuario}, registrado exitosamente!")
        return redirect(url_for('login'))
    
    except sqlite3.IntegrityError:
        flash("Ese nombre de usuario ya existe")
        return redirect(url_for('registro'))
    
    except Exception as e:
        flash(f"Error: {e}") 
        return redirect(url_for('registro'))

#vista de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]

    with sqlite3.connect("usuarios.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            session["usuario"] = usuario
            return redirect("/dashboard")
        else:
            flash("Credenciales incorrectas")
            return redirect(url_for('login'))
 
 
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
