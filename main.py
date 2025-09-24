import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from dotenv import load_dotenv
from database import update_db, get_mac
from router import router
from datetime import datetime
import threading

load_dotenv()

# mosquitto credentials
user = os.getenv('MOSQUITTO_USER')
password = os.getenv('MOSQUITTO_PASSWORD')
mqtt_host = os.getenv('MOSQUITTO_HOST')
mqtt_port = os.getenv('MOSQUITTO_PORT')
mqtt_topic = os.getenv('MOSQUITTO_TOPIC')

# API
# frontend url for cors
url_frontend = os.getenv('URL_FRONTEND')

app = FastAPI()

origins = [
    str(url_frontend),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"], # porta da aplicação php
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=[""])

@app.get("/")
def root():
    return {"message": "API to connect in broker mqtt"}

# MQTT callback's
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"MQTT broker conected with result code: {reason_code}")
    client.subscribe(mqtt_topic)
    print(f"MAC's in database: {get_mac()}")

def on_disconnect(client, userdata, rc):
    print("MQTT broker disconnected with result code: %s", rc)

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}")

    json_string = msg.payload
    data = json.loads(json_string)

    # Processa somente se a chave 'data' estiver presente
    if 'data' not in data:
        print("Mensagem ignorada: não contém campo 'data'.")
        return

    # Valor do hidrometro (ajustável)
    litros = 1000

    try:
        date_time = datetime.utcfromtimestamp(data['data']['epoch'])

        print(
            f"devid: {data['devid']}, "
            f"volume: {int(data['data']['in1_cnt_pulses']) * litros}, "
            f"umidade: {int(data['data']['var0']) / 10}, "
            f"temperatura: {int(data['data']['var1']) / 10}, "
            f"profundiade: {int(100 - (data['data']['adc'] / 100))}m",
            f"timestamp: {date_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        update_db(
            str(data['devid']),
            int(data['data']['in1_cnt_pulses']) * litros,
            int(data['data']['var0']) / 10,
            int(data['data']['var1']) / 10,
            int(data['data']['adc'])
        )

    except KeyError as e:
        print(f"Campo esperado não encontrado: {e}")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# caso nao usar broker publico
#client.username_pw_set(user, password)
client.connect(str(mqtt_host), int(mqtt_port), 60)

# tls opcional
#client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

def run_mqtt():
    client.loop_forever()

mqtt_thread = threading.Thread(target=run_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()