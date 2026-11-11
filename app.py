from flask import Flask, render_template, request, redirect, url_for
from db import obtener_conexion

app = Flask(__name__)

# ----------------- INICIO / DASHBOARD -----------------
@app.route('/')
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM usuario")
    total_usuarios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM producto")
    total_productos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM venta")
    total_ventas = cursor.fetchone()[0]
    
    cursor.close()
    conexion.close()
    return render_template('index.html', u=total_usuarios, p=total_productos, v=total_ventas)

# ----------------- CRUD USUARIOS -----------------
@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        identificacion = request.form['identificacion']

        cursor.execute(
            "INSERT INTO usuario (nombre, correo, identificacion) VALUES (%s, %s, %s)",
            (nombre, correo, identificacion)
        )
        conexion.commit()
        return redirect(url_for('usuarios'))

    cursor.execute("SELECT * FROM usuario")
    lista_usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/usuarios/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        cursor.execute(
            "UPDATE usuario SET nombre=%s, correo=%s WHERE id_usuario=%s",
            (nombre, correo,  id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('usuarios'))

    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('usuarios'))

# ----------------- CRUD PRODUCTOS -----------------
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        fecha_entrada = request.form['fecha_entrada']

        cursor.execute(
            "INSERT INTO producto (nombre, categoria, cantidad, fecha_entrada) VALUES (%s, %s, %s, %s)",
            (nombre, categoria, cantidad, fecha_entrada)
        )
        conexion.commit()
        return redirect(url_for('productos'))

    cursor.execute("SELECT * FROM producto")
    lista_productos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template('productos.html', productos=lista_productos)

@app.route('/productos/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        fecha_entrada = request.form['fecha_entrada']

        cursor.execute(
            "UPDATE producto SET nombre=%s, categoria=%s, cantidad=%s, fecha_entrada=%s WHERE id_producto=%s",
            (nombre, categoria, cantidad, fecha_entrada, id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('productos'))

    cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()

    return render_template('editar_producto.html', producto=producto)

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id,))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        return redirect(url_for('productos'))
        
    except mysql.connector.Error as err:
        # Aquí atrapamos el error de la llave foránea y podemos avisarle al usuario
        print(f"Error al eliminar: {err}")
        return "No puedes eliminar este producto porque está asociado a una venta existente. Elimina primero la venta relacionada."

# ----------------- CRUD VENTAS -----------------
@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        fecha_venta = request.form['fecha_venta']
        metodo_pago = request.form['metodo_pago']
        total = request.form['total']
        id_usuario = request.form['id_usuario']
        id_producto = request.form['id_producto']

        cursor.execute(
            "INSERT INTO venta (fecha_venta, metodo_pago, total, id_usuario, id_producto) VALUES (%s, %s, %s, %s, %s)",
            (fecha_venta, metodo_pago, total, id_usuario, id_producto)
        )
        conexion.commit()
        return redirect(url_for('ventas'))

    cursor.execute("SELECT * FROM usuario")
    usuarios_select = cursor.fetchall()

    cursor.execute("SELECT * FROM producto")
    productos_select = cursor.fetchall()


    query_ventas = """
        SELECT v.id_venta, v.fecha_venta, v.metodo_pago, v.total, 
        u.nombre AS cliente, p.nombre AS producto 
        FROM venta v
        JOIN usuario u ON v.id_usuario = u.id_usuario
        JOIN producto p ON v.id_producto = p.id_producto
    """
    cursor.execute(query_ventas)
    lista_ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'ventas.html', 
        ventas=lista_ventas, 
        usuarios=usuarios_select, 
        productos=productos_select
    )

@app.route('/ventas/editar_venta/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    if request.method == 'POST':
        fecha_venta = request.form['fecha_venta']
        metodo_pago = request.form['metodo_pago']
        total = request.form['total']
        id_usuario = request.form['id_usuario']
        id_producto = request.form['id_producto']

        cursor.execute(
            "UPDATE venta SET fecha_venta=%s, metodo_pago=%s, total=%s, id_usuario=%s, id_producto=%s WHERE id_venta=%s",
            (fecha_venta, metodo_pago, total, id_usuario, id_producto, id)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for('ventas'))

    cursor.execute("SELECT * FROM usuario")
    usuarios_select = cursor.fetchall()

    cursor.execute("SELECT * FROM producto")
    productos_select = cursor.fetchall()


    cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (id,))
    venta = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        'editar_venta.html', 
        venta=venta, 
        usuarios=usuarios_select, 
        productos=productos_select
    )

@app.route('/ventas/eliminar/<int:id>')
def eliminar_venta(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM venta WHERE id_venta = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('ventas'))

if __name__ == '__main__':
    app.run(debug=True)