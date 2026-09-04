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
        CREATE TABLE IF NOT EXISTS nota (
            id SERIAL PRIMARY KEY,
            matricula_id INTEGER NOT NULL,
            calificacion NUMERIC(3,2) NOT NULL,
            observacion VARCHAR(200)
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()