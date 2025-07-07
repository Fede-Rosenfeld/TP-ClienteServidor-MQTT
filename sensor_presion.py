import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    valor = round(random.uniform(950, 1050), 2)
    mensaje = json.dumps({"sensor": "pre", "value": valor})
    client.publish("sensors/pre", mensaje)
    print("Publicado:", mensaje)
    time.sleep(5)
