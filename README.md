# Gestión Corporativa

Aplicación web desarrollada con **Django** para la gestión de información de una organización. Utiliza una base de datos relacional (MySQL en producción) y Django ORM para la persistencia y consulta de datos.

## Objetivo

Transformar la información que inicialmente se encontraba en archivos JSON en una solución web basada en una base de datos relacional, con autenticación propia, roles, dashboards diferenciados, mantenedores CRUD y transacciones operacionales. **No se utiliza Django Admin para operar el sistema**; toda la operación se realiza mediante plantillas propias.

## Tecnologías

- Python
- Django 6.1.1
- MySQL (producción) / SQLite (desarrollo)
- mysqlclient
- python-dotenv
- HTML / Bootstrap 5
- Git / GitHub

## Estructura del proyecto

```text
BackEnd/
├── gestion_corporativa/     # Configuración del proyecto
├── core/                    # Autenticación, dashboards, usuarios y roles
│   ├── decorators.py        # Decorador role_required
│   ├── roles.py             # Definición de roles y permisos
│   ├── forms.py             # Formularios de usuarios
│   ├── views.py             # Dashboard y gestión de usuarios
│   └── management/commands/setup_roles.py
├── recursos_humanos/        # Department, Employee + CRUD
├── operaciones/             # Project, Assignment + CRUD/transacción
├── templates/               # Plantillas propias (Bootstrap)
├── static/                  # CSS/JS de Bootstrap
├── data.json                # Datos iniciales
├── loader.py                # Carga inicial de datos
├── manage.py
├── requirements.txt
└── .env / .env.local        # Variables de entorno (no versionadas)
```

## Modelos y relaciones

| Modelo | Aplicación | Descripción |
|---|---|---|
| Department | recursos_humanos | Departamentos |
| Employee | recursos_humanos | Empleados (FK Department) |
| Project | operaciones | Proyectos |
| Assignment | operaciones | Asignación empleado-proyecto (FK Employee, Project) |

Relaciones:

```text
Department 1 ──── N Employee
Employee   1 ──── N Assignment N ──── 1 Project
```

## Roles y permisos

El sistema define tres grupos de Django:

| Rol | Acceso |
|---|---|
| **Administrador** | Acceso total: mantenedores, transacciones, gestión de usuarios y dashboards globales. |
| **Supervisor** | Crear/editar mantenedores y asignaciones; sin eliminación ni gestión de usuarios. |
| **Administrativo** | Solo lectura de información operativa; operaciones críticas bloqueadas. |

Los grupos y permisos se crean con:

```bash
python manage.py setup_roles
```

La autorización de vistas se implementa con el decorador `core.decorators.role_required`.

## Funcionalidades

- Inicio y cierre de sesión propios (sin Django Admin).
- Dashboards diferenciados por rol.
- Gestión de usuarios desde la interfaz: crear, editar, asignar roles y eliminar.
- Recuperación de contraseña por correo con token seguro de Django.
- Mantenedores CRUD: Departamentos, Empleados, Proyectos.
- Transacción operacional: Asignaciones (Empleado + Proyecto) con validación de duplicados.
- Búsqueda en todos los listados.
- **Protección global de sesión**: `LoginRequiredMiddleware` exige autenticación en todas las rutas, excepto login y recuperación de contraseña (`@login_not_required`).
- Rutas inexistentes responden **404** con página propia; accesos sin permiso responden **403**.
- Validación de **RUT chileno** (módulo 11) en el mantenedor de empleados.
- Nombre de usuario limitado a **32 caracteres**.
- Política de contraseñas: mínimo 8 caracteres, una mayúscula, un número y un carácter especial.

## Configuración del entorno

Variables utilizadas (archivo `.env` o `.env.local`):

```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.ejemplo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=no-reply@ejemplo.cl
```

Si no se define `DB_HOST`, el proyecto usa **SQLite** (`db.sqlite3`) para desarrollo. En producción (AWS EC2) se configuran las variables `DB_*` para usar **MySQL**.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # completar credenciales
python manage.py migrate
python manage.py setup_roles
python manage.py loaddata  # opcional, si se usan fixtures
python loader.py          # carga inicial desde data.json
python manage.py runserver
```

Acceder a `http://127.0.0.1:8000/login/`.

## Usuarios de demostración (desarrollo)

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | Admin12345! | Administrador |
| supervisor | Supervisor12345! | Supervisor |
| administrativo | Administrativo12345! | Administrativo |

> Las contraseñas se almacenan como hash PBKDF2-SHA256 (nunca en texto plano).
> Política: mínimo 8 caracteres, al menos una mayúscula, un número y un carácter especial.

> Cambiar estas contraseñas antes de cualquier despliegue real.

## Pruebas

```bash
python manage.py test
```

Cubren autenticación, autorización por rol, dashboards, CRUD y recuperación de contraseña.

### Probar recuperación de contraseña en desarrollo

Con el backend de correo de consola, el email se imprime en la terminal y el enlace puede aparecer **cortado por el formato quoted-printable** (`=\n`), por lo que copiarlo tal cual resulta inválido. Para obtener un enlace limpio y válido:

```bash
python manage.py reset_link admin
# o por email:
python manage.py reset_link admin@empresa.cl --base-url http://127.0.0.1:8000
```

Abre el enlace mostrado, define la nueva contraseña y accede. También puedes probar el flujo real desde `/password-reset/` configurando un SMTP en `.env`.

## Despliegue en AWS EC2

1. Clonar el repositorio e instalar dependencias en un virtualenv.
2. Configurar `.env` con credenciales de MySQL y SMTP.
3. Ejecutar `migrate`, `setup_roles` y `collectstatic`.
4. Servir con Gunicorn detrás de Nginx.
5. Configurar `ALLOWED_HOSTS` con el dominio/IP de la instancia y `DEBUG=False`.
