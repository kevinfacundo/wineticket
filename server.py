# Módulos y librerías necesarias
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import qrcode
import mysql.connector
import io
import base64
from flask import send_file
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user



# Inicialización Flask
app = Flask(__name__)
load_dotenv()



# Configuración de la base de datos MySQL
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')



# Inicialización de MySQL
mysql = MySQL(app)



# Configurar la carpeta donde se guardan los QR generados
QR_FOLDER = 'static/qr_codes'



# Configuración de Flask-Login
app.secret_key = "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."



# Clase de modelo de usuario
class User(UserMixin):
    def __init__(self, id, nombre, apellido, email, password, pais, provincia, rol, fecha_registro):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
        self.pais = pais
        self.provincia = provincia
        self.rol = rol
        self.fecha_registro = fecha_registro



# Carga de usuario para FLASK-LOGIN
@login_manager.user_loader
def load_user(user_id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])
    return None



# Ruta de INICIO
@app.route('/inicio')
@login_required
def inicio():
    return render_template('index.html')



# RUTAS EVENTOS DESTACADOS (eventos dentro del carrusel)

# Ruta evento Vendimia 2024
@app.route('/vendimia')
@login_required
def vendimia():
    return render_template('eventos_destacados/vendimia.html')

# Ruta evento Vino el cine
@app.route('/vino_el_cine')
@login_required
def vino_el_cine():
    return render_template('eventos_destacados/vino_el_cine.html')

# Ruta evento Expo wine Hilton
@app.route('/expo_wine_hilton')
@login_required
def expo_wine_hilton():
    return render_template('eventos_destacados/expo_wine_hilton.html')

# RUTAS OTROS EVENTOS

# Ruta evento Sunset bodega Lopez
@app.route('/sunset_bodega_lopez')
def sunset_bodega_lopez():
    return render_template('otros_eventos/sunset_lopez.html')

@app.route('/valentino_bodega_septima')
def valentino_bodega_septima():
    return render_template('otros_eventos/valentino_bodega_septima.html')

@app.route('/degustacion_wine_bar')
def degustacion_wine_bar():
    return render_template('otros_eventos/degustacion_wine_bar.html')

@app.route('/cine_frances_bodega_atamisque')
def cine_atamisque():
    return render_template('otros_eventos/cine_atamisque.html')



# Ruta MIS RESEÑAS para ver, agregar y eliminar reseñas
@app.route('/mis_reseñas', methods=['GET', 'POST'])
@login_required
def mis_reseñas():
    if request.method == 'POST':
        if 'comentario' in request.form:  # Si es una solicitud para agregar una reseña
            comentario = request.form['comentario']
            
            # Insertar la nueva reseña en la base de datos
            with mysql.connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO reseñas (usuario_id, comentario, fecha)
                    VALUES (%s, %s, NOW())
                """, (current_user.id, comentario))
                mysql.connection.commit()
            flash("Reseña agregada exitosamente", "success")
            return redirect(url_for('mis_reseñas'))
        
        elif 'eliminar_reseña' in request.form:  # Si es una solicitud para eliminar una reseña
            reseña_id = request.form['eliminar_reseña']
            
            # Eliminar la reseña de la base de datos
            with mysql.connection.cursor() as cur:
                cur.execute("""
                    DELETE FROM reseñas WHERE id = %s AND usuario_id = %s
                """, (reseña_id, current_user.id))
                mysql.connection.commit()
            flash("Reseña eliminada exitosamente", "success")
            return redirect(url_for('mis_reseñas'))
    
    # Recuperar las reseñas del usuario logueado
    with mysql.connection.cursor() as cur:
        cur.execute("""
            SELECT id, comentario, fecha FROM reseñas 
            WHERE usuario_id = %s ORDER BY fecha DESC
        """, (current_user.id,))
        reseñas = cur.fetchall()
    
    return render_template('mis_reseñas.html', reseñas=reseñas)



# Ruta GENERAR Y ALMACENAR QR
@app.route('/comprar_tickets', methods=['GET', 'POST'])
@login_required
def comprar_tickets():
    if request.method == 'POST':
        # Obtener la información de la compra
        cantidad = request.form['cantidad_entradas']
        tipo = request.form['types_tickets']
        metodo_pago = request.form['metodo_pago']
        
        # Insertar la compra en la tabla `compras` (sin QR aún)
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO compras (usuario_id, evento_id, cantidad, codigo_qr, fecha_compra, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_user.id, None, cantidad, '', datetime.now(), current_user.id))
        mysql.connection.commit()

        # Obtener el id de la compra recién creada
        compra_id = cur.lastrowid

        # Generar el código QR
        url = f"http://localhost:5000/detalle_compra/{compra_id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_bytes = buffered.getvalue()
        qr_code_str = base64.b64encode(qr_code_bytes).decode("utf-8")

        # Almacenar el QR en la tabla `qr_codes`
        cur.execute("INSERT INTO qr_codes (compra_id, codigo) VALUES (%s, %s)", (compra_id, qr_code_str))
        mysql.connection.commit()
        cur.close()

        # Guardar el archivo QR para descarga
        qr_path = os.path.join('static', 'qr_codes', f'qr_code_{compra_id}.png')
        with open(qr_path, 'wb') as f:
            f.write(qr_code_bytes)

        flash('Compra realizada exitosamente y QR generado.', 'success')
        return redirect(url_for('confirmar_compra', compra_id=compra_id))

    return render_template('compras_tickets/comprar_tickets.html')



# Ruta DESCARGAR QR
@app.route('/confirmar_compra/<int:compra_id>')
@login_required
def confirmar_compra(compra_id):
    # Proporcionar la ruta del QR para la descarga
    qr_path = os.path.join('static', 'qr_codes', f'qr_code_{compra_id}.png')
    return render_template('compra_confirmada.html', qr_path=qr_path, compra_id=compra_id)



# Ruta VOLVER A DESCARGAR QR
@app.route('/descargar_qr/<int:compra_id>')
@login_required
def descargar_qr(compra_id):
    # Ruta del archivo QR
    qr_path = os.path.join('static', 'qr_codes', f'qr_code_{compra_id}.png')
    if os.path.exists(qr_path):
        return send_file(qr_path, as_attachment=True, download_name=f'qr_code_{compra_id}.png')
    else:
        flash('El archivo QR no existe.', 'danger')
        return redirect(url_for('mis_tickets'))



# Ruta MIS TICKETS
@app.route('/mis_tickets')
@login_required
def mis_tickets():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT compras.id, qr_codes.codigo 
        FROM compras 
        JOIN qr_codes ON compras.id = qr_codes.compra_id
        WHERE compras.usuario_id = %s
    """, (current_user.id,))
    tickets = cur.fetchall()  # Debe devolver una lista de tuplas con id y codigo
    cur.close()
    return render_template('mis_tickets.html', tickets=tickets)



