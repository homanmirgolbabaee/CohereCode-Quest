import streamlit as st
from weaviate import *
import weaviate
from weaviate.schema import Schema
import cohere


# Initliazing Cohere 
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]

co = cohere.Client(COHERE_API_KEY)
print("Cohere Client initialized ...")
def generate_response_with_cohere(query):
    response = co.generate(
        model="medium",  # Choose the model size (e.g., 'medium', 'large')
        prompt=query,
        max_tokens=50,
        temperature=0.5  # Adjust the creativity of the response
    ).generations[0].text
    return response.strip()



CLUSTER_URL = st.secrets['WEAVIATE_CLUSTER_URL']
WEAVIATE_API = st.secrets['WEAVIATE_KEY']



auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API)
client = weaviate.Client(url=CLUSTER_URL, auth_client_secret=auth_config)

# Define the schema
schema = Schema(client)

# Define the Customer class
customer_class = {
    "class": "Customer",
    "vectorizer": "text2vec-cohere",
    "vectorIndexConfig": {"distance": "dot"},  # for multilingual models
    "properties": [
        {"name": "name", "dataType": ["string"]},
        {"name": "language", "dataType": ["string"]},
        {"name": "location", "dataType": ["string"]}
    ],
}

# Define the Inquiry class
inquiry_class = {
    "class": "Inquiry",
    "vectorizer": "text2vec-cohere",
    "vectorIndexConfig": {"distance": "dot"},  # for multilingual models
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

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# define language pairs

language_pairs = {
    'en-de': 'Helsinki-NLP/opus-mt-en-de',
    'en-fr': 'Helsinki-NLP/opus-mt-en-fr',
    'es-en': 'Helsinki-NLP/opus-mt-es-en',
    'en-it': 'Helsinki-NLP/opus-mt-en-it',
    'it-en': 'Helsinki-NLP/opus-mt-it-en'
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
translated_text_it_en = translate_text("Come Estai?",'it','en')
print(translated_text_en)  # Outputs the translated text in English
print(translated_text_de)  # Outputs the translated text in German
print(translated_text_fr)  # Outputs the translated text in French
print(translated_text_en)  # Outputs the translated text in English
print(translated_text_it)  # Outputs the translated text in Italian
print(translated_text_it_en)

# Test the function
test_query = "How do I reset my password?"
response = generate_response_with_cohere(test_query)
print(response)


import numpy as np
import cohere
from cohere.responses.classify import Example

co = cohere.Client(COHERE_API_KEY)
def calculate_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_most_similar(query, inquiries):
    query_embedding = co.embed([query]).embeddings[0]
    highest_similarity = 0
    most_similar_response = None

    for inquiry in inquiries:
        inquiry_embedding = co.embed([inquiry['question']]).embeddings[0]
        similarity = calculate_similarity(query_embedding, inquiry_embedding)
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_response = inquiry['response']

    return most_similar_response

# Example usage
print("Entering Advanced Search ...\n")
user_query = "reset my password?"
response = find_most_similar(user_query, inquiries)
print(response)

