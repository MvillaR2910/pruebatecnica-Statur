# Aplicativo de Gestión de Clientes

Aplicación web construida con `Flask`, `SQLite`, `SQLAlchemy` y `Flask-Login` para la gestión de clientes, autenticación de usuarios y control de acceso por propietario de registros.

## Funcionalidades

- Inicio de sesión con validación de credenciales.
- Registro de nuevos usuarios.
- Carga inicial de usuario administrador, departamentos y ciudades.
- Registro de clientes.
- Consulta de todos los clientes registrados.
- Edición y eliminación solo para clientes creados por el usuario autenticado.
- Validaciones de unicidad para:
  - documento de identidad
  - correo electrónico
  - número de celular

## Tecnologías

- `Python`
- `Flask`
- `Flask-SQLAlchemy`
- `Flask-Login`
- `SQLite`
- `HTML`
- `CSS`
- `Jinja2`

## Estructura principal

```text
cliente_crud_app/
|- app/
|  |- models/
|  |- routes/
|  |- static/
|  `- templates/
|- config.py
|- crear_bd.py
|- database.db
|- requirements.txt
`- run.py
```

## Requisitos previos

- `Python 3.11` o superior
- `pip`

## Instalación y ejecución

### 1. Entrar al proyecto

```powershell
cd .\cliente_crud_app
```

### 2. Crear entorno virtual

```powershell
python -m venv venv
```

### 3. Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```powershell
pip install -r .\requirements.txt
```

### 5. Crear la base de datos y cargar datos iniciales

```powershell
python .\crear_bd.py --reset
```

Este comando:

- crea o recrea la base de datos
- crea el usuario administrador
- carga departamentos y ciudades base

### 6. Ejecutar la aplicación

```powershell
python .\run.py
```

La aplicación queda disponible en:

```text
http://127.0.0.1:5000
```

## Credenciales por defecto

- Usuario: `admin`
- Contraseña: `admin123`

## Registro de nuevos usuarios

Además del usuario administrador, cualquier persona puede registrarse desde la ruta:

```text
/registro
```

Los usuarios registrados pueden:

- iniciar sesión
- ver todos los clientes
- crear sus propios clientes
- editar y eliminar únicamente los clientes creados por ellos mismos

## Reglas de negocio implementadas

### Usuarios

- el nombre de usuario no puede repetirse
- la contraseña se almacena con hash seguro

### Clientes

- `documento_identidad` es único
- `email` es único
- `telefono` es único
- un cliente debe pertenecer a un departamento y a una ciudad válidos
- la ciudad seleccionada debe pertenecer al departamento seleccionado
- solo el creador del cliente puede editarlo o eliminarlo

## Datos iniciales cargados

Se cargan automáticamente:

- 1 usuario administrador
- 5 departamentos
- 13 ciudades

## Cómo probar la aplicación

### Flujo 1: autenticación

1. Ir a `http://127.0.0.1:5000`
2. Iniciar sesión con `admin / admin123`
3. Cerrar sesión
4. Registrar un nuevo usuario en `/registro`
5. Iniciar sesión con el nuevo usuario

### Flujo 2: CRUD de clientes

1. Crear un cliente nuevo
2. Verificar que aparece en el listado
3. Editar el cliente
4. Eliminar el cliente

### Flujo 3: restricciones por usuario

1. Iniciar sesión con `admin`
2. Crear un cliente
3. Cerrar sesión
4. Entrar con otro usuario
5. Verificar que el cliente creado por `admin` sí se visualiza
6. Verificar que para ese cliente solo aparece el estado `Solo lectura`
7. Intentar editar o eliminar manualmente por URL y confirmar que el sistema lo bloquea

### Flujo 4: validaciones

Probar que el sistema rechaza:

- documento repetido
- correo repetido
- celular repetido
- campos vacíos
- ciudad que no pertenezca al departamento seleccionado

## Script de inicialización

También puedes crear la base con usuario personalizado:

```powershell
python .\crear_bd.py --reset --admin-user miadmin --admin-password miclave123
```

## Base de datos

El proyecto usa `SQLite` y guarda el archivo en:

```text
database.db
```

La inicialización del esquema y de los datos base se realiza desde:

```text
crear_bd.py
```

Además, el proyecto incluye el archivo:

```text
schema.sql
```

Este archivo contiene:

- creación de tablas
- llaves primarias y foráneas
- usuario administrador inicial
- departamentos y ciudades base

### Opciones de entrega para la empresa

La empresa puede levantar la base de datos de cualquiera de estas dos formas:

- **Opción 1: usando ORM**
  - `python .\crear_bd.py --reset`
- **Opción 2: usando SQL**
  - importar `schema.sql` en SQLite

La opción recomendada para este proyecto es `crear_bd.py`, porque mantiene el flujo exacto del entorno de desarrollo.

## Nota sobre UTF-8 en PowerShell

Si en la terminal ves textos raros como `GestiÃ³n` o `ContraseÃ±a`, ejecuta esto antes de leer archivos:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

## Observaciones

- Si ya existe una base anterior y cambió el modelo, se recomienda ejecutar `python .\crear_bd.py --reset`.
- La interfaz sigue la paleta solicitada: negro, blanco y naranja.
- El proyecto fue pensado para ejecutarse localmente en entorno de desarrollo.

## Autor

Prueba técnica desarrollada por `Mateo Villa Rojo`.
