from db import connect_db

#* Obtenemos todos los cursos
def fetch_all_courses():
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, codigo, nombre, creditos, semestre, docente_id 
        FROM curso
    """
    
    cursor.execute(sql)
    courses = cursor.fetchall()
    
    lista = []
    
    for item in courses:
    
        lista.append({
                'id': item[0],
                'codigo': item[1],
                'nombre': item[2],
                'creditos': item[3],
                'semestre': item[4],
                'docente_id': item[5]
            })                
        

    cursor.close()
    connection.close()
    return lista

#* Creamos un nuevo curso
def create_new_course(data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO curso (codigo, nombre, creditos, semestre, docente_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data.get('codigo'),
        data.get('nombre'),
        data.get('creditos'),
        data.get('semestre'),
        data.get('docente_id')
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
#* Buscamos un curso por id
def fetch_course_by_id(course_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, codigo, nombre, creditos, semestre, docente_id
        FROM curso
        WHERE id = %s
    """
    cursor.execute(sql, (course_id,))
    course = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not course:
        return None
    
    return {
        'id': course[0],
        'codigo': course[1],
        'nombre': course[2],
        'creditos': course[3],
        'semestre': course[4],
        'docente_id': course[5],
    }
    
#* Actualizar curso
def update_course_by_id(course_id, data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        UPDATE curso 
        SET codigo = %s, nombre = %s, creditos = %s, semestre = %s, docente_id = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data.get('codigo'),
        data.get('nombre'),
        data.get('creditos'),
        data.get('semestre'),
        data.get('docente_id'),
        course_id       
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()

#* Borrar curso por id    
def delete_course_by_id(course_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "DELETE FROM curso WHERE id = %s"
    cursor.execute(sql,(course_id,))
    connection.commit()
    
        
    cursor.close()
    connection.close()
    



