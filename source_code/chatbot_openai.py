import streamlit as st 
from streamlit_chat import message
from langchain_experimental.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI

import pandas as pd
import tempfile
import os



def chat_(uploaded_file, query):

    if uploaded_file :
    #use tempfile because CSVLoader only accepts a file_path
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        df = pd.read_csv(f'{tmp_file_path}')

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        agent_executor = create_pandas_dataframe_agent(
            llm,
            df,
            agent_type="openai-tools",
            verbose=True
        )

        

        # agent = create_csv_agent(OpenAI(temperature=0), 
        #                     f'{tmp_file_path}' ,
        #                     verbose = True)

        with st.spinner('Loading ...'):
            return agent_executor.run(query)
            # return agent.run(query)
            
    
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

# uploaded_file = st.sidebar.file_uploader("Upload your Data", type="csv")

# if uploaded_file :
#    #use tempfile because CSVLoader only accepts a file_path
#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         tmp_file.write(uploaded_file.getvalue())
#         tmp_file_path = tmp_file.name

#     loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
#                 'delimiter': ','})
#     data = loader.load()
#     #st.json(data)
#     embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
#                                        model_kwargs={'device': 'cpu'})

#     db = FAISS.from_documents(data, embeddings)
#     db.save_local(DB_FAISS_PATH)
#     llm = load_llm()
#     chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

#     def conversational_chat(query):
#         result = chain({"question": query, "chat_history": st.session_state['history']})
#         st.session_state['history'].append((query, result["answer"]))
#         return result["answer"]
    
#     if 'history' not in st.session_state:
#         st.session_state['history'] = []

#     if 'generated' not in st.session_state:
#         st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]

#     if 'past' not in st.session_state:
#         st.session_state['past'] = ["Hey ! 👋"]
        
    #container for the chat history
    # response_container = st.container()
    # #container for the user's text input
    # container = st.container()

    # with container:
    #     with st.form(key='my_form', clear_on_submit=True):
            
    #         user_input = st.text_input("Query:", placeholder="Talk to your csv data here (:", key='input')
    #         submit_button = st.form_submit_button(label='Send')
            
    #     if submit_button and user_input:
    #         output = conversational_chat(user_input)
            
    #         st.session_state['past'].append(user_input)
    #         st.session_state['generated'].append(output)

    # if st.session_state['generated']:
    #     with response_container:
    #         for i in range(len(st.session_state['generated'])):
    #             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
    #             message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")



    

