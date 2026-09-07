# Arquitectura del Sistema: Sistema Académico Distribuido

##  Objetivo del Proyecto
El propósito principal de este proyecto es diseñar e implementar una plataforma integral para la administración de procesos académicos universitarios, facilitando el control y seguimiento de docentes, cursos, estudiantes, matrículas y calificaciones.

Para lograrlo, el sistema adopta un enfoque modular basado en microservicios, buscando resolver las necesidades clave del entorno educativo:
* **Autonomía y escalabilidad:** Desacoplar cada área funcional (Docentes, Cursos, Estudiantes, Matrículas y Notas) para que puedan evolucionar y mantenerse de forma independiente.
* **Punto de acceso unificado:** Centralizar todas las peticiones de los clientes a través de un API Gateway, garantizando una comunicación ordenada y segura.
* **Aislamiento de datos:** Respaldar cada servicio con su propia base de datos PostgreSQL, asegurando la integridad y disponibilidad de la información sin dependencias directas entre módulos.






 Integrantes y Roles

| Integrante | Rol en el Proyecto | Responsabilidades Principales |
| :--- | :--- | :--- |
| Olver Edinson Arenas Vásquez | Desarrollador | Implementación de microservicios y documentación técnica |
| Dayan Fajardo | Administrador / DevOps | Gestión del repositorio, control de versiones y revisiones |
| daniel fernandez | Desarrollador | Desarrollo de microservicios y lógica de negocio |
| cristian giron | Desarrollador | Pruebas de integración, endpoints y soporte en base de datos |






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




 Problema que resuelve
El sistema resuelve la necesidad de centralizar y automatizar la gestión académica de una institución educativa, que sin él tendría que manejarse de forma manual, dispersa o en hojas de cálculo/sistemas aislados.  
Concretamente resuelve:
La desconexión entre los distintos procesos académicos (docentes, cursos, estudiantes, matrículas y notas), integrándose bajo una arquitectura común accesible vía API
La escalabilidad y mantenibilidad del software académico: al ser microservicios independientes, cada dominio (docentes, cursos, etc.) puede crecer, desplegarse y mantenerse sin afectar a los demás, algo que un sistema monolítico tradicional no permite fácilmente.

¿Quién lo usará?
Personal administrativo/académico: para registrar docentes, crear cursos y gestionar matrículas.
Docentes: consultando o gestionando información de los cursos que dictan (y potencialmente registrando notas).
Estudiantes: consultando sus matrículas, cursos inscritos y calificaciones.
¿Qué pasaría si no existiera?
Sin este sistema, la institución tendría que depender de procesos manuales o herramientas no integradas que generaría la gestión manual y propensa a errores, procesos lentos y poco escalables, mayor riesgo de inconsistencia de datos.


 Servicios del sistema
- 
- 
- 

 Comunicación entre servicios
...

## Tipo de arquitectura
Se eligió la arquitectura de microservicios porque permite dividir el sistema en servicios independientes, facilitando el mantenimiento y el crecimiento según la demanda. Además, cada módulo puede escalar o actualizarse sin afectar el funcionamiento de los demás. No se eligieron otras arquitecturas porque son menos flexibles para un sistema académico con múltiples procesos.

 Modelo de Datos y Dominio

 1. Servicio de Docentes (`docentes-service`)

 Tabla: `docente`

### ¿Qué procesos son independientes?



 2. Servicio de Cursos (`cursos-service`)

 Tabla: `curso`

A su vez hay casos donde un servicio necesita **comunicarse directamente con otro** para validar o completar información, ya que las claves no son solo lógicas osea que no existe una base de datos compartida como Por ejemplo:



 3. Servicio de Estudiantes (`estudiantes-service`)

 Tabla: `estudiante`

### ¿Qué pasa si el servicio consultado no responde?



 4. Servicio de Matrículas (`matriculas-service`)

Tabla: `matricula`

Se eligió la arquitectura de microservicios porque permite dividir el sistema en servicios independientes, facilitando el mantenimiento y el crecimiento según la demanda. Además, cada módulo puede escalar o actualizarse sin afectar el funcionamiento de los demás. No se eligieron otras arquitecturas porque son menos flexibles para un sistema académico con múltiples procesos.



 5. Servicio de Notas (`notas-service`)

 Tabla: `nota`

...


### ¿Qué información debe guardarse?


 Relaciones del Sistema

- **Docentes**: Id, cédula (identificación única), nombre, correo institucional, departamento, género (opcional).
- **Cursos**: Id, código único, nombre, número de créditos, semestre, y el `docente_id` que lo dicta.
- **Estudiantes**: Id, cédula, nombre, correo institucional, programa académico.
- **Matrículas**: Id, `estudiante_id`, `curso_id`, año lectivo, periodo.
- **Notas**: Id, `matricula_id`, calificación, observación opcional.

 Docente → Curso

**Tabla:** `docente`

| Campo          | Tipo de Dato   | Restricciones / Reglas               |
| -------------- | -------------- | ------------------------------------ |
| `id`           | `INTEGER`      | Primary Key, Autogenerado (`SERIAL`) |
| `cedula`       | `VARCHAR(20)`  | `NOT NULL`, `UNIQUE`                 |
| `nombre`       | `VARCHAR(100)` | `NOT NULL`                           |
| `correo`       | `VARCHAR(100)` | `NOT NULL`, `UNIQUE`                 |
| `departamento` | `VARCHAR(100)` | `NOT NULL`                           |
| `genero`       | `VARCHAR(20)`  | Opcional                             |

---

### 2. Servicio de Cursos (`cursos-service`)

**Tabla:** `curso`

