
from streamlit import secrets
import streamlit as st
from weaviate import *
import weaviate
from weaviate.schema import Schema


CLUSTER_URL = st.secrets['WEAVIATE_CLUSTER_URL']
WEAVIATE_API = st.secrets['WEAVIATE_KEY']

print(CLUSTER_URL)
print(WEAVIATE_API)


auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API)
client = weaviate.Client(url=CLUSTER_URL, auth_client_secret=auth_config)

# Define the schema
schema = Schema(client)

# Define the Customer class
customer_class = {
    "class": "Customer",
    "properties": [
        {"name": "name", "dataType": ["string"]},
        {"name": "language", "dataType": ["string"]},
        {"name": "location", "dataType": ["string"]}
    ],
}

# Define the Inquiry class
inquiry_class = {
    "class": "Inquiry",
    "properties": [
        {"name": "question", "dataType": ["string"]},
        {"name": "language", "dataType": ["string"]},
        {"name": "response", "dataType": ["string"]}
    ],
}




# Create some sample data
customers = [
    {"name": "Alice", "language": "English", "location": "USA"},
    {"name": "Carlos", "language": "Spanish", "location": "Spain"}
]

inquiries = [
    {"question": "How do I reset my password?", "language": "English", "response": "You can reset your password by going to settings."},
    {"question": "¿Cómo restablezco mi contraseña?", "language": "Spanish", "response": "Puede restablecer su contraseña en la configuración."}
]

# Import the data into Weaviate
for customer in customers:
    client.data_object.create(customer, "Customer")

for inquiry in inquiries:
    client.data_object.create(inquiry, "Inquiry")
    
    
# Example query to find inquiries in a specific language
query = """
{
  Get {
    Inquiry(where: {
      operator: Equal
      path: ["language"]
      valueString: "English"
    }) {
      question
      response
    }
  }
}
"""

# Execute the query
result = client.query.raw(query)
print(result)    


from langchain.schema import Document
from langchain.document_transformers import GoogleTranslateTransformer
import os 
import asyncio
from transformers import pipeline

os.environ['OPENAI_API_KEY'] = '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'

# define language pairs

language_pairs = {
    'en-de': 'Helsinki-NLP/opus-mt-en-de',
    'en-fr': 'Helsinki-NLP/opus-mt-en-fr',
    'es-en': 'Helsinki-NLP/opus-mt-es-en',
    'en-it': 'Helsinki-NLP/opus-mt-en-it'
}

# Initialize the translation model
# Example: English to German translation model
translator = pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")


def translate_text(text, source_lang, target_lang):
    model_key = f'{source_lang}-{target_lang}'
    if model_key in language_pairs:
        model_name = language_pairs[model_key]
        translator = pipeline("translation", model=model_name)
        translation = translator(text, max_length=512)
        return translation[0]['translation_text']
    else:
        raise ValueError(f"No translation model found for {model_key}")
      
      
# Example usage

translated_text_de = translate_text("How are you?", 'en', 'de')  # English to German
translated_text_fr = translate_text("How are you?", 'en', 'fr')  # English to French
translated_text_en = translate_text("¿Cómo estás?", 'es', 'en')  # Spanish to English
translated_text_it = translate_text("How are you?", 'en', 'it')  # Spanish to English

print(translated_text_en)  # Outputs the translated text in English
print(translated_text_de)  # Outputs the translated text in German
print(translated_text_fr)  # Outputs the translated text in French
print(translated_text_en)  # Outputs the translated text in English
print(translated_text_it)  # Outputs the translated text in Italian
