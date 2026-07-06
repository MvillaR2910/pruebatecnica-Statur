import argparse

from app import create_app, db
from app.models.ciudad import Ciudad
from app.models.departamento import Departamento
from app.models.usuario import Usuario

app = create_app()

DEPARTAMENTOS_Y_CIUDADES = [
    {
        "codigo": 5,
        "nombre": "Antioquia",
        "ciudades": [
            {"codigo": 5001, "nombre": "Medellín"},
            {"codigo": 5002, "nombre": "Bello"},
            {"codigo": 5004, "nombre": "Turbo"},
        ],
    },
    {
        "codigo": 8,
        "nombre": "Atlántico",
        "ciudades": [
            {"codigo": 8001, "nombre": "Barranquilla"},
            {"codigo": 8078, "nombre": "Baranoa"},
            {"codigo": 8088, "nombre": "Malambo"},
        ],
    },
    {
        "codigo": 11,
        "nombre": "Bogotá D.C.",
        "ciudades": [
            {"codigo": 11001, "nombre": "Bogotá D.C."},
        ],
    },
    {
        "codigo": 68,
        "nombre": "Santander",
        "ciudades": [
            {"codigo": 68001, "nombre": "Bucaramanga"},
            {"codigo": 68077, "nombre": "Barbosa"},
            {"codigo": 68679, "nombre": "San Gil"},
        ],
    },
    {
        "codigo": 76,
        "nombre": "Valle del Cauca",
        "ciudades": [
            {"codigo": 76001, "nombre": "Cali"},
            {"codigo": 76109, "nombre": "Buenaventura"},
            {"codigo": 76834, "nombre": "Tuluá"},
        ],
    },
]


def sembrar_departamentos_y_ciudades():
    for departamento_data in DEPARTAMENTOS_Y_CIUDADES:
        departamento = Departamento.query.get(departamento_data["codigo"])

        if departamento is None:
            departamento = Departamento(
                codigo_departamento=departamento_data["codigo"],
                nombre_departamento=departamento_data["nombre"],
            )
            db.session.add(departamento)
        else:
            departamento.nombre_departamento = departamento_data["nombre"]

        for ciudad_data in departamento_data["ciudades"]:
            ciudad = Ciudad.query.get(ciudad_data["codigo"])

            if ciudad is None:
                ciudad = Ciudad(
                    codigo_ciudad=ciudad_data["codigo"],
                    nombre_ciudad=ciudad_data["nombre"],
                    departamento_id=departamento_data["codigo"],
                )
                db.session.add(ciudad)
            else:
                ciudad.nombre_ciudad = ciudad_data["nombre"]
                ciudad.departamento_id = departamento_data["codigo"]


def sembrar_usuario_administrador(admin_user, admin_password):
    usuario = Usuario.query.filter_by(usuario=admin_user).first()
    if usuario is None:
        usuario = Usuario(usuario=admin_user)
        db.session.add(usuario)
    usuario.set_password(admin_password)


def inicializar_base_de_datos(reset=False, admin_user=None, admin_password=None):
    with app.app_context():
        if reset:
            db.drop_all()
        db.create_all()

        admin_user = admin_user or "admin"
        admin_password = admin_password or "admin123"

        sembrar_departamentos_y_ciudades()
        sembrar_usuario_administrador(admin_user, admin_password)
        db.session.commit()

        print(f"Usuario administrador listo: {admin_user}")
        print(
            f"Catálogo inicial cargado: {Departamento.query.count()} departamentos y "
            f"{Ciudad.query.count()} ciudades."
        )
        print("Base de datos creada correctamente")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--admin-user")
    parser.add_argument("--admin-password")
    args = parser.parse_args()
    inicializar_base_de_datos(
        reset=args.reset,
        admin_user=args.admin_user,
        admin_password=args.admin_password
    )
