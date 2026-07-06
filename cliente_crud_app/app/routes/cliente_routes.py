from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.models.ciudad import Ciudad
from app.models.cliente import Cliente
from app.models.departamento import Departamento

cliente_bp = Blueprint('cliente', __name__)


def _obtener_catalogos():
    departamentos = Departamento.query.order_by(Departamento.nombre_departamento.asc()).all()
    ciudades = Ciudad.query.order_by(Ciudad.nombre_ciudad.asc()).all()
    return departamentos, ciudades

def _obtener_valores_formulario():
    return {
        "documento_identidad": request.form.get("documento_identidad", "").strip(),
        "nombres": request.form.get("nombres", "").strip(),
        "apellidos": request.form.get("apellidos", "").strip(),
        "departamento_id": request.form.get("departamento_id", "").strip(),
        "ciudad_id": request.form.get("ciudad_id", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "telefono": request.form.get("telefono", "").strip(),
    }


def _validar_cliente_formulario(datos, cliente_actual=None):
    campos_requeridos = [
        "documento_identidad",
        "nombres",
        "apellidos",
        "departamento_id",
        "ciudad_id",
        "email",
        "telefono",
    ]

    if any(not datos[campo] for campo in campos_requeridos):
        return "Todos los campos son obligatorios.", None, None

    try:
        departamento_id = int(datos["departamento_id"])
        ciudad_id = int(datos["ciudad_id"])
    except ValueError:
        return "Departamento y ciudad deben ser válidos.", None, None

    departamento = Departamento.query.get(departamento_id)
    ciudad = Ciudad.query.get(ciudad_id)

    if departamento is None:
        return "El departamento seleccionado no existe.", None, None

    if ciudad is None:
        return "La ciudad seleccionada no existe.", None, None

    if ciudad.departamento_id != departamento.codigo_departamento:
        return "La ciudad no pertenece al departamento seleccionado.", None, None

    consulta_duplicados = Cliente.query.filter(
        or_(
            Cliente.documento_identidad == datos["documento_identidad"],
            Cliente.email == datos["email"],
            Cliente.telefono == datos["telefono"],
        )
    )

    if cliente_actual is not None:
        consulta_duplicados = consulta_duplicados.filter(
            Cliente.documento_identidad != cliente_actual.documento_identidad
        )

    cliente_duplicado = consulta_duplicados.first()
    if cliente_duplicado:
        if cliente_duplicado.documento_identidad == datos["documento_identidad"]:
            return "Ya existe un cliente con ese documento.", None, None
        if cliente_duplicado.telefono == datos["telefono"]:
            return "Ya existe un cliente con ese número de celular.", None, None
        return "Ya existe un cliente con ese correo electrónico.", None, None

    return None, departamento, ciudad


@cliente_bp.route("/clientes")
@login_required
def panel_clientes():
    clientes = Cliente.query.order_by(Cliente.nombres.asc(), Cliente.apellidos.asc()).all()
    return render_template("clientes/index.html", clientes=clientes)


@cliente_bp.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def crear_cliente():
    departamentos, ciudades = _obtener_catalogos()

    if not departamentos or not ciudades:
        flash("Debes cargar departamentos y ciudades antes de registrar clientes.", "warning")
        return redirect(url_for("cliente.panel_clientes"))

    if request.method == "POST":
        datos = _obtener_valores_formulario()
        error, _, _ = _validar_cliente_formulario(datos)

        if error:
            flash(error, "danger")
            return render_template(
                "clientes/form.html",
                cliente=None,
                departamentos=departamentos,
                ciudades=ciudades,
                form_data=datos,
                accion="crear",
            )

        cliente = Cliente(
            documento_identidad=datos["documento_identidad"],
            nombres=datos["nombres"],
            apellidos=datos["apellidos"],
            departamento_id=int(datos["departamento_id"]),
            ciudad_id=int(datos["ciudad_id"]),
            email=datos["email"],
            telefono=datos["telefono"],
            creado_por_id=current_user.id,
        )
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("cliente.panel_clientes"))

    return render_template(
        "clientes/form.html",
        cliente=None,
        departamentos=departamentos,
        ciudades=ciudades,
        form_data={},
        accion="crear",
    )


@cliente_bp.route("/clientes/<string:documento_identidad>/editar", methods=["GET", "POST"])
@login_required
def editar_cliente(documento_identidad):
    cliente = Cliente.query.get_or_404(documento_identidad)

    if cliente.creado_por_id != current_user.id:
        flash("No puedes editar este cliente porque fue creado por otro usuario.", "warning")
        return redirect(url_for("cliente.panel_clientes"))

    departamentos, ciudades = _obtener_catalogos()

    if request.method == "POST":
        datos = _obtener_valores_formulario()
        datos["documento_identidad"] = cliente.documento_identidad
        error, _, _ = _validar_cliente_formulario(datos, cliente_actual=cliente)

        if error:
            flash(error, "danger")
            return render_template(
                "clientes/form.html",
                cliente=cliente,
                departamentos=departamentos,
                ciudades=ciudades,
                form_data=datos,
                accion="editar",
            )

        cliente.nombres = datos["nombres"]
        cliente.apellidos = datos["apellidos"]
        cliente.departamento_id = int(datos["departamento_id"])
        cliente.ciudad_id = int(datos["ciudad_id"])
        cliente.email = datos["email"]
        cliente.telefono = datos["telefono"]
        db.session.commit()
        flash("Cliente actualizado correctamente.", "success")
        return redirect(url_for("cliente.panel_clientes"))

    form_data = {
        "documento_identidad": cliente.documento_identidad,
        "nombres": cliente.nombres,
        "apellidos": cliente.apellidos,
        "departamento_id": str(cliente.departamento_id),
        "ciudad_id": str(cliente.ciudad_id),
        "email": cliente.email,
        "telefono": cliente.telefono,
    }
    return render_template(
        "clientes/form.html",
        cliente=cliente,
        departamentos=departamentos,
        ciudades=ciudades,
        form_data=form_data,
        accion="editar",
    )


@cliente_bp.route("/clientes/<string:documento_identidad>/eliminar", methods=["POST"])
@login_required
def eliminar_cliente(documento_identidad):
    cliente = Cliente.query.get_or_404(documento_identidad)

    if cliente.creado_por_id != current_user.id:
        flash("No puedes eliminar este cliente porque fue creado por otro usuario.", "warning")
        return redirect(url_for("cliente.panel_clientes"))

    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("cliente.panel_clientes"))
