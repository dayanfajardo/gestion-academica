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
- [API Gateway](#api-gateway)
- [Configuración de variables de entorno](#configuración-mediante-variables-de-entorno)
- [Docker](#docker)
- [Docker-compose](#docker-compose)
- [Pruebas del sistema](#pruebas-del-sistema)
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
              │ navegador: http://localhost:8000
              ▼
┌───────────────────────────┐
│          Frontend         │
│     Home / Interfaz UI    │  (archivos estáticos servidos por el gateway)
└─────────────┬─────────────┘
              │ HTTP / JSON
              ▼
┌───────────────────────────┐
│   API Gateway (Nginx)     │  puerto 8000 → 80
└─────────────┬─────────────┘
              │
       ┌──────┼──────┬──────────┬─────────┐
       ▼      ▼      ▼          ▼         ▼
  Docentes  Cursos  Estudiantes Matrículas Notas
   :5001    :5002     :5003      :5004    :5005
      │        │        │          │         │
      ▼        ▼        ▼          ▼         ▼
 docentes_db cursos_db estudiantes_db matriculas_db notas_db
 (PostgreSQL, cada una en su propio contenedor y volumen)
```

Comunicación entre microservicios y ubicación del **Timeout** y el **Circuit Breaker** (`src/resilience.py` del servicio que hace la petición):

```text
Cursos ──────[Timeout 2 s + Circuit Breaker "docentes"]──────► Docentes
   GET /docentes/{id}

Matrículas ──[Timeout 2 s + Circuit Breaker "estudiantes"]───► Estudiantes
   GET /estudiantes/{id}
Matrículas ──[Timeout 2 s + Circuit Breaker "cursos"]────────► Cursos
   GET /cursos/{id}

Notas ───────[Timeout 2 s + Circuit Breaker "matriculas"]────► Matrículas
   GET /matriculas/{id}
```

Todos los contenedores se definen en `docker-compose.yml` y se comunican por la red interna de Docker usando el nombre del servicio (por ejemplo `http://docentes-service:5001`).

Cada microservicio posee su propia lógica de negocio, base de datos y contenedor Docker. El **API Gateway** funciona como punto de entrada único para los clientes.

---

## Servicios del sistema

Los principales servicios del sistema académico son:

1. **Docentes:** gestiona la información de los profesores, como cédula, nombre, correo, departamento y género.
2. **Cursos:** administra los cursos ofrecidos, incluyendo código, nombre, créditos y semestre.
3. **Estudiantes:** gestiona los datos de los estudiantes, como cédula, nombre, correo y programa académico.
4. **Matrículas:** administra la relación entre estudiantes y cursos.
5. **Notas:** almacena las calificaciones asociadas a cada matrícula.

### Inventario de servicios

| Microservicio | Responsabilidad | Base de datos | Comunicación con otros servicios | Estado |
| --- | --- | --- | --- | --- |
| **docentes-service** | CRUD de docentes | `docentes_db` | Ninguna (es consultado por Cursos) | Implementado |
| **cursos-service** | CRUD de cursos | `cursos_db` | Consulta a Docentes | Implementado |
| **estudiantes-service** | CRUD de estudiantes | `estudiantes_db` | Ninguna (es consultado por Matrículas) | Implementado |
| **matriculas-service** | CRUD de matrículas | `matriculas_db` | Consulta a Estudiantes y Cursos | Implementado |
| **notas-service** | CRUD de notas | `notas_db` | Consulta a Matrículas | Implementado |
| **gateway** | Punto de entrada único y servidor de la vista Home | No aplica | Reenvía a los 5 servicios | Implementado |
| **frontend** | Vista Home e interfaz CRUD | No aplica | Solo se comunica con el gateway | Implementado |

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

1. **Cursos → Docentes:** antes de crear o actualizar un curso, se valida que exista el `docente_id`.
2. **Matrículas → Estudiantes y Cursos:** antes de crear o actualizar una matrícula, se valida que existan el `estudiante_id` y el `curso_id`.
3. **Notas → Matrículas:** antes de registrar o actualizar una nota, se valida que exista el `matricula_id`.

| Servicio solicitante | Servicio destino | Endpoint | Método HTTP | Información intercambiada |
| --- | --- | --- | --- | --- |
| Cursos | Docentes | `http://docentes-service:5001/docentes/{id}` | GET | Existencia del docente asignado al curso |
| Matrículas | Estudiantes | `http://estudiantes-service:5003/estudiantes/{id}` | GET | Existencia del estudiante a matricular |
| Matrículas | Cursos | `http://cursos-service:5002/cursos/{id}` | GET | Existencia del curso a matricular |
| Notas | Matrículas | `http://matriculas-service:5004/matriculas/{id}` | GET | Existencia de la matrícula calificada |

Si el servicio destino responde `200`, la operación continúa. Si responde `404`, el servicio solicitante responde `400` con un mensaje como `"El docente no existe."` y no guarda nada. Ningún servicio consulta la base de datos de otro: siempre se usa el endpoint correspondiente.


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

Para manejar este escenario se implementó:

- **Timeouts** en las peticiones entre servicios.
- **Circuit Breaker** sobre cada dependencia.
- Códigos de error claros, como `503 Service Unavailable` o `504 Gateway Timeout`, cuando falla un servicio dependiente.

El detalle está en [Timeout y Circuit Breaker](#timeout-y-circuit-breaker).

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

### Monitoreo del Circuit Breaker
| Método  | Endpoint | Descripción | Entrada | Respuesta 
| --- | --- | --- | --- | --- | 
| **GET** | /cursos/circuito | Estado del circuito hacia Docentes | Ninguna | Estado, fallos y segundos para HALF_OPEN |
| **GET** | /matriculas/circuito | Estado de los circuitos hacia Estudiantes y Cursos | Ninguna | Estado, fallos y segundos para HALF_OPEN |
| **GET** | /notas/circuito | Estado del circuito hacia Matrículas | Ninguna | Estado, fallos y segundos para HALF_OPEN |

### Códigos HTTP utilizados

| Situación | Código | Ejemplo |
| --- | --- | --- |
| Solicitud correcta | `200` | Consultar, actualizar o eliminar un registro existente |
| Recurso creado | `201` | `POST` exitoso |
| Datos inválidos o referencia inexistente | `400` | Crear un curso con un `docente_id` que no existe |
| Recurso inexistente | `404` | `GET /cursos/9999` |
| Registro duplicado | `409` | Cédula o correo ya registrados |
| Error interno | `500` | Error no controlado en el servicio |
| El servicio consultado respondió con error | `502` | Docentes respondió `5xx` |
| Dependencia no disponible o circuito abierto | `503` | Docentes detenido |
| Tiempo de espera agotado | `504` | Docentes no respondió en 2 segundos |

Un `404` del servicio consultado no se trata como una caída: significa que el recurso no existe y se responde `400` al cliente.

---

## Tipo de arquitectura

Se eligió una **arquitectura de microservicios** porque permite dividir el sistema en servicios independientes, facilitando el mantenimiento, el despliegue y el crecimiento según la demanda.

Cada módulo puede escalar o actualizarse sin afectar directamente a los demás, lo que ofrece mayor flexibilidad frente a una arquitectura monolítica tradicional.

---

## Bases de datos por servicio
| Microservicio | Base de datos | Contenedor | Volumen | Tablas principales | Operaciones implementadas |
| --- | --- | --- | --- | --- | --- |
| **Docentes** | PostgreSQL `docentes_db` | `docentes-db` | `docentes_data` | `docente` | SELECT, INSERT, UPDATE, DELETE |
| **Cursos** | PostgreSQL `cursos_db` | `cursos-db` | `cursos_data` | `curso` | SELECT, INSERT, UPDATE, DELETE |
| **Estudiantes** | PostgreSQL `estudiantes_db` | `estudiantes-db` | `estudiantes_data` | `estudiante` | SELECT, INSERT, UPDATE, DELETE |
| **Matrículas** | PostgreSQL `matriculas_db` | `matriculas-db` | `matriculas_data` | `matricula` | SELECT, INSERT, UPDATE, DELETE |
| **Notas** | PostgreSQL `notas_db` | `notas-db` | `notas_data` | `nota` | SELECT, INSERT, UPDATE, DELETE |

Cada servicio se conecta solamente a su base de datos, con los datos de conexión que recibe por variables de entorno (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`). Las tablas se crean al iniciar el servicio si todavía no existen.

### Persistencia

Los datos se guardan en volúmenes de Docker (`docentes_data`, `cursos_data`, etc.), montados en `/var/lib/postgresql/data` de cada contenedor de base de datos. Por eso la información se conserva aunque los contenedores se detengan o se vuelvan a crear.

Prueba de persistencia (sin borrar volúmenes, es decir, **sin** usar `docker compose down -v`):

```bash
# 1. Registrar un dato, por ejemplo un docente, desde la vista Home o con POST /docentes
# 2. Recrear los contenedores de la aplicación y de la base de datos
docker compose up -d --force-recreate docentes-service docentes-db
# 3. Consultar de nuevo: el docente sigue registrado
curl http://localhost:8000/docentes
```

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

Medidas implementadas:

- **Timeouts** para evitar peticiones bloqueadas indefinidamente.
- **Circuit Breaker** para dejar de consultar un servicio que está fallando de forma repetida.
- Códigos HTTP adecuados ante fallas controladas, en los servicios y en el gateway.
- `restart: on-failure` en `docker-compose.yml` para que un servicio que falla al iniciar se reinicie solo.

Medidas propuestas, **pendientes** de implementar:

- Un endpoint `/health` en cada servicio para verificar su disponibilidad.
- **Reintentos exponenciales** cuando un servicio se encuentre temporalmente reiniciándose o no disponible.

### Timeout y Circuit Breaker

Las llamadas síncronas entre servicios están protegidas con **timeout** y **circuit breaker** (librería [`pybreaker`](https://pypi.org/project/pybreaker/)), implementados en `src/resilience.py` de cada servicio consumidor:

| Servicio consumidor | Servicio consultado | Circuito |
| --- | --- | --- |
| Cursos | Docentes | `docentes` |
| Matrículas | Estudiantes y Cursos | `estudiantes`, `cursos` (independientes) |
| Notas | Matrículas | `matriculas` |

Funcionamiento:

- Cada petición tiene un tiempo máximo de espera (`<SERVICIO>_TIMEOUT`).
- Los timeouts, errores de conexión y respuestas **5xx** cuentan como fallo. Un **404** no cuenta (es una respuesta válida: el recurso no existe).
- Tras `CB_MAX_FALLOS` fallos consecutivos el circuito pasa a **OPEN** y las peticiones se rechazan de inmediato sin consultar al servicio caído.
- Pasados `CB_RECUPERACION` segundos el circuito pasa a **HALF_OPEN**: la siguiente petición se deja pasar; si tiene éxito el circuito vuelve a **CLOSED**, si falla vuelve a **OPEN**.
- Cada cambio de estado queda registrado en los logs del servicio, por ejemplo `[circuit breaker docentes] CLOSED -> OPEN`.

Configuración (valores del archivo `.env`):

| Parámetro | Cursos → Docentes | Matrículas → Estudiantes | Matrículas → Cursos | Notas → Matrículas |
| --- | --- | --- | --- | --- |
| Servicio que realiza la solicitud | Cursos | Matrículas | Matrículas | Notas |
| Servicio protegido | Docentes | Estudiantes | Cursos | Matrículas |
| Umbral de fallas (`CB_MAX_FALLOS`) | 3 | 3 | 3 | 3 |
| Tiempo de recuperación (`CB_RECUPERACION`) | 30 s | 30 s | 30 s | 30 s |
| Timeout configurado | `DOCENTES_TIMEOUT` = 2 s | `ESTUDIANTES_TIMEOUT` = 2 s | `CURSOS_TIMEOUT` = 2 s | `MATRICULAS_TIMEOUT` = 2 s |

Respuestas ante fallas del servicio consultado:

| Situación | Código HTTP |
| --- | --- |
| Circuito abierto | `503 Service Unavailable` |
| Tiempo de espera agotado | `504 Gateway Timeout` |
| No se pudo conectar | `503 Service Unavailable` |
| El servicio respondió 5xx | `502 Bad Gateway` |

Estado de los circuitos (también accesible a través del gateway en el puerto 8000):

- `GET /cursos/circuito`
- `GET /matriculas/circuito`
- `GET /notas/circuito`

Ejemplo de respuesta de `GET /cursos/circuito`:

```json
{
  "docentes": {
    "estado_circuito": "OPEN",
    "fallos_consecutivos": 3,
    "max_fallos": 3,
    "periodo_recuperacion": 30,
    "segundos_para_half_open": 30
  }
}
```

`pybreaker` solo cambia de OPEN a HALF_OPEN cuando llega una nueva petición. Por eso el endpoint informa `HALF_OPEN` en cuanto termina el periodo de recuperación: la siguiente petición será la de prueba.

#### Prueba del Timeout

`docker compose pause` congela el contenedor sin apagarlo: acepta la conexión pero nunca responde, lo que simula una respuesta lenta.

```bash
docker compose pause docentes-service
# Crear un curso: a los 2 segundos responde 504
#   {"error": "Gateway Timeout", "message": "Tiempo de espera agotado al consultar el servicio de docentes.", "status": 504}
docker compose unpause docentes-service
```

#### Prueba del Circuit Breaker y de recuperación

1. `GET /cursos/circuito` → estado inicial `CLOSED`.
2. `docker compose stop docentes-service`.
3. Crear un curso 3 veces → cada intento responde `503` *"No se pudo conectar con el servicio de docentes"* y `fallos_consecutivos` sube a 1, 2 y 3.
4. `GET /cursos/circuito` → `OPEN`.
5. Crear otro curso → `503` *"Circuito abierto: el servicio de docentes no será consultado"*, sin esperar respuesta de Docentes.
6. Mientras tanto, `GET /cursos` sigue funcionando: solo fallan las operaciones que necesitan a Docentes.
7. `docker compose start docentes-service` y esperar a que `segundos_para_half_open` llegue a 0 → `HALF_OPEN`.
8. Crear un curso → la petición de prueba llega a Docentes y el circuito vuelve a `CLOSED`.
9. `docker compose logs cursos-service` muestra las transiciones `CLOSED -> OPEN`, `OPEN -> HALF_OPEN` y `HALF_OPEN -> CLOSED`.

### Fallas en la base de datos

Una falla o pérdida de información en una base de datos puede generar inconsistencias debido a las referencias lógicas existentes entre los distintos servicios.

**Medidas propuestas:**

- Implementar **backups automáticos y periódicos**.
- Utilizar **réplicas de lectura** en los servicios con mayor volumen de consultas.
- Monitorear recursos como conexiones activas, espacio en disco y disponibilidad para detectar problemas antes de una caída total.

---

## API Gateway

El gateway es un contenedor **Nginx** independiente (`gateway/`), definido en `docker-compose.yml` y publicado en `http://localhost:8000`. Es el único punto de entrada que usa el cliente: la vista Home nunca llama directamente a los puertos de los servicios.

| Solicitud al Gateway | Servicio destino | Dirección interna |
| --- | --- | --- |
| `/` | Vista Home (archivos de `frontend/`) | `/usr/share/nginx/html` |
| `GET, POST /docentes` · `GET, PUT, DELETE /docentes/{id}` | Docentes | `http://docentes-service:5001` |
| `GET, POST /cursos` · `GET, PUT, DELETE /cursos/{id}` · `GET /cursos/circuito` | Cursos | `http://cursos-service:5002` |
| `GET, POST /estudiantes` · `GET, PUT, DELETE /estudiantes/{id}` | Estudiantes | `http://estudiantes-service:5003` |
| `GET, POST /matriculas` · `GET, PUT, DELETE /matriculas/{id}` · `GET /matriculas/circuito` | Matrículas | `http://matriculas-service:5004` |
| `GET, POST /notas` · `GET, PUT, DELETE /notas/{id}` · `GET /notas/circuito` | Notas | `http://notas-service:5005` |

Características (`gateway/nginx.conf`):

- Reenvía el método HTTP, el cuerpo, la respuesta y el código de estado sin modificarlos. No ejecuta consultas a las bases de datos ni repite la lógica de los servicios.
- Usa el DNS interno de Docker (`resolver 127.0.0.11`) para encontrar a cada servicio por su nombre, aunque su contenedor se haya recreado y cambiado de IP.
- Si no logra comunicarse con un servicio, responde en JSON en lugar de la página de error de Nginx:

```json
{"error": "Bad Gateway", "message": "El gateway no pudo comunicarse con el servicio solicitado.", "status": 502}
```

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
| `DOCENTES_TIMEOUT` | Segundos máximos de espera al consultar Docentes (usado por Cursos) |
| `CURSOS_TIMEOUT` | Segundos máximos de espera al consultar Cursos (usado por Matrículas) |
| `ESTUDIANTES_TIMEOUT` | Segundos máximos de espera al consultar Estudiantes (usado por Matrículas) |
| `MATRICULAS_TIMEOUT` | Segundos máximos de espera al consultar Matrículas (usado por Notas) |
| `CB_MAX_FALLOS` | Fallos consecutivos para abrir el circuit breaker |
| `CB_RECUPERACION` | Segundos que el circuito permanece abierto antes de volver a intentar |



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
El proyecto cuenta con un archivo `docker-compose.yml` que permite levantar todos los servicios y sus bases de datos de manera coordinada: 11 contenedores (gateway, 5 microservicios y 5 bases de datos), las variables de entorno leídas del archivo `.env`, los puertos y los volúmenes de persistencia.

Para ejecutarlo se debe utilizar el comando:
```bash
docker compose up -d --build
```

Para comprobar el estado de los contenedores:
```bash
docker compose ps
```

Luego se abre `http://localhost:8000` en el navegador.

| Contenedor | Puerto publicado | Puerto interno |
| --- | --- | --- |
| gateway | `8000` | `80` |
| docentes-service, cursos-service, estudiantes-service, matriculas-service, notas-service | `5001` a `5005` | `5001` a `5005` |
| docentes-db, cursos-db, estudiantes-db, matriculas-db, notas-db | `15433` a `15437` | `5432` |

### ¿Por qué no es necesario publicar todos los puertos?

Docker Compose crea una red interna en la que cada contenedor se encuentra por el nombre de su servicio. Por esa red los servicios se comunican entre sí (`http://docentes-service:5001`) y con sus bases de datos (`docentes-db:5432`), sin pasar por los puertos publicados. El cliente solo necesita el puerto `8000` del gateway.

Los puertos de los servicios (`5001` a `5005`) y de las bases de datos (`15433` a `15437`) se publican únicamente para pruebas durante el desarrollo, por ejemplo con Thunder Client o pgAdmin. En un despliegue real se podrían quitar, de modo que solo el gateway quede expuesto.

---

## Pruebas del sistema

Matriz de verificación. Las pruebas se realizaron a través del gateway (`http://localhost:8000`) con datos propios del proyecto. Las capturas de las evidencias se guardan en [`docs/pruebas`](docs/pruebas).

| Prueba | Resultado esperado | Resultado obtenido |
| --- | --- | --- |
| Arquitectura completa | Los 5 servicios del diseño están implementados | Cumple: docentes, cursos, estudiantes, matrículas y notas |
| Docker Compose | Los 11 contenedores en ejecución | Cumple: `docker compose ps` muestra todos en estado `Up` |
| CRUD Docentes | POST, GET, PUT, DELETE y 404 para un ID inexistente | Cumple |
| CRUD Cursos | POST, GET, PUT, DELETE y 404 para un ID inexistente | Cumple |
| CRUD Estudiantes | POST, GET, PUT, DELETE y 404 para un ID inexistente | Cumple |
| CRUD Matrículas | POST, GET, PUT, DELETE y 404 para un ID inexistente | Cumple |
| CRUD Notas | POST, GET, PUT, DELETE y 404 para un ID inexistente | Cumple |
| Bases de datos | Cada servicio guarda en su propia base y los datos persisten al recrear los contenedores | Cumple |
| Comunicación HTTP | Crear un curso, una matrícula o una nota con una referencia inexistente | Cumple: `400` con mensaje, por ejemplo `"El docente no existe."`, y no se guarda nada |
| Timeout | Error controlado cuando Docentes no responde | Cumple: `504` a los 2 segundos con `docentes-service` pausado |
| Circuit Breaker CLOSED | Las peticiones pasan y se cuentan los fallos | Cumple: `fallos_consecutivos` sube 1, 2, 3 |
| Circuit Breaker OPEN | Las peticiones se rechazan sin consultar al servicio caído | Cumple: `503` *"Circuito abierto"* inmediato |
| Circuit Breaker HALF_OPEN | Pasado el tiempo de recuperación se permite una petición de prueba | Cumple: `HALF_OPEN` a los 30 segundos |
| Recuperación | Con el servicio restablecido el circuito vuelve a CLOSED | Cumple: `CLOSED` y `fallos_consecutivos` en 0 |
| Gateway | Acceso a los 5 servicios desde el puerto 8000 | Cumple: además responde `502` en JSON si un servicio está detenido |
| Home | La vista usa datos reales de los microservicios | Cumple: resumen, tablas y formularios CRUD de los 5 módulos |

---

## Estado del proyecto

Proyecto académico orientado a aplicar conceptos de **sistemas distribuidos, microservicios, APIs REST, Docker y PostgreSQL**.

**Terminado:**

- 5 microservicios con CRUD completo y base de datos PostgreSQL propia.
- Validación entre servicios mediante HTTP.
- Manejo de errores HTTP, Timeout y Circuit Breaker con endpoint de monitoreo.
- API Gateway con Nginx para los 5 servicios y la vista Home.
- Vista Home con acceso a todas las operaciones CRUD a través del gateway.
- Ejecución completa con Docker Compose y persistencia en volúmenes.

**Pendiente:**

- Endpoint `/health` y reintentos exponenciales.
- Autenticación y permisos por rol (administrativo, docente, estudiante).
- Contenedor propio para la vista Home (hoy la sirve el gateway).
