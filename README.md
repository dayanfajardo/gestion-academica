#  Sistema Académico Distribuido

##  Descripción

Los principales dominios gestionados son:

* Docentes
* Cursos
* Estudiantes
* Matrículas
* Notas

La comunicación entre los diferentes componentes se realiza mediante **APIs REST**, mientras que el acceso externo al sistema se centraliza mediante un **API Gateway**.

---

#  Arquitectura del Sistema

El sistema utiliza una arquitectura basada en **microservicios**, donde cada servicio se encarga de una funcionalidad específica.

```text
                         ┌─────────────────────┐
                         │       Cliente       │
                         │  Frontend / Postman │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │      API Gateway    │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │           │          │          │           │
             ▼           ▼          ▼          ▼           ▼
        ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
        │Docentes │ │ Cursos  │ │Estudiant│ │Matrículas│ │  Notas  │
        │ Service │ │ Service │ │ Service │ │ Service │ │ Service │
        └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
             │           │          │          │           │
             ▼           ▼          ▼          ▼           ▼
        PostgreSQL  PostgreSQL PostgreSQL PostgreSQL PostgreSQL
```

---

# 🗄️ Modelo de Datos y Dominio

Cada microservicio administra una entidad principal dentro del dominio académico.

| Microservicio             | Entidad      | Atributos principales                                               | Descripción                                               |
| :------------------------ | :----------- | :------------------------------------------------------------------ | :-------------------------------------------------------- |
| **`docentes-service`**    | `docente`    | `id` (PK), `cedula`, `nombre`, `correo`, `departamento`, `genero`   | Registro y gestión del cuerpo docente.                    |
| **`cursos-service`**      | `curso`      | `id` (PK), `codigo`, `nombre`, `creditos`, `semestre`, `docente_id` | Catálogo de asignaturas académicas y docente responsable. |
| **`estudiantes-service`** | `estudiante` | `id` (PK), `cedula`, `nombre`, `correo`, `carrera`                  | Registro y gestión de los estudiantes.                    |
| **`matriculas-service`**  | `matricula`  | `id` (PK), `estudiante_id`, `curso_id`, `fecha`                     | Gestión de la inscripción de estudiantes en cursos.       |
| **`notas-service`**       | `nota`       | `id` (PK), `matricula_id`, `calificacion`, `porcentaje`             | Registro y seguimiento de las calificaciones académicas.  |

> **Nota:** Las relaciones entre microservicios se manejan mediante identificadores (`ID`) y comunicación a través de APIs. No se utilizan claves foráneas físicas entre bases de datos pertenecientes a diferentes microservicios.

---

# Relaciones del Sistema

Las principales relaciones del dominio académico son las siguientes:

## Docente → Curso

```text
Docente (1) ─────────── (N) Curso
```

Un docente puede impartir múltiples cursos.

Cada curso tiene asociado un docente responsable mediante el atributo:

```text
docente_id
```

Este identificador permite establecer la relación lógica entre `docente` y `curso`.

---

## Estudiante ↔ Curso

```text
Estudiante (N) ─────────── (M) Curso
```

Un estudiante puede matricularse en múltiples cursos y un curso puede tener múltiples estudiantes.

Debido a que esta relación es de tipo **N:M**, se utiliza la entidad `matricula` como entidad intermedia.

```text
┌──────────────┐
│  Estudiante  │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│  Matrícula   │
└──────┬───────┘
       │
       │ N:1
       ▼
┌──────────────┐
│    Curso     │
└──────────────┘
```

La entidad `matricula` almacena los identificadores:

```text
estudiante_id
curso_id
```

permitiendo identificar qué estudiante está inscrito en qué curso.

---

##  Matrícula → Nota

```text
Matrícula (1) ─────────── (N) Nota
```

Una matrícula puede tener múltiples registros de notas correspondientes a diferentes evaluaciones o actividades académicas.

La relación se establece mediante:

```text
matricula_id
```

De esta manera, cada nota queda asociada a una matrícula específica.

---



# Arquitectura Interna de los Microservicios

Cada microservicio utiliza una estructura modular basada en diferentes capas.

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

## Responsabilidad de cada componente

| Archivo / Componente   | Responsabilidad                                                                                     |
| :--------------------- | :-------------------------------------------------------------------------------------------------- |
| **`app.py`**           | Punto de entrada y configuración principal de la aplicación Flask.                                  |
| **`src/routes.py`**    | Define los endpoints HTTP utilizando `Blueprints`. Recibe las peticiones y devuelve las respuestas. |
| **`src/services.py`**  | Contiene la lógica de negocio y las operaciones SQL necesarias para gestionar los datos.            |
| **`db.py`**            | Gestiona la conexión con PostgreSQL mediante `psycopg2-binary`.                                     |
| **`requirements.txt`** | Contiene las dependencias necesarias para ejecutar el microservicio.                                |
| **`Dockerfile`**       | Define la configuración necesaria para construir la imagen Docker del microservicio.                |

---

# Tecnologías Utilizadas

| Tecnología          | Uso                                               |
| :------------------ | :------------------------------------------------ |
| **Python**          | Lenguaje principal de desarrollo.                 |
| **Flask**           | Framework utilizado para construir las APIs REST. |
| **PostgreSQL**      | Sistema gestor de bases de datos.                 |
| **psycopg2-binary** | Conector entre Python y PostgreSQL.               |
| **Docker**          | Contenerización de los microservicios.            |
| **Docker Compose**  | Orquestación de los contenedores.                 |
| **API Gateway**     | Enrutamiento centralizado de las solicitudes.     |

---

