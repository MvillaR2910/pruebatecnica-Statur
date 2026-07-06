from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    usuario = db.Column(db.String(100), unique=True, nullable=False)

    contrasena_hash = db.Column(db.String(255), nullable=False)

    clientes = db.relationship(
        "Cliente",
        back_populates="creado_por",
        lazy=True
    )

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

    def get_id(self):
        return str(self.id)
