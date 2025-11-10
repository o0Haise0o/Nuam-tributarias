# Nuam-tributarias
Nuam-tributarias
Proyecto universitario para la gestión de calificaciones tributarias. Desarrollado en un stack Full Stack con Django (Backend API) y React + TypeScript (Frontend).

Descripción
Esta plataforma permite la administración (CRUD) de calificaciones financieras, el registro de auditoría de cambios y la carga masiva de datos a través de archivos CSV.

Características Principales
Gestión CRUD: Creación, Lectura, Actualización (con modal) y Eliminación de Calificaciones.

Edición Detallada: Permite modificar campos clave como monto y periodo_comercial.

Carga Masiva (Bulk Upload): Importación de datos desde archivos .csv.

Auditoría (AuditLog): Seguimiento de todas las operaciones (Crear, Editar, Borrar) realizadas en el sistema.

Exportación: Descarga de la vista actual de datos a .csv.

API RESTful: Backend robusto construido con Django REST Framework.

Stack Tecnológico
Backend: Python 3.12, Django, Django REST Framework (DRF), django-filter.

Frontend: React, TypeScript, Vite, Axios, Tailwind CSS (para estilos base).

Base de Datos: SQLite (para desarrollo).

Instalación y Puesta en Marcha
Sigue estos pasos para configurar el entorno de desarrollo.

Pre-requisitos
Git

Python 3.12

Node.js (v18 o superior)

npm (o yarn)

1. Clonar el Repositorio
Bash

git clone https://github.com/o0Haise0o/Nuam-tributarias
cd Nuam-tributarias
2. Configurar el Backend (Django)
Sigue los pasos específicos para tu sistema operativo. (Asegúrate de tener tu archivo backend/requirements.txt listo).

Opción A: Linux / macOS
Bash

# 1. Crear y activar el entorno virtual de Python
python3.12 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias del backend
pip install -r backend/requirements.txt

# 3. Navegar al directorio del backend
cd backend/

# 4. Aplicar migraciones (creará el archivo db.sqlite3)
python manage.py migrate

# 5. Crear un superusuario para acceder al /admin
python manage.py createsuperuser

# 6. Iniciar el servidor de Django (API)
python manage.py runserver
Opción B: Windows (CMD o PowerShell)
Bash

# 1. Crear y activar el entorno virtual de Python
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar dependencias del backend
pip install -r backend\requirements.txt

# 3. Navegar al directorio del backend
cd backend\

# 4. Aplicar migraciones (creará el archivo db.sqlite3)
python manage.py migrate

# 5. Crear un superusuario para acceder al /admin
python manage.py createsuperuser

# 6. Iniciar el servidor de Django (API)
python manage.py runserver
Resultado: La API estará corriendo en http://127.0.0.1:8000. Deja esta terminal abierta.

3. Configurar el Frontend (React)
Abre una NUEVA TERMINAL (no cierres la del backend). Los comandos son idénticos para Linux y Windows.

Bash

# 1. Navegar al directorio del frontend (desde la raíz del proyecto)
cd frontend/

# 2. Instalar dependencias de Node.js
npm install

# 3. Iniciar el servidor de desarrollo (Vite)
npm run dev
La aplicación React estará corriendo en http://localhost:5173 (o el puerto que indique Vite).

Autores
Bruno Contreras, Jaime Matute, Tomas Bello
