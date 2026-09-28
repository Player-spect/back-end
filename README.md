# Gestión Corporativa

Aplicación web desarrollada con **Django** para la gestión de información de una organización. El proyecto utiliza una base de datos relacional MySQL y Django ORM para la persistencia y consulta de los datos.

## Objetivo

Transformar la información que inicialmente se encontraba almacenada en archivos JSON en una solución web basada en una base de datos relacional, permitiendo administrar las entidades mediante **Django Admin** y visualizar la información desde la aplicación web.

## Tecnologías

- Python
- Django 6.1.1
- MySQL
- mysqlclient
- python-dotenv
- HTML
- Bootstrap
- Git / GitHub

## Estructura del proyecto

```text
Gestion/
├── gestion_corporativa/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── recursos_humanos/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── operaciones/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── recursos_humanos/
│   └── operaciones/
├── static/
├── data.json
├── loader.py
├── manage.py
├── requirements.txt
├── .env
└── .gitignore
```

## Aplicaciones

### Recursos Humanos

Esta aplicación administra:

- **Department:** departamentos de la organización.
- **Employee:** empleados y su departamento asociado.

Relación:

```text
Department 1 ──────── N Employee
```

### Operaciones

Esta aplicación administra:

- **Project:** proyectos de la organización.
- **Assignment:** asignaciones de empleados a proyectos.

Relaciones:

```text
Employee 1 ──────── N Assignment N ──────── 1 Project
```

## Modelos y persistencia

La aplicación utiliza **Django ORM** para trabajar con la base de datos.

Los modelos principales son:

| Modelo | Aplicación | Descripción |
|---|---|---|
| Department | recursos_humanos | Representa los departamentos |
| Employee | recursos_humanos | Representa los empleados |
| Project | operaciones | Representa los proyectos |
| Assignment | operaciones | Relaciona empleados con proyectos |

Las relaciones entre entidades se implementan mediante `ForeignKey`.

## Migración de datos

El proyecto incluye `data.json` como fuente de información inicial y `loader.py` para cargar esa información mediante Django ORM hacia la base de datos.

Una vez realizada la carga, las vistas de la aplicación consultan la información directamente desde la base de datos mediante Django ORM.

## Django Admin

Todas las entidades del proyecto se encuentran registradas en Django Admin.

Desde el panel de administración es posible:

- Crear registros.
- Modificar registros.
- Eliminar registros.
- Visualizar registros.
- Buscar registros mediante los campos configurados en `search_fields`.
- Trabajar con entidades relacionadas mediante las relaciones definidas en los modelos.

Para acceder al panel:

```text
/admin/
```

Se requiere un usuario administrador creado con:

```bash
python manage.py createsuperuser
```

## Aplicación web

La aplicación cuenta con vistas para visualizar:

- Empleados.
- Departamentos.
- Proyectos.
- Asignaciones.

Los listados utilizan consultas mediante Django ORM y se presentan mediante plantillas HTML con Bootstrap.

Las vistas incluyen los controles visuales de **Agregar, Modificar, Eliminar y Buscar** requeridos para la interfaz. Las operaciones CRUD desde la interfaz pública no forman parte de esta etapa de evaluación.

## Base de datos

La configuración de la base de datos utiliza MySQL y variables de entorno.

Las variables utilizadas son:

```text
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

No se deben publicar credenciales reales en el repositorio.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Player-spect/back-end.git
cd back-end
```

### 2. Crear y activar el entorno virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con los valores correspondientes a la instalación de MySQL.

Ejemplo de estructura:

```env
SECRET_KEY=secret_key
DB_NAME=nombre_base_de_datos
DB_USER=usuario_mysql
DB_PASSWORD=contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear usuario administrador

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Luego acceder a:

```text
http://127.0.0.1:8080/
```

Y al panel administrativo:

```text
http://127.0.0.1:8080/admin/
```

## Variables sensibles

El archivo `.env` contiene información sensible y debe mantenerse fuera del control de versiones. El proyecto utiliza `.gitignore` para evitar que este archivo sea incluido en Git.
