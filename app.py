import os
from decimal import Decimal, InvalidOperation

import pymysql
from flask import Flask, request, jsonify, render_template, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "false").lower() == "true",
)

def get_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        autocommit=True,
    )

@app.get("/health")
def health():
    try:
        connection = get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        finally:
            connection.close()

        return jsonify(
            status="ok",
            cliente="Vidri",
            runtime="Python Flask",
            database="MySQL",
            databaseConnection="connected",
        )
    except Exception:
        return jsonify(status="error", databaseConnection="disconnected"), 503

@app.get("/")
def login_page():
    return render_template("login.html")

@app.get("/dashboard")
def dashboard():
    if "user_id" not in session:
        return render_template("login.html"), 401
    return render_template("dashboard.html")

@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario", "")
    password = data.get("password", "")

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, usuario, password_hash FROM usuarios WHERE usuario=%s",
                (usuario,),
            )
            user = cursor.fetchone()
    finally:
        connection.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify(error="Credenciales incorrectas"), 401

    session.clear()
    session["user_id"] = user["id"]
    session["usuario"] = user["usuario"]

    return jsonify(mensaje="Autenticación exitosa")

@app.get("/api/session")
def current_session():
    if "user_id" not in session:
        return jsonify(authenticated=False), 401

    return jsonify(authenticated=True, usuario=session["usuario"])

@app.get("/api/productos")
def productos():
    if "user_id" not in session:
        return jsonify(error="No autorizado"), 401

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY id")
            result = cursor.fetchall()
    finally:
        connection.close()

    for producto in result:
        producto["precio"] = float(producto["precio"])

    return jsonify(result)

@app.post("/api/productos")
def crear_producto():
    if "user_id" not in session:
        return jsonify(error="No autorizado"), 401

    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()

    try:
        precio = Decimal(str(data.get("precio", "")))
    except InvalidOperation:
        return jsonify(error="Precio inválido"), 400

    if not nombre or len(nombre) > 150 or not precio.is_finite() or precio < 0:
        return jsonify(error="Datos inválidos"), 400

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos(nombre, precio) VALUES(%s, %s)",
                (nombre, str(precio)),
            )
            producto_id = cursor.lastrowid
    finally:
        connection.close()

    return jsonify(id=producto_id, nombre=nombre, precio=float(precio)), 201


@app.put("/api/productos/<int:producto_id>")
def actualizar_producto(producto_id):

    if "user_id" not in session:
        return jsonify(error="No autorizado"), 401

    if producto_id <= 0:
        return jsonify(error="ID inválido"), 400

    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()

    try:
        precio = Decimal(str(data.get("precio", "")))
    except InvalidOperation:
        return jsonify(error="Precio inválido"), 400

    if (
        not nombre
        or len(nombre) > 150
        or not precio.is_finite()
        or precio < 0
    ):
        return jsonify(error="Datos inválidos"), 400

    connection = get_db()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM productos
                WHERE id = %s
                """,
                (producto_id,)
            )

            if not cursor.fetchone():
                return jsonify(
                    error="Producto no encontrado"
                ), 404

            cursor.execute(
                """
                UPDATE productos
                SET nombre = %s, precio = %s
                WHERE id = %s
                """,
                (nombre, str(precio), producto_id)
            )

    finally:
        connection.close()

    return jsonify(
        mensaje="Producto actualizado correctamente",
        producto={
            "id": producto_id,
            "nombre": nombre,
            "precio": float(precio)
        }
    )






@app.delete("/api/productos/<int:producto_id>")
def eliminar_producto(producto_id):

    if "user_id" not in session:
        return jsonify(error="No autorizado"), 401

    if producto_id <= 0:
        return jsonify(error="ID inválido"), 400

    connection = get_db()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM productos
                WHERE id = %s
                """,
                (producto_id,)
            )

            eliminados = cursor.rowcount

    finally:
        connection.close()

    if eliminados == 0:
        return jsonify(
            error="Producto no encontrado"
        ), 404

    return jsonify(
        mensaje="Producto eliminado correctamente",
        id=producto_id
    )





@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(mensaje="Sesión cerrada")
