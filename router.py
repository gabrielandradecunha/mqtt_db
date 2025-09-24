import paho.mqtt.client as mqtt
from fastapi import APIRouter, Form
import os
from dotenv import load_dotenv

load_dotenv()

mqtt_host = os.getenv('MOSQUITTO_HOST')
mqtt_port = int(os.getenv('MOSQUITTO_PORT'))
mqtt_user = os.getenv('MOSQUITTO_USER')
mqtt_password = os.getenv('MOSQUITTO_PASSWORD')
mqtt_topic = os.getenv('MOSQUITTO_TOPIC')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#client.username_pw_set(mqtt_user, mqtt_password)

# tls opcional
#client.tls_set()

client.connect(mqtt_host, mqtt_port, 60)

router = APIRouter()

def ligarmotor(topic: str):
    value = '{"motor": 1}'
    client.publish(topic, value)
    print(f"Publicado no tópico {topic}: {value}")

@router.post('/ligarmotor')
def motor():
    topic = f"{mqtt_topic}/motor"
    ligarmotor(topic)
    return {"message": f"{topic}"}
