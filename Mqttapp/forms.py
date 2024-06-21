from django import forms
from core.models import MqttBrokerSettings, MqttTopic

class MqttBrokerSettingsForm(forms.ModelForm):
    class Meta:
        model = MqttBrokerSettings
        fields = ['name', 'broker_address', 'port', 'username', 'password']

class MqttTopicForm(forms.ModelForm):
    class Meta:
        model = MqttTopic
        fields = ['broker', 'topic']