# Ruta MI PERFIL
@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')



# Ruta crear usuarios en USUARIOS
@app.route('/crear_usuarios', methods=['GET', 'POST'])
@login_required
def crear_usuarios():
    print(f"Current User: {current_user}")  # Depuración
    if current_user.rol != 'admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        pais = request.form['pais']
        provincia = request.form['provincia']
        rol = request.form.get('rol', 'user')  # Rol predeterminado

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO usuarios (nombre, apellido, email, password, pais, provincia, rol, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())",
                            (nombre, apellido, email, password, pais, provincia, rol))
                mysql.connection.commit()
            flash("Usuario creado exitosamente", "success")
            return redirect(url_for('usuarios'))
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            flash("Error al crear el usuario", "error")

    return render_template('crear_usuarios.html')



# Ruta editar usuarios en USUARIOS
@app.route('/edit_usuarios/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_usuarios(id):
    if current_user.rol != 'admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('usuarios'))  # Redirige directamente a usuarios

    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cur.fetchone()
    
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('usuarios'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        pais = request.form['pais']
        provincia = request.form['provincia']
        rol = request.form['rol']

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("""UPDATE usuarios 
                               SET nombre = %s, apellido = %s, email = %s, pais = %s, provincia = %s, rol = %s 
                               WHERE id = %s""", 
                            (nombre, apellido, email, pais, provincia, rol, id))
                mysql.connection.commit()
            flash("Usuario actualizado exitosamente", "success")
            return redirect(url_for('usuarios'))  # Redirige a la lista de usuarios después de la edición
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            flash("Error al actualizar el usuario", "error")

    return render_template('edit_usuarios.html', usuario=usuario)



# Ruta para eliminar usuarios solo para admin
@app.route('/eliminar_usuarios/<int:id>', methods=['POST'])
@login_required
def eliminar_usuarios(id):
    if current_user.rol != 'admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('inicio'))

    try:
        with mysql.connection.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            mysql.connection.commit()
        flash("Usuario eliminado exitosamente", "success")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        flash("Error al eliminar el usuario", "error")

    return redirect(url_for('usuarios'))  



# Ruta TABLA USUARIOS solo para admins
@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.rol != 'admin':  # Verifica si el usuario no es admin
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('inicio'))
    
    # Consulta para obtener todos los usuarios de la base de datos
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
    
    return render_template('usuarios.html', usuarios=usuarios)



# Ruta de LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Verificar si el usuario ya está autenticado
        return redirect(url_for('inicio'))  # Redirige al inicio si ya está logueado

    error_message = None  # Inicia la variable para el mensaje de error

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()

            if user:  # Si se encuentra el usuario con ese email
                if user[4] == password:  # Si la contraseña es correcta
                    user_obj = User(*user)
                    login_user(user_obj)
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('inicio'))
                else:
                    error_message = "Credenciales inválidas. Por favor, inténtalo de nuevo."  # Contraseña incorrecta
            else:
                error_message = "Usuario no registrado. Por favor, regístrate."  # Usuario no encontrado

    return render_template('login.html', error_message=error_message)



# Ruta de REGISTRO
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        pais = request.form.get('pais')
        provincia = request.form.get('provincia')
        rol = 'user'

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("INSERT INTO usuarios (nombre, apellido, email, password, pais, provincia, rol, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())",
                            (nombre, apellido, email, password, pais, provincia, rol))
                mysql.connection.commit()
            flash('¡Registro exitoso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error al registrar usuario en la base de datos: {str(e)}")
            flash('Error al registrar usuario', 'error')
    return render_template('register.html')



# Ruta de LOGOUT
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()  # Cierra la sesión
        flash('Has cerrado sesión', 'info')  # Muestra un mensaje
        return redirect(url_for('login'))  # Redirige al login
    return redirect(url_for('inicio'))  # Si es un GET, redirige a la página principal



# Levanta el server
if __name__ == '__main__':
    app.run(port=5000, debug=True)