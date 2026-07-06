from app import db


class Ciudad(db.Model):

    __tablename__ = "ciudades"

    codigo_ciudad = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre_ciudad = db.Column(
        db.String(100),
        nullable=False
    )

    departamento_id = db.Column(
        db.Integer,
        db.ForeignKey("departamentos.codigo_departamento"),
        nullable=False
    )

    departamento = db.relationship(
        "Departamento",
        back_populates="ciudades"
    )

    clientes = db.relationship(
        "Cliente",
        back_populates="ciudad",
        lazy=True
    )
