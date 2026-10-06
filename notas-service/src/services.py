from db import connect_db


#* Obtener todas las notas
def fetch_all_grades():
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        SELECT id, matricula_id, calificacion, observacion
        FROM nota
    """
    
    cursor.execute(sql)
    grade = cursor.fetchall()
    
    lista = []
    
    for item in grade:
        lista.append({
            'id': item[0],
            'matricula_id': item[1],
            'calificacion': item[2],
            'observacion': item[3]
        })
    
    cursor.close()
    connection.close()
    return lista

#* Crear nueva nota
def create_new_grade(data):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO nota (matricula_id, calificacion, observacion)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (
        data.get('matricula_id'),
        data.get('calificacion'),
        data.get('observacion')
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
#* Buscamos una nota por id
def fetch_grade_by_id(grade_id):

    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
       SELECT id, matricula_id, calificacion, observacion
       FROM nota
       WHERE id = %s
    """
    cursor.execute(sql, (grade_id,))
    grade = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not grade:
        return None
    return {
        'id': grade[0],
        'matricula_id': grade[1],
        'calificacion': grade[2],
        'observacion': grade[3]
    }
    
#* Actualizamos nota por id
def update_grade_by_id(grade_id, data):
    
    connection = connect_db()
    cursor = connection.cursor()    
    
    sql = """
        UPDATE nota
        SET matricula_id = %s, calificacion = %s, observacion = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data.get('matricula_id'),
        data.get('calificacion'),
        data.get('observacion'),
        grade_id
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()

#* Eliminamos por id
def delete_grade_by_id(grade_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "DELETE FROM nota WHERE id = %s"
    
    cursor.execute(sql, (grade_id,))
    connection.commit()
    
    cursor.close()
    connection.close()