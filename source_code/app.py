import streamlit as st
from streamlit_option_menu import option_menu

from sweetviz import analyze
import pandas as pd
import dtale

# from source_code.chatbot_openai import chat_
from chatbot_pandasai import chat_

#set page
st.set_page_config(page_title="Analytics Dashboard", page_icon="🌎", layout="wide")  

# load CSS Style
with open('./src/style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#option menu

with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
        options=['Home','EDA','Chatbot'],
        icons=['house','graph-up','robot'],
        menu_icon="cast", #option
        default_index=0, #option
        orientation="vertical" )



uploaded_file = st.sidebar.file_uploader("Upload File", type=["csv"])

if selected=='Home':
    st.header("👩‍💼 Health and fitness - Data App")
    
    div1 , div2 = st.columns(2)
    with div1:
        st.image('images/logo.jpg', width=400)
    with div2:
        st.image('images/Women_logo.png', width=530)

if selected== 'EDA':
    st.header("📈 Exploratory Data Analysis (EDA) in Python")
    # Create an empty space using markdown and HTML
    st.markdown("""
    <style>
    div[data-testid="stHeader"] {
    margin-bottom: 20px; /* Adjust the margin as needed */
    }
    </style>

    ---
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col2:
        dtale_bt = st.button('Detailed Analysis')
        if dtale_bt:
            if uploaded_file is not None:
                # Read the uploaded CSV file into a DataFrame
                data = pd.read_csv(uploaded_file)

                st.write("### Sample Data")
                st.write(data.head())

                st.write("### Data Analysis with D-Tale")
                dtale.show(data).open_browser()
        
        

    with col1:
        sweetviz_bt = st.button('View Statistics')
        if sweetviz_bt:
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)

                # Analyze data using Sweetviz
                sweetviz_report = analyze(data)

                # Generate HTML report using Sweetviz
                report_html = sweetviz_report.show_html()

                # Display Sweetviz report in Streamlit app
                st.subheader("Sweetviz Report:")
                st.components.v1.html(open("SWEETVIZ_REPORT.html", "r").read(), width=1000, height=600, scrolling=True)




if selected == 'Chatbot':
    st.header("🤖 Your Data Assistant")

    # Create an empty space using markdown and HTML
    st.markdown("""
    <style>
    div[data-testid="stHeader"] {
    margin-bottom: 20px; /* Adjust the margin as needed */
    }
    </style>

    ---
    """, unsafe_allow_html=True)

    # Text input for user to ask questions
    user_input = st.text_input("Ask me anything:")

    if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

    if user_input:

        st.session_state['chat_history'].append(("You", user_input))
        response = chat_(uploaded_file= uploaded_file, query=user_input)
        st.write("Bot:", response)
        

        st.session_state['chat_history'].append(("Bot", response))

    st.subheader("Your Chat History")

    # st.write(st.session_state['chat_history'])
    
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")