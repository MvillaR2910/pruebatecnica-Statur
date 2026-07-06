from app import db


class Departamento(db.Model):

    __tablename__ = "departamentos"

    codigo_departamento = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre_departamento = db.Column(
        db.String(100),
        nullable=False
    )

    ciudades = db.relationship(
        "Ciudad",
        back_populates="departamento",
        cascade="all, delete-orphan",
        lazy=True
    )

    clientes = db.relationship(
        "Cliente",
        back_populates="departamento",
        lazy=True
    )
