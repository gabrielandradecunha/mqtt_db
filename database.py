import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_mac():
    dbname = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    database_url = f"postgresql://{db_user}:{password}@{host}:{port}/{dbname}"

    try:
        connection = psycopg2.connect(database_url)
        print("Connection with DB established...")
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return

    cursor = connection.cursor()
    query = "SELECT mac FROM reservatorios"

    try:
        cursor.execute(query)
        macs = cursor.fetchall()
        mac_list = [mac[0] for mac in macs]
        return mac_list
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        if connection:
            connection.close()

def update_db(mac_adress, new_vol, umidade, temperatura, profundidade):
    dbname = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    database_url = f"postgresql://{db_user}:{password}@{host}:{port}/{dbname}"

    try:
        connection = psycopg2.connect(database_url)
        print("Connection with DB established...")
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return

    cursor = connection.cursor()
    query = "UPDATE reservatorios SET volume_atual=%s, umidade=%s, profundidade=%s, temperatura=%s WHERE mac=%s"

    try:
        cursor.execute(query, (new_vol, umidade, profundidade, temperatura, mac_adress))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Volume atualizado com sucesso para o reservatório com o mac {mac_adress}. Novo volume: {new_vol}")
        else:
            print(f"Nenhum reservatório encontrado com o mac {mac_adress}. Nenhuma atualização realizada.")
    except Exception as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
        connection.rollback()
    finally:
        cursor.close()
        if connection:
            connection.close()
