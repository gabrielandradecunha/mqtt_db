import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from database import insert_telemetry
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
url_frontend = os.getenv('URL_FRONTEND')

app = FastAPI()

origins = [str(url_frontend)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
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

def on_disconnect(client, userdata, rc):
    print("MQTT broker disconnected with result code: %s", rc)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8").strip()
        valores = payload.split(",")

        if len(valores) != 12:
            print(f"Mensagem ignorada, formato incorreto: {payload}")
            return

        unix = int(valores[0])
        latitude = float(valores[1])
        longitude = float(valores[2])
        course = float(valores[3])
        speed = float(valores[4])
        altitude = int(valores[5])
        pitch = float(valores[6])
        roll = float(valores[7])
        accelMagnitude = float(valores[8])
        maxDeltaAccel = float(valores[9])
        power_status = int(valores[10])
        error_status = int(valores[11])

        insert_telemetry(
            unix, latitude, longitude, course, speed,
            altitude, pitch, roll, accelMagnitude,
            maxDeltaAccel, power_status, error_status
        )

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set()
client.username_pw_set(user, password)
client.connect(str(mqtt_host), int(mqtt_port), 60)

client.on_connect = on_connect
client.on_message = on_message

def run_mqtt():
    client.loop_forever()

mqtt_thread = threading.Thread(target=run_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()
