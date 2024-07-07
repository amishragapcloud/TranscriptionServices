import streamlit as st
import openai
import os
from dotenv import load_dotenv
from extras import *
from saveasdocx import *
import random

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_id = os.getenv("AZURE_DEPLOYMENT_ID")

st.set_page_config(
    page_title="GapcloudAI - Conversations with your Data",
    page_icon="🤖",
    layout="wide"
)

logo_url = "https://media.licdn.com/dms/image/C560BAQGeCieaiSruPg/company-logo_200_200/0/1630669521343/gapcloud_logo?e=2147483647&v=beta&t=jFkQ6l0vG434rsZTMywindOO_6FkdrH4FYhE0W6Xj0Q"
logo_html = f"""
<div style="position: absolute; top: 10px; right: 10px; z-index: 1000;">
    <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

st.markdown('<h1 class="title" style="color: Black; display: inline;">GapcloudAI</h1>'
            '<h3 style="color: Pink; display: inline;">Actions on your Data</h3>', 
            unsafe_allow_html=True)

st.markdown("      ")

st.markdown('<h2 class="title" style="color: Black; display: inline;">BP Call Transcription</h2>', unsafe_allow_html=True)
st.markdown("      ")
st.write("Upload an audio file to get the transcription")

uploaded_file = st.file_uploader("Choose an audio file", type=["m4a", "mp3", "wav", "flac"])

def sidebar():
    global TEMP, MODEL
    with st.sidebar:
        with st.expander("Settings", expanded=True):
            TEMP = st.slider(label='LLM Temperature', min_value=0.0, max_value=1.0, value=0.7)
            MODEL = st.selectbox(label='LLM Model', options=['gpt-4', 'gpt-3.5-turbo'])

sidebar()

def random_color():

    return f'rgb({random.randint(100, 200)}, {random.randint(100, 200)}, {random.randint(100, 200)})'

if not deployment_id:
    st.error("The AZURE_DEPLOYMENT_ID environment variable is not set.")
else:
    if uploaded_file is not None:
        try:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with open(uploaded_file.name, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model=deployment_id,
                    file=audio_file
                )
                
                st.audio(uploaded_file, format='audio/mp3')
                
                st.write("**Transcription Results:**")
                st.write(transcript)
                
                key_points = analyze_key_phrases(transcript)  
                sentiment = analyze_sentiment(transcript) 
                intent = infer_intent(key_points) 
                problem = extract_problem_statement(transcript)
                empathy = calculate_empathy(sentiment)
                categorization = categorization(key_points)
  
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Sentiment:</div>** {sentiment}", unsafe_allow_html=True)  
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Key Phrases:</div>**", unsafe_allow_html=True)
                for phrase in key_points:  
                    st.write("- ", phrase)
                
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Intent:</div>** {intent}", unsafe_allow_html=True)
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Problem Statement:</div>** {problem}", unsafe_allow_html=True)
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Empathy:</div>** {empathy}", unsafe_allow_html=True)
                st.markdown(f"**<div style='background-color: {random_color()}; color: black; font-weight: bold;'>Call Category:</div>** {categorization}", unsafe_allow_html=True)


 
                
        except Exception as e:
            st.error(f"An error occurred: {e}")




with open("test.pdf","rb") as pdf_file:
   PDFbyte=pdf_file.read()


st.download_button(label="Export",data=PDFbyte,file_name="Transcription.pdf",mime='application/octet-stream')
