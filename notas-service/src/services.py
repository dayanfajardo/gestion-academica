import requests
import os

from db import connect_db

MATRICULAS_SERVICE_URL = os.getenv('MATRICULAS_SERVICE_URL')

def enrollment_exists(enrollment_id):
    url = f"{MATRICULAS_SERVICE_URL}/matriculas/{enrollment_id}"
    response = requests.get(url, timeout=5)
    
    return response.status_code == 200 

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
            'calificacion': float(item[2]),
            'observacion': item[3]
        })
    
    cursor.close()
    connection.close()
    return lista

#* Crear nueva nota
def create_new_grade(data):
    
    #Aqui guardo el id de matricula
    enrollment_id = data.get('matricula_id')
    
    if not enrollment_exists(enrollment_id):
        return 'enrollment_not_found'
        
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """
        INSERT INTO nota (matricula_id, calificacion, observacion)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (
        enrollment_id,
        data.get('calificacion'),
        data.get('observacion')
    ))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return 'created'
    
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
        'calificacion': float(grade[2]),
        'observacion': grade[3]
    }
    
#* Actualizamos nota por id
def update_grade_by_id(grade_id, data):

    enrollment_id = data.get('matricula_id')

    if not enrollment_exists(enrollment_id):
        return 'enrollment_not_found'
    
    connection = connect_db()
    cursor = connection.cursor()    
    
    sql = """
        UPDATE nota
        SET matricula_id = %s, calificacion = %s, observacion = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        enrollment_id,
        data.get('calificacion'),
        data.get('observacion'),
        grade_id
    ))

    updated = cursor.rowcount > 0
    
    connection.commit()
    
    cursor.close()
    connection.close()

    return updated

#* Eliminamos por id
def delete_grade_by_id(grade_id):
    
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "DELETE FROM nota WHERE id = %s"
    
    cursor.execute(sql, (grade_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    
    cursor.close()
    connection.close()

    return deleted