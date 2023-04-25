# import settings
from django.conf import settings
import os
import openai

# OpenAI API Key
if settings.OPENAI_API_KEY:
    openai.api_key = "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"
else:
    raise Exception('OpenAI API Key not found')


def get_completion(prompt):
    query = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt }]
    )
    response = query.get('choices')[0]['message']['content']
    return response
