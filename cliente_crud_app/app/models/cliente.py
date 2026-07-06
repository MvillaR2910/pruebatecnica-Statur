from app import db


class Cliente(db.Model):

    __tablename__ = "clientes"

    documento_identidad = db.Column(
        db.String(20),
        primary_key=True
    )

    nombres = db.Column(
        db.String(100),
        nullable=False
    )

    apellidos = db.Column(
        db.String(100),
        nullable=False
    )

    departamento_id = db.Column(
        db.Integer,
        db.ForeignKey("departamentos.codigo_departamento"),
        nullable=False
    )

    ciudad_id = db.Column(
        db.Integer,
        db.ForeignKey("ciudades.codigo_ciudad"),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    telefono = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    creado_por_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    departamento = db.relationship(
        "Departamento",
        back_populates="clientes"
    )

    ciudad = db.relationship(
        "Ciudad",
        back_populates="clientes"
    )

    creado_por = db.relationship(
        "Usuario",
        back_populates="clientes"
    )
