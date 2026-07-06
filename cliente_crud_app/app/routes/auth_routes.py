from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("cliente.panel_clientes"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("cliente.panel_clientes"))

    if request.method == "POST":
        usuario_ingresado = request.form.get("usuario", "").strip()
        password_ingresado = request.form.get("contrasena", "")

        usuario = Usuario.query.filter_by(usuario=usuario_ingresado).first()

        if usuario and usuario.check_password(password_ingresado):
            login_user(usuario)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("cliente.panel_clientes"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("cliente.panel_clientes"))

    if request.method == "POST":
        usuario_ingresado = request.form.get("usuario", "").strip()
        password_ingresado = request.form.get("contrasena", "")
        confirmar_password = request.form.get("confirmar_contrasena", "")

        if not usuario_ingresado or not password_ingresado or not confirmar_password:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("auth/register.html")

        if len(usuario_ingresado) < 4:
            flash("El usuario debe tener al menos 4 caracteres.", "danger")
            return render_template("auth/register.html")

        if len(password_ingresado) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
            return render_template("auth/register.html")

        if password_ingresado != confirmar_password:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("auth/register.html")

        usuario_existente = Usuario.query.filter_by(usuario=usuario_ingresado).first()
        if usuario_existente:
            flash("Ese nombre de usuario ya está en uso.", "danger")
            return render_template("auth/register.html")

        nuevo_usuario = Usuario(usuario=usuario_ingresado)
        nuevo_usuario.set_password(password_ingresado)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
