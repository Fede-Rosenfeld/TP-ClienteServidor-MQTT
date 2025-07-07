import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    valor = round(random.uniform(20, 30), 2)
    mensaje = json.dumps({"sensor": "temp", "value": valor})
    client.publish("sensors/temp", mensaje)
    print("Publicado:", mensaje)
    time.sleep(5)
