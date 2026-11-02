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
- HTML / Bootstrap 5 (footer sticky)
- Gunicorn + Nginx (despliegue)
- Git / GitHub

## Estructura del proyecto

```text
Gestion/
├── gestion_corporativa/          # Configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── core/                         # Autenticación, dashboards, usuarios y roles
│   ├── decorators.py             # role_required + get_roles
│   ├── roles.py                  # Roles y permisos por grupo
│   ├── validators.py             # Política de contraseñas y username
│   ├── forms.py                  # Creación/edición de usuarios
│   ├── views.py                  # Dashboard, usuarios y páginas de error
│   ├── templatetags/auth_tags.py # Etiqueta has_group
│   └── management/commands/
│       ├── setup_roles.py        # Crea grupos y permisos
│       └── reset_link.py         # Enlace de recuperación (desarrollo)
├── recursos_humanos/             # Department, Employee + CRUD
│   ├── validators.py             # Validación de RUT (módulo 11)
│   └── forms.py
├── operaciones/                  # Project, Assignment + CRUD/transacción
│   └── forms.py
├── templates/                    # Plantillas propias (Bootstrap)
│   ├── core/                     # Login, dashboards, usuarios, reset
│   ├── recursos_humanos/
│   ├── operaciones/
│   └── 403.html, 404.html, 500.html
├── static/                       # CSS/JS de Bootstrap
├── data.json                     # Datos iniciales
├── loader.py                     # Carga inicial de datos
├── manage.py
├── requirements.txt
├── .env.example
└── .env                          # Variables de entorno (no versionado)
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

| Rol | Ver | Crear/Editar | Eliminar | Usuarios | Dashboard |
|---|:---:|:---:|:---:|:---:|---|
| **Administrador** | ✅ | ✅ | ✅ | ✅ | Global |
| **Supervisor** | ✅ | ✅ | ❌ | ❌ | Operacional |
| **Administrativo** | ✅ | ❌ | ❌ | ❌ | Solo lectura |

- **Administrador**: todos los permisos del sistema.
- **Supervisor**: crea/edita mantenedores y asignaciones; no elimina ni gestiona usuarios.
- **Administrativo**: solo visualiza información operativa; operaciones críticas bloqueadas.

Los grupos y permisos se crean con:

```bash
python manage.py setup_roles
```

La autorización se aplica con `core.decorators.role_required` y, en plantillas, con `{% has_group 'Administrador' %}`.

## Funcionalidades

- Inicio y cierre de sesión propios (sin Django Admin).
- **Protección global de sesión** con `LoginRequiredMiddleware`: toda ruta exige autenticación salvo login y recuperación de contraseña (`@login_not_required`).
- Dashboards diferenciados por rol.
- Gestión de usuarios desde la interfaz: crear, editar, asignar roles y eliminar.
- Recuperación de contraseña por correo con **token seguro de Django** (un solo uso).
- Mantenedores CRUD: **Departamentos**, **Empleados**, **Proyectos**.
- **Transacción operacional**: Asignaciones (Empleado + Proyecto) con validación de duplicados.
- Búsqueda en todos los listados.
- Validación de **RUT chileno** (algoritmo módulo 11) en empleados.
- **Username** limitado a 32 caracteres.
- **Política de contraseñas**: mínimo 8 caracteres, una mayúscula, un número y un carácter especial.
- Páginas propias de error **403, 404 y 500**.
- Interfaz responsive con Bootstrap 5 y footer sticky.

## Seguridad

- Contraseñas almacenadas como hash **PBKDF2-SHA256** (nunca en texto plano).
- Variables sensibles (SECRET_KEY, DB, SMTP) en `.env`, fuera de Git.
- Protección CSRF en todos los formularios.
- Autorización por grupos y permisos de Django.
- Sesión requerida globalmente.
- Validación de entradas mediante formularios Django (RUT, username, contraseña, presupuesto, duplicados).
- Django Admin deshabilitado en las rutas.

## Configuración del entorno

Variables utilizadas (archivo `.env`):

```env
SECRET_KEY=...
DEBUG=False
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

- Sin `DB_HOST`, el proyecto usa **SQLite** (`db.sqlite3`) para desarrollo.
- Con `DB_*` definidos, usa **MySQL** (producción).
- Sin configuración SMTP, el correo se imprime en la consola (`console.EmailBackend`).

## Instalación en desarrollo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # completar credenciales
python manage.py migrate
python manage.py setup_roles
python loader.py              # carga inicial desde data.json
python manage.py runserver
```

Acceder a `http://127.0.0.1:8000/login/`.

## Usuarios de demostración (desarrollo)

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | Admin12345! | Administrador |
| supervisor | Supervisor12345! | Supervisor |
| administrativo | Administrativo12345! | Administrativo |

> Las contraseñas se almacenan como hash PBKDF2-SHA256.
> Cambiar estas credenciales antes de un despliegue real.

## Pruebas

```bash
python manage.py test
```

Las pruebas cubren: autenticación, autorización por rol, protección global de sesión, dashboards, CRUD, transacción con duplicados, política de contraseñas, validación de RUT y recuperación de contraseña.

### Probar recuperación de contraseña en desarrollo

Con el backend de consola, el enlace puede aparecer cortado por el formato quoted-printable (`=\n`) del correo. Para obtener un enlace limpio:

```bash
python manage.py reset_link admin
python manage.py reset_link admin@empresa.cl --base-url http://127.0.0.1:8000
```

Abre el enlace, define la nueva contraseña y accede. Para probar el flujo real, configura un SMTP en `.env`.

---

## Despliegue mínimo correcto (AWS EC2)

Guía mínima para dejar la aplicación operativa en una instancia Ubuntu con MySQL, Gunicorn y Nginx, usando la **IP pública de AWS** (sin dominio propio).

