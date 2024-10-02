import streamlit as st
import os
from langchain.tools import Tool
from langchain.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from docx import Document
from io import BytesIO
import base64
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
import PyPDF2
import docx2txt
from PIL import Image

# Load environment variables
load_dotenv()

# Set the API keys from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Check if the API keys are set
if not groq_api_key or not serper_api_key:
    st.error("Please set the GROQ_API_KEY and SERPER_API_KEY in your .env file.")
    st.stop()

# Initialize ChatGroq
try:
    llm = ChatGroq(
        api_key=groq_api_key,
        model_name='llama-3.1-70b-versatile',
        temperature=0.7
    )
except Exception as e:
    st.error(f"Error initializing ChatGroq: {str(e)}")
    st.stop()

# Initialize search tool
search_tool = None
try:
    search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    search_tool = Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events; need to gather information about the user inputs. Attend and search main key words and phrases"
    )
except Exception as e:
    st.error(f"Error initializing search tool: {str(e)}")
    st.stop()

# ... (keep the rest of your code unchanged until the "Get Diagnosis and Treatment Plan" button)

# Execution button for generating diagnosis and treatment plan
if st.button("Get Diagnosis and Treatment Plan"):
    with st.spinner('Diagnosing...'):
        try:
            # Combine all input into a single prompt
            prompt = f"""
            Analyze the following patient information and provide a diagnosis and treatment plan:
            
            Gender: {gender}
            Age: {age}
            Symptoms: {symptoms}
            Medical History: {medical_history}
            Additional Information: {file_content}
            
            Please provide:
            1. A detailed, step-by-step, effective, scientifically proven preliminary diagnosis.
            2. A comprehensive treatment plan tailored to the patient's diagnosis, symptoms, and medical history.
            """
            
            # Get response from ChatGroq
            response = llm.predict(prompt)
            
            # Format the result
            formatted_result = format_result(response)
            
            st.markdown(formatted_result)
            
            docx_file = generate_docx(formatted_result)
            download_link = get_download_link(docx_file, "diagnosis_and_treatment_plan.docx")
            st.markdown(download_link, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
