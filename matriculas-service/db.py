import os   
import psycopg2

def connect_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT', 5432)
    )
    
def init_db():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matricula (
            id SERIAL PRIMARY KEY,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            anio INTEGER NOT NULL,
            periodo VARCHAR(10) NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()