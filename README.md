# 🤖 Customer Service Assistant

## 🌟 Overview
This application, crafted for the LablabAI Hackathon, is a multilingual customer service chatbot 🌍, integrating technologies like Streamlit, Cohere, Weaviate, and Langchain. It's engineered to aid customers with various queries, supporting multiple languages for a global audience.

## ✨ Features
- **Multilingual Support 🌐**: Detects and responds in several languages, enhancing user experience.
- **Dynamic Responses 💬**: Leverages Cohere's cutting-edge API for context-aware, intelligent responses.
- **Feedback System 📝**: Integrates Weaviate for efficient customer feedback management.
- **Customizable Interaction 🖥️**: Interactive chat interface for user queries, including quick help for common issues like order tracking and return policies.

## 🛠️ Technologies Used
- **Streamlit**: Crafting the web app's user interface.
- **Cohere API**: For advanced natural language processing.
- **Weaviate**: Database management and feedback handling.
- **Transformers**: Language detection and translation functionality.

## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone [repository-url]

## 🚀 Setup
- Set your API keys for Cohere,Weaviate and OpenAI. These should be configured in Streamlit's secrets or your environment variables.

## 🌐 Running the Application
- **Launch the application with Streamlit**:
   ```bash
   streamlit run app.py

## 📖 Usage
Language is set to "Auto" 🗣️ on the top right menu. (language detection feature)
Enter your query in the chat interface 💻. 
Receive and review the bot's response, including intent label and confidence score 📊.
Use the sidebar to rate your experience and provide feedback 🌟.
