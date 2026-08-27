# Arquitectura del Sistema: [Nombre del Proyecto]

## Problema que resuelve
¿Qué problema resuelve el sistema?
El sistema resuelve la necesidad de centralizar y automatizar la gestión académica de una institución educativa, que sin él tendría que manejarse de forma manual, dispersa o en hojas de cálculo/sistemas aislados.  
Concretamente resuelve:
La desconexión entre los distintos procesos académicos (docentes, cursos, estudiantes, matrículas y notas), integrándolos bajo una arquitectura común accesible vía API
La escalabilidad y mantenibilidad del software académico: al ser microservicios independientes, cada dominio (docentes, cursos, etc.) puede crecer, desplegarse y mantenerse sin afectar a los demás, algo que un sistema monolítico tradicional no permite fácilmente. 
¿Quién lo usará?
Personal administrativo/académico: para registrar docentes, crear cursos y gestionar matrículas.
Docentes: consultando o gestionando información de los cursos que dictan (y potencialmente registrando notas). 
Estudiantes: consultando sus matrículas, cursos inscritos y calificaciones. 
¿Qué pasaría si no existiera?
Sin este sistema, la institución tendría que depender de procesos manuales o herramientas no integradas que generaría la gestión manual y propensa a errores, procesos lentos y poco escalables, mayor riesgo de inconsistencia de datos.


## Servicios del sistema
Los principales servicios del sistema de gestión académica son:

1. **Docentes**: Gestiona la información de los profesores: cédula, nombre, correo, departamento y género. Es el punto de partida de la relación académica, ya que cada curso depende de un docente responsable.
2. **Cursos**: Administra los cursos ofrecidos (código, nombre, créditos, semestre).
3. **Estudiantes**: Gestiona los datos de los estudiantes matriculados en el sistema: cédula, nombre, correo y programa académico al que pertenecen.
4. **Matrículas**: Gestiona la matrícula que hacen los estudiantes.
5. **Notas**: Almacena las calificaciones asociadas a cada matrícula.

### ¿Qué partes pueden trabajar por separado?

Cada microservicio es independiente en su desarrollo porque tiene su propia base de datos, su propia lógica de negocio y cada uno va a tener su propio contenedor Docker.

### ¿Qué procesos son independientes?

- El proceso de **despliegue** de cada microservicio es independiente, debido a que cada uno cuenta con su propio Dockerfile.
- El proceso de **modelado de base de datos** de cada uno de ellos es independiente y no existe un bloqueo mutuo.
- El proceso de **pruebas** para cada microservicio se puede dar de manera aislada e independiente.

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
        ┌─────────┐ ┌─────────┐ ┌───────────┐ ┌──────────┐ ┌─────────┐
        │Docentes │ │ Cursos  │ │Estudiante │ │Matrículas│ │  Notas  │
        │ Service │ │ Service │ │ Service   │ | Service  │ │ Service │
        └────┬────┘ └────┬────┘ └────┬──────┘ └────┬─────┘ └────┬────┘
             │           │           │             │            │
             ▼           ▼           ▼             ▼            ▼
        PostgreSQL  PostgreSQL   PostgreSQL   PostgreSQL     PostgreSQL


```
## Comunicación entre servicios
...

## Tipo de arquitectura
microservicios
Se eligió una arquitectura basada en microservicios porque, aunque el sistema no es demasiado grande, tiene diferentes partes del negocio que están bien separadas y que no tienen el mismo nivel de uso. Por ejemplo, las matrículas y las notas pueden tener mucha más actividad en ciertos periodos del año. Con microservicios podemos escalar de forma independiente las partes que más lo necesiten y, si una falla, no necesariamente afecta a todo el sistema.
No se escogió una arquitectura en capas porque, al estar todo más centralizado, sería necesario escalar gran parte del sistema aunque solo una sección tuviera mucha carga. Tampoco se eligió una arquitectura completamente basada en eventos, porque agregaría una complejidad de comunicación y mensajería que no es necesaria para un sistema donde la mayoría de las operaciones son CRUD. Finalmente, se descartó el modelo cliente-servidor tradicional porque no permite tener tanta independencia para desplegar y manejar cada parte del sistema por separado   

## Base de datos
### ¿Qué información debe guardarse?

A continuación se presentan los datos que necesitamos para cada microservicio:

- **Docentes**: Id, cédula (identificación única), nombre, correo institucional, departamento, género (opcional).
- **Cursos**: Id, código único, nombre, número de créditos, semestre, y el `docente_id` que lo dicta.
- **Estudiantes**: Id, cédula, nombre, correo institucional, programa académico.
- **Matrículas**: Id, `estudiante_id`, `curso_id`, año lectivo, periodo.
- **Notas**: Id, `matricula_id`, calificación, observación opcional.

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


### ¿Qué datos son críticos?

1. **Cédula** (docente y estudiante): Es único y no editable; identifica legalmente a la persona. Si se duplica o se pierde, se rompe la trazabilidad académica.
2. **docente_id** (Curso): Sin este dato, un curso queda sin responsable.
3. **estudiante_id y curso_id** (Matrícula): Son las llaves lógicas que conectan nuestro sistema; perder esto rompe la relación estudiante-curso.
4. **matricula_id** (Nota): Sin este vínculo, una calificación queda sin dueño.
5. **Calificación**: Es el dato final que certifica el rendimiento académico.

### ¿Qué pasaría si se pierden?

Al tener bases de datos separadas, la pérdida de algún dato no necesariamente tumba los demás servicios, pero sí se pueden presentar inconsistencias en la lógica de nuestro sistema, por ejemplo:

1. **Se pierden Docentes**: Los cursos quedan con un `docente_id` que ya no existe.
2. **Se pierden Estudiantes**: Las matrículas quedan con `estudiante_id` huérfanos.
3. **Se pierden Cursos**: El estudiante tiene una nota, pero no se podría saber en qué materia.
4. **Se pierden Notas**: Se pierde el historial académico.

## Usuarios del sistema
...

## Riesgos y fallas posibles
### Fallas en un servicio (ejemplo: servicio de Notas)

Si se presentan fallas, por ejemplo, en el servicio de Notas, las demás funcionalidades (matricular, consultar docentes/cursos) siguen funcionando, pero cualquier operación que dependa de Notas (consultar calificaciones) fallará: el Gateway enruta la petición, pero no se obtendría respuesta.

**Solución:**

- Implementar un endpoint `/health` en cada servicio; de esta forma el Gateway sabrá qué servicios se encuentran disponibles.
- Si el servicio se está reiniciando y no está caído, se necesitaría la implementación de **reintentos exponenciales**, en donde se esperaría cada vez más tiempo entre cada intento fallido de conexión.

### Fallas en la base de datos

Si hay fallos en la base de datos se generarían inconsistencias en la lógica de nuestro sistema, ya que se pierden referencias a datos que se encuentran en las demás bases de datos.

**Solución:**

- Implementar backups automáticos y periódicos.
- Réplicas de lectura en los servicios más consultados, de modo que si la instancia principal falla pueda responder una réplica.
- Monitorear los recursos de nuestras bases de datos (conexiones activas, espacio en disco, etc.) para detectar problemas antes de que se vuelvan caídas totales.
