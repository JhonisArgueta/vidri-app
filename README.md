# Vidri App — Python Flask + MySQL

Aplicación web desarrollada con **Python, Flask y MySQL**, desplegada en una plataforma **PaaS (Platform as a Service) multicliente** mediante Docker y Kubernetes.

## Descripción

Vidri es una aplicación web que integra autenticación de usuarios, un dashboard y conexión a una base de datos MySQL.

Forma parte de un proyecto académico de computación en la nube, cuyo objetivo es demostrar el despliegue y la administración de aplicaciones de diferentes clientes, utilizando distintas tecnologías dentro de una misma plataforma PaaS.

## Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje de programación del backend |
| Flask | Framework web |
| MySQL | Base de datos relacional |
| HTML y CSS | Interfaz web |
| Docker | Contenerización |
| Kubernetes | Orquestación y despliegue |
| NGINX Ingress | Acceso HTTP/HTTPS |
| Git y GitHub | Control de versiones |

## Características principales

- Autenticación de usuarios.
- Verificación segura de contraseñas mediante Werkzeug.
- Conexión a una base de datos MySQL.
- Dashboard web.
- Configuración mediante variables de entorno.
- Aplicación contenerizada mediante Docker.
- Despliegue independiente en Kubernetes.
- Endpoint de salud para verificar la aplicación y su conexión con MySQL.
- Integración con el monitoreo y la administración de recursos de la plataforma PaaS.

## Estructura del proyecto

```text
vidri-python/
├── templates/
│   ├── dashboard.html
│   └── login.html
├── .gitignore
├── Dockerfile
├── app.py
├── requirements.txt
└── README.md
```

## Variables de entorno

La aplicación obtiene su configuración a través de variables de entorno.

| Variable | Descripción |
|---|---|
| `DB_HOST` | Servidor MySQL |
| `DB_PORT` | Puerto de MySQL |
| `DB_USER` | Usuario de la base de datos |
| `DB_PASSWORD` | Contraseña de MySQL |
| `DB_NAME` | Nombre de la base de datos |
| `SECRET_KEY` | Clave secreta de Flask |
| `COOKIE_SECURE` | Configuración de cookies seguras |

Las credenciales reales no se almacenan en este repositorio.

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhonisArgueta/vidri-app.git
cd vidri-app
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Ejemplo para un entorno de desarrollo:

```bash
export DB_HOST="localhost"
export DB_PORT="3306"
export DB_USER="usuario_mysql"
export DB_PASSWORD="contraseña_de_desarrollo"
export DB_NAME="vidri_db"
export SECRET_KEY="clave_aleatoria_de_desarrollo"
export COOKIE_SECURE="false"
```

Los valores deben ajustarse a la configuración de MySQL. La base de datos y sus tablas deben estar creadas previamente.

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación requiere que MySQL esté disponible y correctamente configurado.

## Despliegue en Kubernetes

Vidri se despliega dentro del namespace `vidri`, mediante la plataforma PaaS multicliente.

La infraestructura utiliza:

- **Deployment:** `paas-vidri-app`
- **Service:** `paas-vidri-app`
- **Namespace:** `vidri`
- **Puerto de la aplicación:** `5000`
- **Puerto del Service:** `80`
- **Base de datos:** MySQL
- **Ingress:** NGINX con HTTPS
- **Dominio interno:** `vidri-app.vidri.paas.local`

La plataforma también permite aplicar cuotas de recursos, políticas de aislamiento y escalabilidad horizontal.

## Arquitectura general

```text
Usuario
   |
   v
NGINX Ingress (HTTPS)
   |
   v
Kubernetes Service
   |
   v
Vidri App (Python Flask)
   |
   v
MySQL
```

## Verificación de funcionamiento

En el entorno PaaS configurado, el endpoint `/health` permite comprobar el estado de la aplicación y la conexión con MySQL.

Ejemplo:

```bash
curl -k https://vidri-app.vidri.paas.local/health
```

La resolución del dominio interno requiere la configuración de red correspondiente.

## Seguridad

- Credenciales gestionadas mediante variables de entorno.
- Verificación de contraseñas mediante hashes.
- Separación de aplicaciones por namespaces de Kubernetes.
- Configuración de acceso HTTPS.
- Restricciones de recursos mediante ResourceQuota.
- Aislamiento de red mediante políticas de Kubernetes.

## Contexto académico

Este proyecto demuestra la ejecución de una aplicación Python Flask conectada a MySQL dentro de una plataforma PaaS multicliente.

Junto con Freund, desarrollada con Node.js y PostgreSQL, permite demostrar la capacidad de la plataforma para desplegar aplicaciones heterogéneas.


### Proyecto relacionado

Freund App — Node.js + PostgreSQL:

