import paho.mqtt.client as mqtt
from core.models import MqttBrokerSettings,ProfileSettings

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    broker_settings = userdata['broker_settings']
    if broker_settings:
        topics = broker_settings.topics.all()
        for topic in topics:
            client.subscribe(topic.topic)

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

def get_mqtt_client(user):
    profile_settings = ProfileSettings.objects.filter(user,user).first()
    broker_settings = MqttBrokerSettings.objects.filter(profile_settings=profile_settings).first()
    if not broker_settings:
        raise ValueError("No MQTT broker settings found for the user in the database.")
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    if broker_settings.username and broker_settings.password:
        client.username_pw_set(broker_settings.username, broker_settings.password)
    
    client.user_data_set({'broker_settings': broker_settings})
    client.connect(broker_settings.broker_address, broker_settings.port, 60)
    return client

