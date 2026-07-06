from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para continuar."
login_manager.login_message_category = "warning"


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager.init_app(app)

    from app.models.usuario import Usuario
    from app.models.departamento import Departamento
    from app.models.ciudad import Ciudad
    from app.models.cliente import Cliente
    
    from app.routes.auth_routes import auth_bp
    from app.routes.cliente_routes import cliente_bp

    app.register_blueprint(auth_bp)

    app.register_blueprint(cliente_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models.usuario import Usuario
    return Usuario.query.get(int(user_id))