### 1. Instancia y Security Group

- Ubuntu 24.04 LTS, tipo `t3.micro`.
- Asocia una **Elastic IP** para que la IP no cambie.
- Reglas entrantes:
  - `22` (SSH) → tu IP
  - `80` (HTTP) → 0.0.0.0/0 (necesario para redirigir a HTTPS)
  - `443` (HTTPS) → 0.0.0.0/0 (si usarás certificado)

### 2. Paquetes del sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip nginx git \
  build-essential pkg-config libmysqlclient-dev mysql-server
```

### 3. Base de datos MySQL

```bash
sudo mysql
```

```sql
CREATE DATABASE gestion_corporativa CHARACTER SET utf8mb4;
CREATE USER 'gestion'@'localhost' IDENTIFIED BY 'ClaveSegura123!';
GRANT ALL PRIVILEGES ON gestion_corporativa.* TO 'gestion'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Proyecto en `/var/www/html/Gestion`

```bash
sudo mkdir -p /var/www/html
sudo chown -R $USER:$USER /var/www/html
cd /var/www/html
git clone https://github.com/Player-spect/back-end.git Gestion
cd /var/www/html/Gestion

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

Crea el `.env` de producción:

```env
SECRET_KEY=<clave-aleatoria-larga>
DEBUG=False
ALLOWED_HOSTS=TU_IP_PUBLICA

DB_NAME=gestion_corporativa
DB_USER=gestion
DB_PASSWORD=ClaveSegura123!
DB_HOST=localhost
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tucorreo@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
DEFAULT_FROM_EMAIL=tucorreo@gmail.com
```

Genera la clave:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Preparar la aplicación

```bash
cd /var/www/html/Gestion
source .venv/bin/activate
python manage.py migrate
python manage.py setup_roles
python loader.py
python manage.py collectstatic --noinput
```

### 6. Permisos para Nginx

```bash
sudo chown -R www-data:www-data /var/www/html/Gestion
sudo chmod 600 /var/www/html/Gestion/.env
sudo chmod 755 /var/www /var/www/html
```

> Si necesitas seguir usando Git con tu usuario, deja el propietario en `$USER` y ejecuta Gunicorn con `User=$USER`.

### 7. Servicio Gunicorn

Crea `/etc/systemd/system/gestion.service`:

```ini
[Unit]
Description=Gestion Corporativa (Gunicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/html/Gestion
Environment="PATH=/var/www/html/Gestion/.venv/bin"
RuntimeDirectory=gestion
RuntimeDirectoryMode=0755
ExecStart=/var/www/html/Gestion/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gestion/gestion.sock \
    gestion_corporativa.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gestion
sudo systemctl status gestion
```

### 8. Nginx

Crea `/etc/nginx/sites-available/gestion`:

```nginx
server {
    listen 80;
    server_name TU_IP_PUBLICA;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name TU_IP_PUBLICA;

    ssl_certificate     /etc/nginx/ssl/gestion.crt;
    ssl_certificate_key /etc/nginx/ssl/gestion.key;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/html/Gestion/staticfiles/;
        expires 30d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gestion/gestion.sock;
    }
}
```

> Si aún no tienes certificado, usa solo el bloque `listen 80` sin la redirección y elimina las líneas `ssl_*`.

Activa el sitio:

```bash
sudo ln -sf /etc/nginx/sites-available/gestion /etc/nginx/sites-enabled/gestion
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Certificado (opcional, sin dominio)

Certificado autofirmado con SAN para la IP:

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/gestion.key \
  -out /etc/nginx/ssl/gestion.crt \
  -subj "/CN=TU_IP_PUBLICA" \
  -addext "subjectAltName=IP:TU_IP_PUBLICA"
sudo chmod 600 /etc/nginx/ssl/gestion.key
sudo systemctl reload nginx
```

El navegador mostrará una advertencia de certificado no confiable; es normal con certificados autofirmados.

### 10. Ajustes de Django para HTTPS (opcional)

En `settings.py`, para que Django reconozca que la petición llegó por HTTPS detrás de Nginx:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

No actives `SECURE_HSTS_SECONDS` con un certificado autofirmado.

### 11. Verificación

```bash
curl -I https://127.0.0.1/login/ -k
sudo journalctl -u gestion -f
sudo tail -f /var/log/nginx/error.log
```

Accede desde el navegador:

```
https://TU_IP_PUBLICA/login/
```

### Checklist mínimo de despliegue

- [ ] `DEBUG=False` en `.env`
- [ ] `ALLOWED_HOSTS` incluye la IP pública
- [ ] Variables `DB_*` configuradas (MySQL, no SQLite)
- [ ] `migrate`, `setup_roles`, `collectstatic` ejecutados
- [ ] `gestion.service` activo y habilitado
- [ ] Nginx activo, `nginx -t` sin errores
- [ ] `staticfiles/` accesible desde el navegador
- [ ] Login, CRUD, asignaciones y recuperación de contraseña probados

### Solución de problemas comunes

| Problema | Causa / solución |
|---|---|
| `Bad Request (400)` | Falta la IP en `ALLOWED_HOSTS` |
| `502 Bad Gateway` | Gunicorn caído o socket con permisos incorrectos (`journalctl -u gestion`) |
| Estilos no cargan | `collectstatic` no ejecutado o `alias` apunta a `staticfiles/` |
| Error de conexión MySQL | Variables `DB_*` incorrectas o servicio `mysql` detenido |
| Enlaces `http://` en correos | Añadir `SECURE_PROXY_SSL_HEADER` |
| Bucle de redirección | `SECURE_SSL_REDIRECT=True` sin `SECURE_PROXY_SSL_HEADER` |
