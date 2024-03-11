import streamlit as st 
from streamlit_chat import message
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import tempfile
import os


def chat_(uploaded_file, query):

    if uploaded_file :
    #use tempfile because CSVLoader only accepts a file_path
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        df = pd.read_csv(f'{tmp_file_path}')

        llm = OpenAI(api_token=os.getenv('OPENAI_API_KEY'))

        pandas_ai = SmartDataframe(df, config={"llm": llm})

        with st.spinner('Loading ...'):
            return pandas_ai.chat(query=query)
            
            
    
    else :
        # Define your chatbot responses here
        responses = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hello! How can I assist you today?",
            "how are you": "I'm just a bot, but I'm here to help!",
            "bye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!"
        }

        # Convert user input to lowercase for case-insensitive matching
        user_input = query.lower()

        # Check if the user input matches any predefined responses
        for key, value in responses.items():
            if key in user_input:
                return value
        return 'No file uploaded, Sorry I dont understand your query !!'


    

