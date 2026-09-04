from db import connect_db

#* Obtengo todos los estudiantes
def fetch_all_students():
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, cedula, nombre, correo, programa 
        FROM estudiante
    """
    cursor.execute(sql)    
        
    students = cursor.fetchall()
    lista = []
    
    for item in students:        
        # Aqui lo hago es guardar el diccionario en la variable estudiante
        estudiante = {
            'id': item[0],
            'cedula': item[1],
            'nombre': item[2],
            'correo': item[3],
            'programa': item[4],
        }            
        lista.append(estudiante)
    
    cursor.close()
    connection.close()
    
    return lista

#* Crear un estudiante
def create_new_student(data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO estudiante(cedula, nombre, correo, programa)
        VALUES (%s, %s, %s, %s)
    """
        
    cursor.execute(sql, (
        data.get('cedula'),
        data.get('nombre'),
        data.get('correo'),
        data.get('programa')
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
#* Obtener un estudiante por id
def fetch_student_by_id(student_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, cedula, nombre, correo, programa
        FROM estudiante
        WHERE id = %s
    """
    cursor.execute(sql,(student_id,))
    student = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not student:
        return None
    
    return {
        'id': student[0],
        'cedula': student[1],
        'nombre': student[2],
        'correo': student[3],
        'programa': student[4]
    }
    
#* Actualizar un estudiante por id
def update_student_by_id(student_id, data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        UPDATE estudiante
        SET cedula = %s, nombre = %s, correo = %s, programa = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data.get('cedula'),
        data.get('nombre'),
        data.get('correo'),
        data.get('programa'),
        student_id
    ))
    connection.commit()    
    
    cursor.close()
    connection.close()

#* Borrar un estudiante por id 
def delete_student_by_id(student_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "DELETE FROM estudiante WHERE id = %s"
    cursor.execute(sql, (student_id,))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    
    
    
    
    
    
    