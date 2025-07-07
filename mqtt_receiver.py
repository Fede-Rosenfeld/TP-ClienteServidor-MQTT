import threading
import paho.mqtt.client as mqtt
import json
import sqlite3
import time

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect("sensores.db",check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor TEXT,
            valor REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insertar lectura
def guardar_lectura(sensor, valor):
    conn = sqlite3.connect("sensores.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO lecturas (sensor, valor, timestamp) VALUES (?, ?, datetime('now'))", (sensor, valor))
    conn.commit()
    conn.close()
    time.sleep(0.1)

def start_mqtt_thread(socketio):
    init_db()  # Inicializar DB al comenzar

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            sensor = payload.get("sensor")
            valor = float(payload.get("value"))

            print(f"MQTT: sensor={sensor}, valor={valor}")
            guardar_lectura(sensor, valor)

            socketio.emit("nueva_lectura", {"sensor": sensor, "value": valor})
        except Exception as e:
            print("Error al procesar mensaje MQTT:", e)

    def mqtt_loop():
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
        client.subscribe("sensors/temp")
        client.on_message = on_message
        client.loop_forever()

    # Lanzar MQTT en hilo separado
    hilo = threading.Thread(target=mqtt_loop)
    hilo.daemon = True
    hilo.start()