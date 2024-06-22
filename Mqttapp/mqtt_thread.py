import threading
from .mqtt_client import get_mqtt_client

def start_mqtt_client(user):
    client = get_mqtt_client(user)
    client.loop_forever()

def start_mqtt_thread(user):
    mqtt_thread = threading.Thread(target=start_mqtt_client, args=(user,))
    mqtt_thread.start()
    return mqtt_thread
