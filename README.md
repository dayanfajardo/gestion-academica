# gestion-academica
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

# Modelo de Datos y Dominio

### 1. Servicio de Docentes (`docentes-service`)

**Tabla:** `docente`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `departamento` | `VARCHAR(100)` | `NOT NULL` |
| `genero` | `VARCHAR(20)` | Opcional |

---

### 2. Servicio de Cursos (`cursos-service`)

**Tabla:** `curso`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `codigo` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `creditos` | `INTEGER` | `NOT NULL` |
| `semestre` | `INTEGER` | `NOT NULL` |
| `docente_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |

---

### 3. Servicio de Estudiantes (`estudiantes-service`)

**Tabla:** `estudiante`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `programa` | `VARCHAR(100)` | `NOT NULL` |

---

### 4. Servicio de Matrículas (`matriculas-service`)

**Tabla:** `matricula`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `estudiante_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `curso_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `anio` | `INTEGER` | `NOT NULL` (Año lectivo) |
| `periodo` | `VARCHAR(10)` | `NOT NULL` (Ej: '1', '2', '2026-1') |

---

### 5. Servicio de Notas (`notas-service`)

**Tabla:** `nota`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `matricula_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `calificacion` | `NUMERIC(3,2)` | `NOT NULL` (Ej: 4.50) |
| `observacion` | `VARCHAR(200)` | Opcional |

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

# gestion-academica
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

# Modelo de Datos y Dominio

### 1. Servicio de Docentes (`docentes-service`)

**Tabla:** `docente`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `departamento` | `VARCHAR(100)` | `NOT NULL` |
| `genero` | `VARCHAR(20)` | Opcional |

---

### 2. Servicio de Cursos (`cursos-service`)

**Tabla:** `curso`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `codigo` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `creditos` | `INTEGER` | `NOT NULL` |
| `semestre` | `INTEGER` | `NOT NULL` |
| `docente_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |

---

### 3. Servicio de Estudiantes (`estudiantes-service`)

**Tabla:** `estudiante`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `cedula` | `VARCHAR(20)` | `NOT NULL`, `UNIQUE` |
| `nombre` | `VARCHAR(100)` | `NOT NULL` |
| `correo` | `VARCHAR(100)` | `NOT NULL`, `UNIQUE` |
| `programa` | `VARCHAR(100)` | `NOT NULL` |

---

### 4. Servicio de Matrículas (`matriculas-service`)

**Tabla:** `matricula`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `estudiante_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `curso_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `anio` | `INTEGER` | `NOT NULL` (Año lectivo) |
| `periodo` | `VARCHAR(10)` | `NOT NULL` (Ej: '1', '2', '2026-1') |

---

### 5. Servicio de Notas (`notas-service`)

**Tabla:** `nota`

| Campo | Tipo de Dato | Restricciones / Reglas |
| --- | --- | --- |
| `id` | `INTEGER` | Primary Key, Autogenerado (`SERIAL`) |
| `matricula_id` | `INTEGER` | `NOT NULL` (Clave foránea lógica) |
| `calificacion` | `NUMERIC(3,2)` | `NOT NULL` (Ej: 4.50) |
| `observacion` | `VARCHAR(200)` | Opcional |

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

