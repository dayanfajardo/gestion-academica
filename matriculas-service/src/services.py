from db import connect_db

# * Consultamos todas las matriculas
def fetch_all_enrollments():
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, estudiante_id, curso_id, anio, periodo
        FROM matricula
    """
    cursor.execute(sql)
    enrollments = cursor.fetchall()
    
    lista = []
    for item in enrollments:
        lista.append({
            'id': item[0], 
            'estudiante_id': item[1], 
            'curso_id': item[2], 
            'anio': item[3], 
            'periodo': item[4]
        })
    
    cursor.close()
    connection.close()
    return lista

# * Creamos nueva matricula
def create_new_enrollment(data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO matricula (estudiante_id, curso_id, anio, periodo)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data.get('estudiante_id'),
        data.get('curso_id'),
        data.get('anio'),
        data.get('periodo')
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()

# * Buscamos una matricula por id
def fetch_enrollment_by_id(enrollment_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, estudiante_id, curso_id, anio, periodo
        FROM matricula
        WHERE id = %s
    """
    cursor.execute(sql, (enrollment_id,))
    enrollment = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not enrollment:
        return None    
    
    return {
        'id': enrollment[0],
        'estudiante_id': enrollment[1],
        'curso_id': enrollment[2],
        'anio': enrollment[3],
        'periodo': enrollment[4]
    }

# * Actualizamos matricula por id
def update_enrollment_by_id(enrollment_id, data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        UPDATE matricula
        SET estudiante_id = %s, curso_id = %s, anio = %s, periodo = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data.get('estudiante_id'),
        data.get('curso_id'),
        data.get('anio'),
        data.get('periodo'),
        enrollment_id
    ))
    connection.commit()
    
    cursor.close()
    connection.close()

# * Eliminamos matricula por id
def delete_enrollment_by_id(enrollment_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "DELETE FROM matricula WHERE id = %s"
    cursor.execute(sql, (enrollment_id,))
    
    connection.commit()
    
    cursor.close()
    connection.close()