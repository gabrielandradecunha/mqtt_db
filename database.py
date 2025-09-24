import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    dbname = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database_url = f"postgresql://{db_user}:{password}@{host}:{port}/{dbname}"
    return psycopg2.connect(database_url)


def insert_telemetry(unix, latitude, longitude, course, speed,
                     altitude, pitch, roll, accelMagnitude,
                     maxDeltaAccel, power_status, error_status):
    """
    Insere um pacote de telemetria na tabela 'telemetria'.
    """
    try:
        connection = get_connection()
        print("Connection with DB established...")
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return

    cursor = connection.cursor()
    query = """
        INSERT INTO telemetria (
            unix, latitude, longitude, course, speed, altitude,
            pitch, roll, accel_magnitude, max_delta_accel,
            power_status, error_status
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cursor.execute(query, (
            unix, latitude, longitude, course, speed,
            altitude, pitch, roll, accelMagnitude,
            maxDeltaAccel, power_status, error_status
        ))
        connection.commit()
        print(f"Pacote de telemetria inserido com sucesso (unix={unix})")
    except Exception as e:
        print(f"Erro ao inserir telemetria: {e}")
        connection.rollback()
    finally:
        cursor.close()
        if connection:
            connection.close()
