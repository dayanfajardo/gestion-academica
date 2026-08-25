from db import connect_db

#* 1. Obtengo todos los docentes
def fetch_all_teachers():
    
  connection = connect_db()
  cursor = connection.cursor()

  cursor.execute(
      'SELECT id, cedula, nombre, correo, departamento, genero FROM docente'
  )
  teachers = cursor.fetchall()

  lista = [
      {
          'id': item[0],
          'cedula': item[1],
          'nombre': item[2],
          'correo': item[3],
          'departamento': item[4],
          'genero': item[5],
      }
      for item in teachers
  ]

  cursor.close()
  connection.close()
  return lista

#* 2. Obtengo por id
def fetch_teacher_by_id(teacher_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
      SELECT id, cedula, nombre, correo, departamento, genero 
      FROM docente 
      WHERE id = %s    
    """
        
    cursor.execute(sql, (teacher_id,))
    teacher = cursor.fetchone()
    
    cursor.close()
    connection.close()
    

    if not teacher:
        return None
        
    return {
        'id': teacher[0],
        'cedula': teacher[1],
        'nombre': teacher[2],
        'correo': teacher[3],
        'departamento': teacher[4],
        'genero': teacher[5]
    }
    
#* 3 Crear docente:
def create_new_teacher(data):
    # Obtengo los datos del cliente, importante
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO docente (cedula, nombre, correo, departamento, genero) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(sql, (
        data.get('cedula'), 
        data.get('nombre'), 
        data.get('correo'), 
        data.get('departamento'), 
        data.get('genero')
    ))
    connection.commit()  
    
    cursor.close()
    connection.close()  
    
#* 4. Actualizar docente
    # Esta función recibe dos parámetros:
    # teacher_id -> el ID del docente que queremos actualizar.
    # data -> contiene los nuevos datos del docente,    
    #"Voy a crear una función llamada update_teacher_by_id que necesita recibir dos datos."
def update_teacher_by_id(teacher_id, data):
    
    connection = connect_db()
    cursor = connection.cursor()
    sql = """
        UPDATE docente 
        SET cedula  = %s, nombre = %s, correo = %s, departamento = %s, genero = %s
        WHERE id = %s
    """
    
    # Ejecutamos la consulta SQL y enviamos los valores
    # que reemplazarán los %s de la consulta.
    cursor.execute(sql, (
        data.get('cedula'),        # Nuevo número de cédula
        data.get('nombre'),        # Nuevo nombre
        data.get('correo'),        # Nuevo correo
        data.get('departamento'),  # Nuevo departamento
        data.get('genero'),        # Nuevo género
        teacher_id                 # ID del docente que queremos modificar
    ))
    connection.commit()
 
    cursor.close()
    connection.close()
    

#* Elimino docente
def delete_teacher_by_id(teacher_id):
  connection = connect_db()
  cursor = connection.cursor()

  sql = 'DELETE FROM docente WHERE id = %s'
  cursor.execute(sql, (teacher_id,))
  connection.commit()

  cursor.close()
  connection.close()
