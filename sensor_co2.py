import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    valor = round(random.uniform(400, 600), 2)
    mensaje = json.dumps({"sensor": "co2", "value": valor})
    client.publish("sensors/co2", mensaje)
    print("Publicado:", mensaje)
    time.sleep(5)
