from flask import Flask, render_template, request, session, redirect, flash,url_for
import sqlite3, bcrypt

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
    return render_template('dashboard.html', usuario= usuario)


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
        contrasena_hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with sqlite3.connect("usuarios.db") as conexion:          
         cursor = conexion.cursor()
         cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario,  contrasena_hashed))
         conexion.commit()

        flash(f"¡Usuario {usuario}, registrado exitosamente!")
        return redirect(url_for('login'))
    
    except sqlite3.IntegrityError:
        flash("Ese nombre de usuario ya existe")
        return redirect(url_for('registro'))
    
    except Exception as e:
        flash(f"Error: {e}") 
        return redirect(url_for('registro'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        import random
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        valor = num1 + num2
        return render_template('login.html', num1=num1, num2=num2, valor=valor)

    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]
    captcha = request.form["captcha"]
    valor = request.form["valor"]

    if not usuario or not contraseña or not captcha:
        flash("Por favor completa todos los campos.")
        return redirect(url_for('login'))

    if int(captcha) != int(valor):
        flash("Captcha incorrecto")
        return redirect(url_for('login'))

    with sqlite3.connect("usuarios.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()

    if resultado:
        contraseña_dba = resultado[2]
        if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_dba.encode('utf-8')):
            session["usuario"] = usuario
            return redirect("/dashboard")

    flash("Credenciales incorrectas")
    return redirect(url_for('login'))

 
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
