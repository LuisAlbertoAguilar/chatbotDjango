# import settings
from django.conf import settings
import os
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.apps import apps
from django.db import models
import uuid
import json
from django.core import serializers

from base_app.models import *
authenticator = IAMAuthenticator('olwfdKnFyjWMJIX7TLCpNcjphhnjllxCNbS4yHOnhlI9')
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/e55e3642-1680-43f3-8fea-a23c0f36f8c5')

assistant_id = 'cf116e14-d209-468e-a633-6ee7431d66fd'

def export_database_to_json():
    tables = ['Product', 'Order', 'OrderItem', 'User']  # Replace with your table names

    data = {}
    for table in tables:
        model = apps.get_model(app_label='base_app', model_name=table)
        queryset = model.objects.all()
        serialized_data = serializers.serialize('json', queryset)
        data[table] = serialized_data

    with open('database.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_database():
    with open('database.json', 'r') as file:
        database = json.load(file)
    return database

def get_completion(prompt):
    try:
        # Creamos una sesión con el asistente y obtenemos el ID de la sesión
        response = assistant.create_session(
            assistant_id=assistant_id
        ).get_result()
        session_id = response.get("session_id")
        # Enviamos un mensaje al asistente con el texto proporcionado como prompt
        response2 = assistant.message(
            assistant_id=assistant_id,
            session_id=session_id,
            input={
                'message_type': 'text',
                'text': prompt.strip(),
                # 'context': {
                #         'database_response': db
                #     }
            }
        ).get_result()
        # TODO: manejar el caso de un iframe
        # {'title': 'Producto X:', 'source': 'https://www.javatpoint.com/', 'response_type': 'iframe'}]},
        # 'user_id': '14768ef6-5ae9-4419-8f1d-1b539ca95125'

        # Devolvemos el texto de respuesta proporcionado por el asistente
        return response2['output']['generic'][0]['text']
    except:
        # En caso de que ocurra una excepción, mostramos un mensaje de error genérico
        return "¡Hola! Parece que ha ocurrido un error al enviar tu mensaje. Lamentamos los inconvenientes que esto pueda haber causado."


def is_related_to_models(text):
    # Get a list of all the model names in the Django app
    model_names = [m.__name__ for m in apps.get_models()]

    # Create a set of all the fields in the Django models
    fields = set()
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if isinstance(field, models.Field):
                fields.add(field.name)

    # Check if the text mentions any of the model names or fields
    for word in text.split():
        if word.lower() in model_names or word.lower() in fields:
            return True

    return False