| Campo        | Tipo de Dato   | Restricciones / Reglas               |
| ------------ | -------------- | ------------------------------------ |
| `id`         | `INTEGER`      | Primary Key, Autogenerado (`SERIAL`) |
| `codigo`     | `VARCHAR(20)`  | `NOT NULL`, `UNIQUE`                 |
| `nombre`     | `VARCHAR(100)` | `NOT NULL`                           |
| `creditos`   | `INTEGER`      | `NOT NULL`                           |
| `semestre`   | `INTEGER`      | `NOT NULL`                           |
| `docente_id` | `INTEGER`      | `NOT NULL` (Clave foránea lógica)    |



### 3. Servicio de Estudiantes (`estudiantes-service`)

**Tabla:** `estudiante`

| Campo      | Tipo de Dato   | Restricciones / Reglas               |
| ---------- | -------------- | ------------------------------------ |
| `id`       | `INTEGER`      | Primary Key, Autogenerado (`SERIAL`) |
| `cedula`   | `VARCHAR(20)`  | `NOT NULL`, `UNIQUE`                 |
| `nombre`   | `VARCHAR(100)` | `NOT NULL`                           |
| `correo`   | `VARCHAR(100)` | `NOT NULL`, `UNIQUE`                 |
| `programa` | `VARCHAR(100)` | `NOT NULL`                           |

---

### 4. Servicio de Matrículas (`matriculas-service`)

**Tabla:** `matricula`

| Campo           | Tipo de Dato  | Restricciones / Reglas               |
| --------------- | ------------- | ------------------------------------ |
| `id`            | `INTEGER`     | Primary Key, Autogenerado (`SERIAL`) |
| `estudiante_id` | `INTEGER`     | `NOT NULL` (Clave foránea lógica)    |
| `curso_id`      | `INTEGER`     | `NOT NULL` (Clave foránea lógica)    |
| `anio`          | `INTEGER`     | `NOT NULL` (Año lectivo)             |
| `periodo`       | `VARCHAR(10)` | `NOT NULL` (Ej: '1', '2', '2026-1')  |



  Matrícula → Nota

**Tabla:** `nota`

| Campo          | Tipo de Dato   | Restricciones / Reglas               |
| -------------- | -------------- | ------------------------------------ |
| `id`           | `INTEGER`      | Primary Key, Autogenerado (`SERIAL`) |
| `matricula_id` | `INTEGER`      | `NOT NULL` (Clave foránea lógica)    |
| `calificacion` | `NUMERIC(3,2)` | `NOT NULL` (Ej: 4.50)                |
| `observacion`  | `VARCHAR(200)` | Opcional                             |

### ¿Qué datos son críticos?

1. **Cédula** (docente y estudiante): Es único y no editable; identifica legalmente a la persona. Si se duplica o se pierde, se rompe la trazabilidad académica.
2. **docente_id** (Curso): Sin este dato, un curso queda sin responsable.
3. **estudiante_id y curso_id** (Matrícula): Son las llaves lógicas que conectan nuestro sistema; perder esto rompe la relación estudiante-curso.
4. **matricula_id** (Nota): Sin este vínculo, una calificación queda sin dueño.
5. **Calificación**: Es el dato final que certifica el rendimiento académico.

### ¿Qué pasaría si se pierden?


1. **Se pierden Docentes**: Los cursos quedan con un `docente_id` que ya no existe.
2. **Se pierden Estudiantes**: Las matrículas quedan con `estudiante_id` huérfanos.
3. **Se pierden Cursos**: El estudiante tiene una nota, pero no se podría saber en qué materia.
4. **Se pierden Notas**: Se pierde el historial académico.

## Usuarios del sistema


 Arquitectura Interna de los Microservicios

| Usuario                      | Descripción                                          | Acciones principales                                                              |
| ---------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Administrativo/Académico** | Personal encargado de la gestión general del sistema | Registrar docentes, crear cursos, gestionar matrículas                            |
| **Docente**                  | Profesor responsable de uno o más cursos             | Consultar/gestionar información de sus cursos, registrar notas de sus estudiantes |
| **Estudiante**               | Usuario matriculado en uno o más cursos              | Consultar sus matrículas, cursos inscritos y calificaciones                       |

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

 Responsabilidad de cada componente

No. Aunque todos ingresan a través del mismo **API Gateway**, el nivel de acceso depende del rol: un estudiante solo debería poder **consultar** su propia información (matrículas y notas), mientras que el personal administrativo y los docentes tienen permisos para **crear y modificar** datos (cursos, matrículas, notas, según corresponda a su rol).



### Fallas en un servicio (ejemplo: servicio de Notas)

Si se presentan fallas, por ejemplo, en el servicio de Notas, las demás funcionalidades (matricular, consultar docentes/cursos) siguen funcionando, pero cualquier operación que dependa de Notas (consultar calificaciones) fallará: el Gateway enruta la petición, pero no se obtendría respuesta.


- Implementar un endpoint `/health` en cada servicio; de esta forma el Gateway sabrá qué servicios se encuentran disponibles.
- Si el servicio se está reiniciando y no está caído, se necesitaría la implementación de **reintentos exponenciales**, en donde se esperaría cada vez más tiempo entre cada intento fallido de conexión.




Si hay fallos en la base de datos se generarían inconsistencias en la lógica de nuestro sistema, ya que se pierden referencias a datos que se encuentran en las demás bases de datos.

**Solución:**

- Implementar backups automáticos y periódicos.
- Réplicas de lectura en los servicios más consultados, de modo que si la instancia principal falla pueda responder una réplica.
- Monitorear los recursos de nuestras bases de datos (conexiones activas, espacio en disco, etc.) para detectar problemas antes de que se vuelvan caídas totales.
