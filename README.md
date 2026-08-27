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
- 
- 
- 

## Comunicación entre servicios
...

## Tipo de arquitectura
microservicios
Se eligió una arquitectura basada en microservicios porque, aunque el sistema no es demasiado grande, tiene diferentes partes del negocio que están bien separadas y que no tienen el mismo nivel de uso. Por ejemplo..   
                    

## Base de datos
...

## Usuarios del sistema
...

## Riesgos y fallas posibles
...
