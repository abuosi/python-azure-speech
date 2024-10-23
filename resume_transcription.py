import os
from openai import AzureOpenAI

def resume_transcription(transcription):

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    message_text = [
        {"role": "system", "content": "Você é um assistente que cria um resumo de um dialogo, e traz uma conclusão"},
        {"role": "user", "content": "Olá, Você pode resumir e trazer um resumo com o sentimento do cliente do dialogo a seguir: "+transcription}
    ]

    chat_completion = client.chat.completions.create(
        model="gpt-4o", # model = "deployment_name".
        messages=message_text
    )

    return chat_completion.choices[0].message.content
