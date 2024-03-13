import streamlit as st
from streamlit_option_menu import option_menu

from sweetviz import analyze
from dtale.views import startup
from dtale.app import get_instance
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

    report_selected = st.selectbox('Select Report', ['None', 'View Statistcs','Detailed Analysis'])

    # col1, col2 = st.columns(2)

    # with col2:
        # dtale_bt = st.button('Detailed Analysis')
        # if dtale_bt:
    if report_selected == 'Detailed Analysis':
        
        if uploaded_file is not None:
            # Read the uploaded CSV file into a DataFrame
            df = pd.read_csv(uploaded_file)

            # st.write("### Sample Data")
            # st.write(df.head())

            st.write("### Data Analysis with D-Tale")
            # dtale.show(data)
            startup(data_id="1", data=df)
            df = get_instance("1").data
            st.markdown(
                    "<iframe src=/dtale/main/1 / width='1000' height='1000'>",
                    unsafe_allow_html=True
                )
        
        

    # with col1:
    #     sweetviz_bt = st.button('View Statistics')
    #     if sweetviz_bt:
    if report_selected == 'View Statistcs':
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)

            # Analyze data using Sweetviz
            sweetviz_report = analyze(data)

            # Generate HTML report using Sweetviz
            report_html = sweetviz_report.show_html(filepath='./source_code/EDA.html',
                                                open_browser=False)
            

            # Display Sweetviz report in Streamlit app
            st.subheader("Statistical Report:")
            st.components.v1.html(open("source_code/EDA.html", "r").read(), width=1000, height=1000, scrolling=True)




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
        