
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




# Schema Initlization - Setup Uncomment if First Time
# Add classes to the schema using the client

#try:
#    client.schema.create_class(customer_class)
#    client.schema.create_class(inquiry_class)
#    print("Schema created successfully.")
#except Exception as e:
#    print(f"An error occurred: {e}")


