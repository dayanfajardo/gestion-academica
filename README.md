# Sistema Académico Distribuido

Sistema de gestión académica basado en una **arquitectura de microservicios**, diseñado para centralizar y automatizar procesos relacionados con docentes, cursos, estudiantes, matrículas y calificaciones.

## Tabla de contenido

- [Problema que resuelve](#problema-que-resuelve)
- [Objetivo del proyecto](#objetivo-del-proyecto)
- [Integrantes y roles](#integrantes-y-roles)
- [Arquitectura del sistema](#arquitectura-del-sistema)
- [Servicios del sistema](#servicios-del-sistema)
- [Comunicación entre servicios](#comunicación-entre-servicios)
- [Documentación de endpoints](#documentacion-de-endpoints)
- [Bases de datos por servicio](#bases-de-datos-por-servicio)
- [Tipo de arquitectura](#tipo-de-arquitectura)
- [Modelo de datos y dominio](#modelo-de-datos-y-dominio)
- [Usuarios del sistema](#usuarios-del-sistema)
- [Arquitectura interna de los microservicios](#arquitectura-interna-de-los-microservicios)
- [Manejo de fallas](#manejo-de-fallas)
- [Configuración de variables de entorno](#configuración-mediante-variables-de-entorno)
- [Docker](#docker)
- [Docker-compose](#docker-compose)
- [Estado del proyecto](#estado-del-proyecto)

---

## Problema que resuelve

El sistema resuelve la necesidad de **centralizar y automatizar la gestión académica** de una institución educativa. Sin una plataforma integrada, estos procesos tendrían que manejarse de forma manual, dispersa o mediante hojas de cálculo y sistemas aislados.

En concreto, permite:

- Integrar los procesos de **docentes, cursos, estudiantes, matrículas y notas** bajo una arquitectura común accesible mediante API.
- Mejorar la **escalabilidad y mantenibilidad** del software, ya que cada dominio puede crecer, desplegarse y mantenerse de forma independiente.
- Reducir errores, inconsistencias de datos y procesos manuales poco escalables.

### ¿Quién lo usará?

- **Personal administrativo/académico:** registrar docentes, crear cursos y gestionar matrículas.
- **Docentes:** consultar y gestionar información de los cursos que dictan y, potencialmente, registrar notas.
- **Estudiantes:** consultar sus matrículas, cursos inscritos y calificaciones.

### ¿Qué pasaría si no existiera?

La institución tendría que depender de procesos manuales o herramientas no integradas, lo que aumentaría el riesgo de errores e inconsistencias, además de generar procesos más lentos y difíciles de escalar.

---

## Objetivo del proyecto

El propósito principal de este proyecto es **diseñar e implementar una plataforma integral para la administración de procesos académicos universitarios**, facilitando el control y seguimiento de docentes, cursos, estudiantes, matrículas y calificaciones.

Para lograrlo, el sistema adopta un enfoque modular basado en microservicios:

- **Autonomía y escalabilidad:** desacoplar cada área funcional para que pueda evolucionar y mantenerse de forma independiente.
- **Punto de acceso unificado:** centralizar las peticiones de los clientes mediante un **API Gateway**.
- **Aislamiento de datos:** respaldar cada servicio con su propia base de datos **PostgreSQL**, evitando dependencias directas entre módulos.

---

## Integrantes y roles

| Integrante | Rol |
| --- | --- |
| **Cristian Girón** | Líder de Proyecto, Documentación Técnica |
| **Dayan Fajardo** | Líder Técnico / DevOps, Presentación y Comunicación|

---

## Arquitectura del sistema

```text
┌───────────────────────────┐
│          Usuario          │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│          Frontend         │
│     Home / Interfaz UI    │
└─────────────┬─────────────┘
              │ HTTP
              ▼
┌───────────────────────────┐
│        API Gateway        │
└─────────────┬─────────────┘
              │
       ┌──────┼──────┬──────────┬─────────┐
       ▼      ▼      ▼          ▼         ▼
  Docentes  Cursos  Estudiantes Matrículas Notas
  Service   Service   Service    Service   Service
      │        │        │          │         │
      ▼        ▼        ▼          ▼         ▼
 PostgreSQL PostgreSQL PostgreSQL PostgreSQL PostgreSQL
```

Cada microservicio posee su propia lógica de negocio, base de datos y contenedor Docker. El **API Gateway** funciona como punto de entrada único para los clientes.

---

## Servicios del sistema

Los principales servicios del sistema académico son:

1. **Docentes:** gestiona la información de los profesores, como cédula, nombre, correo, departamento y género.
2. **Cursos:** administra los cursos ofrecidos, incluyendo código, nombre, créditos y semestre.
3. **Estudiantes:** gestiona los datos de los estudiantes, como cédula, nombre, correo y programa académico.
4. **Matrículas:** administra la relación entre estudiantes y cursos.
5. **Notas:** almacena las calificaciones asociadas a cada matrícula.

### Independencia de los microservicios

Cada microservicio puede desarrollarse y mantenerse de manera independiente porque cuenta con:

- Su propia **base de datos**.
- Su propia **lógica de negocio**.
- Su propio **contenedor Docker**.
- Su propio **Dockerfile** para el despliegue.

También son independientes los procesos de:

- **Despliegue**.
- **Modelado de base de datos**.
- **Pruebas**.

---
## Comunicación entre servicios

| Servicio  | Responsabilidad | Información administrada | Comunicación con otros servicios
| --- | --- | --- | --- |
| **Docentes** | gestiona la información de los profesores | Datos personales |  |
| **Cursos** | administra los cursos ofrecidos | Información sobre cursos | Docentes,  |
| **Estudiantes** | gestiona los datos de los estudiantes | Datos personales |  |
| **Matriculas** | administra la relación entre estudiantes y cursos | Relación estudiante - curso | estudiantes, cursos | 
| **Notas** | almacena las calificaciones asociadas a cada matrícula | Información académica | Matriculas |

La comunicación entre los microservicios funciona de manera **síncrona** mediante peticiones **HTTP/REST**, utilizando **JSON** como formato de intercambio de datos.

El **API Gateway** recibe las peticiones del cliente y las enruta al servicio correspondiente según el recurso solicitado:

```text
/docentes
/cursos
/estudiantes
/matriculas
/notas
```

Algunos servicios también necesitan comunicarse directamente entre sí para validar información:

1. **Matrículas → Estudiantes y Cursos:** antes de crear una matrícula, se valida que existan el `estudiante_id` y el `curso_id`.
2. **Notas → Matrículas:** antes de registrar una nota, se valida que exista el `matricula_id`.


### El servicio Cursos necesita consultar la información de un docente.
| Elemento | Descripción | 
| --- | --- |
| **Servicio que solicita** | Cursos  |
| **Servicio que responde** | Docentes |
| **Endpoint utilizado** | http://docentes-service:5001/docentes/{id_docente} |
| **Información enviada** | Id Docente |
| **Información recibida** | Información de docente | 

### El servicio Matrículas necesita consultar la información de un estudiante.
| Elemento | Descripción | 
| --- | --- |
| **Servicio que solicita** | Matrículas  |
| **Servicio que responde** | Estudiantes |
| **Endpoint utilizado** | http://estudiantes-service:5003/estudiantes/{id_estudiante} |
| **Información enviada** | Id estudiante |
| **Información recibida** | Información del estudiante | 

### El servicio Matrículas necesita consultar la información de un curso.
| Elemento | Descripción | 
| --- | --- |
| **Servicio que solicita** | Matrículas  |
| **Servicio que responde** | Cursos |
| **Endpoint utilizado** | http://cursos-service:5002/cursos/{id_curso} |
| **Información enviada** | Id curso |
| **Información recibida** | Información del curso | 

### El servicio Notas necesita consultar la información de una matícula.
| Elemento | Descripción | 
| --- | --- |
| **Servicio que solicita** | Notas  |
| **Servicio que responde** | Matrículas |
| **Endpoint utilizado** | http://matriculas-service:5004/matriculas/{id_matricula} |
| **Información enviada** | Id matricula |
| **Información recibida** | Información de la matrícula | 

---
### Formato de datos

Los servicios exponen y consumen información en formato **JSON**, lo que facilita la interoperabilidad entre ellos aunque cada microservicio tenga una base de datos independiente.

### ¿Qué pasa si un servicio no responde?

Si, por ejemplo, el servicio de Matrículas necesita validar un estudiante y el servicio de Estudiantes no responde, la operación de matrícula **no debería completarse**, con el fin de evitar inconsistencias.

Para manejar este escenario se propone:

- Definir **timeouts** en las peticiones entre servicios.
- Retornar códigos de error claros, como `503 Service Unavailable`, cuando falle un servicio dependiente.

---

## Documentacion de endpoints
### Servicio Docentes
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /docentes | Consultar docentes | Ninguna | Listado de docentes |
| **GET** | docentes/{id} | Consultar docente | ID docente | Docente específico | 
| **POST** | /docentes | Crear docente | JSON docente | Confirmación | 
| **PUT** | docentes/{id} | Actualizar docente | Json actualizado | Docente modificado |  
| **DELETE** | /docentes/{id} | Eliminar docente | ID docente | confirmación | 

### Servicio Cursos
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /cursos | Consultar cursos | Ninguna | Listado de cursos |
| **GET** | cursos/{id} | Consultar curso | ID curso | curso específico | 
| **POST** | /cursos | Crear curso | JSON curso | Confirmación | 
| **PUT** | cursos/{id} | Actualizar curso | Json actualizado | curso modificado |  
| **DELETE** | /cursos/{id} | Eliminar curso | ID curso | confirmación | 

### Servicio Estudiantes
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /estudiantes | Consultar estudiantes | Ninguna | Listado de estudiantes |
| **GET** | estudiantes/{id} | Consultar estudiante | ID estudiante | estudiante específico | 
| **POST** | /estudiantes | Crear estudiante | JSON estudiante | Confirmación | 
| **PUT** | estudiantes/{id} | Actualizar estudiante | Json actualizado | estudiante modificado |  
| **DELETE** | /estudiantes/{id} | Eliminar estudiante | ID estudiante | confirmación | 

### Servicio Matriculas
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /matriculas | Consultar matriculas | Ninguna | Listado de matriculas |
| **GET** | matriculas/{id} | Consultar matricula | ID matricula | matricula específico | 
| **POST** | /matriculas | Crear matricula | JSON matricula | Confirmación | 
| **PUT** | matriculas/{id} | Actualizar matricula | Json actualizado | matricula modificada |  
| **DELETE** | /matriculas/{id} | Eliminar matricula | ID matricula | confirmación | 

### Servicio Notas
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /notas | Consultar notas | Ninguna | Listado de notas |
| **GET** | notas/{id} | Consultar nota | ID nota | nota específica | 
| **POST** | /notas | Crear nota | JSON nota | Confirmación | 
| **PUT** | notas/{id} | Actualizar nota | Json actualizado | nota modificada |  
| **DELETE** | /notas/{id} | Eliminar nota | ID nota | confirmación | 
---

## Tipo de arquitectura

Se eligió una **arquitectura de microservicios** porque permite dividir el sistema en servicios independientes, facilitando el mantenimiento, el despliegue y el crecimiento según la demanda.

Cada módulo puede escalar o actualizarse sin afectar directamente a los demás, lo que ofrece mayor flexibilidad frente a una arquitectura monolítica tradicional.

---

## Bases de datos por servicio
| Servicio  | Base de datos utilizada | Tablas principales |
| --- | --- | --- | 
| **Docentes** | PostgreSQL | docente |
| **Cursos** | PostgreSQL | curso |
| **Estudiantes** | PostgreSQL | estudiante |
| **Matrículas** | PostgreSQL | matricula |
| **Notas** | PostgreSQL | nota |

---

## Modelo de datos y dominio

Cada microservicio administra su propio dominio y su propia tabla principal.

### 1. Servicio de Docentes (`docentes-service`)

**Tabla:** `docente`

| Campo | Tipo de dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `departamento` | `VARCHAR(100)` | `NOT NULL` |
| `genero` | `VARCHAR(20)` | Opcional |

### 2. Servicio de Cursos (`cursos-service`)

**Tabla:** `curso`

| Campo | Tipo de dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, autogenerado (`SERIAL`) |
| `codigo` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `creditos` | `INTEGER` | `NOT NULL` |
| `semestre` | `INTEGER` | `NOT NULL` |
| `docente_id` | `INTEGER` | `NOT NULL` (clave foránea lógica) |

### 3. Servicio de Estudiantes (`estudiantes-service`)

**Tabla:** `estudiante`

| Campo | Tipo de dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `programa` | `VARCHAR(100)` | `NOT NULL` |

### 4. Servicio de Matrículas (`matriculas-service`)

**Tabla:** `matricula`

| Campo | Tipo de dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, autogenerado (`SERIAL`) |
| `estudiante_id` | `INTEGER` | `NOT NULL` (clave foránea lógica) |
| `curso_id` | `INTEGER` | `NOT NULL` (clave foránea lógica) |
| `anio` | `INTEGER` | `NOT NULL` (año lectivo) |
| `periodo` | `VARCHAR(10)` | `NOT NULL` (ej.: `1`, `2`, `2026-1`) |

### 5. Servicio de Notas (`notas-service`)

**Tabla:** `nota`

| Campo | Tipo de dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, autogenerado (`SERIAL`) |
| `matricula_id` | `INTEGER` | `NOT NULL` (clave foránea lógica) |
| `calificacion` | `NUMERIC(3,2)` | `NOT NULL` (ej.: `4.50`) |
| `observacion` | `VARCHAR(200)` | Opcional |

### Relaciones del sistema

- **Docente → Curso:** un curso referencia al docente responsable mediante `docente_id`.
- **Estudiante → Matrícula:** una matrícula referencia al estudiante mediante `estudiante_id`.
- **Curso → Matrícula:** una matrícula referencia al curso mediante `curso_id`.
- **Matrícula → Nota:** una nota referencia a la matrícula mediante `matricula_id`.

### Datos críticos

1. **Cédula** de docentes y estudiantes: identifica de forma única a la persona.
2. **`docente_id`:** permite identificar al responsable de un curso.
3. **`estudiante_id` y `curso_id`:** conectan al estudiante con el curso matriculado.
4. **`matricula_id`:** vincula una calificación con una matrícula.
5. **Calificación:** representa el resultado académico del estudiante.

### Impacto de la pérdida de datos

- Si se pierden **docentes**, algunos cursos podrían quedar asociados a un `docente_id` inexistente.
- Si se pierden **estudiantes**, algunas matrículas quedarían con referencias huérfanas.
- Si se pierden **cursos**, se perdería la relación entre determinadas matrículas y sus asignaturas.
- Si se pierden **notas**, se afectaría directamente el historial académico.

---

## Usuarios del sistema

| Usuario | Descripción | Acciones principales |
| --- | --- | --- |
| **Administrativo/Académico** | Personal encargado de la gestión general del sistema | Registrar docentes, crear cursos y gestionar matrículas |
| **Docente** | Profesor responsable de uno o más cursos | Consultar o gestionar sus cursos y registrar notas |
| **Estudiante** | Usuario matriculado en uno o más cursos | Consultar matrículas, cursos inscritos y calificaciones |

Aunque todos ingresan a través del mismo **API Gateway**, el nivel de acceso depende del rol. Un estudiante debería poder consultar únicamente su propia información, mientras que el personal administrativo y los docentes tendrían permisos de creación o modificación según sus responsabilidades.

---

## Arquitectura interna de los microservicios

La estructura base propuesta para cada microservicio es:

```text
microservicio/
│
├── app.py
│
├── src/
│   ├── routes.py
│   └── services.py
│
├── db.py
│
├── requirements.txt
│
└── Dockerfile
```

### Responsabilidad de los componentes

- **`app.py`:** punto de entrada de la aplicación.
- **`src/routes.py`:** definición de endpoints y rutas HTTP.
- **`src/services.py`:** lógica de negocio del microservicio.
- **`db.py`:** configuración y manejo de la conexión con la base de datos.
- **`requirements.txt`:** dependencias de Python necesarias para ejecutar el servicio.
- **`Dockerfile`:** instrucciones para construir la imagen Docker del microservicio.

---

## Manejo de fallas

### Fallas en un servicio

Si se presenta una falla en un servicio, por ejemplo **Notas**, las demás funcionalidades independientes pueden continuar operando. Sin embargo, cualquier operación que dependa directamente de dicho servicio no podrá completarse correctamente.

Como medidas de manejo se propone:

- Implementar un endpoint `/health` en cada servicio para verificar su disponibilidad.
- Implementar **reintentos exponenciales** cuando un servicio se encuentre temporalmente reiniciándose o no disponible.
- Utilizar **timeouts** para evitar peticiones bloqueadas indefinidamente.
- Retornar códigos HTTP adecuados ante fallas controladas.

### Fallas en la base de datos

Una falla o pérdida de información en una base de datos puede generar inconsistencias debido a las referencias lógicas existentes entre los distintos servicios.

**Medidas propuestas:**

- Implementar **backups automáticos y periódicos**.
- Utilizar **réplicas de lectura** en los servicios con mayor volumen de consultas.
- Monitorear recursos como conexiones activas, espacio en disco y disponibilidad para detectar problemas antes de una caída total.

---
## Configuración mediante variables de entorno
| Variable | Uso |
| --- | --- |
| `DB_NAME_DOCENTES` | nombre de base de datos del servicio de docentes |
| `DB_NAME_CURSOS` | nombre de base de datos del servicio de cursos |
| `DB_NAME_ESTUDIANTES` | nombre de base de datos del servicio de estudiantes |
| `DB_NAME_MATRICULAS` | nombre de base de datos del servicio de matrículas |
| `DB_NAME_NOTAS` | nombre de base de datos del servicio de notas |
| `DB_PORT` | Puerto de conexión a la base de datos |
| `DB_USER` | Usuario de la base de datos |
| `DB_PASSWORD` | Contraseña del usuario de la base de datos |
| `DB_HOST_DOCENTES` | dirección del servidor donde está corriendo la base de datos de Docentes  |
| `DB_HOST_CURSOS` | dirección del servidor donde está corriendo la base de datos de Cursos  |
| `DB_HOST_ESTUDIANTES` | dirección del servidor donde está corriendo la base de datos de Estudiantes  |
| `DB_HOST_MATRICULAS` | dirección del servidor donde está corriendo la base de datos de Matrículas  |
| `DB_HOST_NOTAS` | dirección del servidor donde está corriendo la base de datos de Notas  |
| `DOCENTES_SERVICE_URL` |  URL del servicio docentes para la comunicación con otros servicios |
| `CURSOS_SERVICE_URL` |  URL del servicio cursos para la comunicación con otros servicios |
| `ESTUDIANTES_SERVICE_URL` | URL del servicio estudiantes para la comunicación con otros servicios  |
| `MATRICULAS_SERVICE_URL` |  URL del servicio matriculas para la comunicación con otros servicios |
| `NOTAS_SERVICE_URL` |  URL del servicio notas para la comunicación con otros servicios |



---
## Docker

La vista `frontend/index.html` es un archivo estático. Actualmente no tiene un contenedor propio ni un proceso de compilación independiente. Se sirve desde el contenedor `gateway`, que utiliza Nginx como servidor web y también como API Gateway.

## Recorrido de la vista

```text
Navegador
   ↓ http://localhost:8000
Docker
   ↓ puerto 8000 → puerto 80
Contenedor gateway
   ↓
Nginx
   ↓
/usr/share/nginx/html/index.html
   ↓
frontend/index.html
```
## Docker-compose
El proyecto cuenta con un archivo `docker-compose.yml` que permite levantar todos los servicios y sus bases de datos de manera coordinada.

Para ejecutarlo se debe utilizar el comando:
```bash
docker-compose up --build -d
```
## Estado del proyecto

Proyecto académico en desarrollo, orientado a aplicar conceptos de **sistemas distribuidos, microservicios, APIs REST, Docker y PostgreSQL**.
