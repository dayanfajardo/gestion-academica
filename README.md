# Arquitectura del Sistema: Sistema Académico Distribuido

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

## Problema que resuelve
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


## Servicios del sistema
- 
- 
- 

## Comunicación entre servicios
...

## Tipo de arquitectura
Se eligió la arquitectura de microservicios porque permite dividir el sistema en servicios independientes, facilitando el mantenimiento y el crecimiento según la demanda. Además, cada módulo puede escalar o actualizarse sin afectar el funcionamiento de los demás. No se eligieron otras arquitecturas porque son menos flexibles para un sistema académico con múltiples procesos.

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

...

## Base de datos
...

## Usuarios del sistema
...

## Riesgos y fallas posibles
...
