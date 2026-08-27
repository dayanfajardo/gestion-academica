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
...

## Usuarios del sistema
...

## Riesgos y fallas posibles
...
