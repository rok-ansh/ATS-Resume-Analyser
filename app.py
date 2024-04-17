# Overview of the Project
# 1. Field to put my Job Description
# 2.Upload PDF
# 3.PDF to Image so that Gemini pro model can read it --> Processing --> Google Gemini Pro
# 4.Prompts Template [Multipple Prompts]




# Lets import the Library
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

# We are getting the API key which is there in env file we can also put it directly under api_key = "value"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ceating a function Gemini pro vision to get the response once we upload the pdf 
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# now lets upload the file and convert PDF to image so that gemini model can read it 
def input_pdf_setup(upload_file):
    # COnvert pdf to image
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())

        # In my resume first have all the content that we have to read first page of image
        first_page = images[0]

        # Lets now convert the image to bytes 
        img_byte_arr  = io.BytesIO()
        first_page.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                # base64 is used : It's basically a way of encoding arbitrary binary data in ASCII text. It takes 4 characters per 3 bytes of data, plus potentially a bit of padding at the end.
                # Essentially each 6 bits of the input is encoded in a 64-character alphabet. The "standard" alphabet uses A-Z, a-z, 0-9 and + and /, with = as a padding character. There are URL-safe variants
                "data":base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
# Streamlit app
st.set_page_config(page_title = "ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key ="input" )
uploaded_file = st.file_uploader("Upload your resume(PDF)...",type=["pdf"])



if uploaded_file is not None:
    st.write("PDF Uploaded successfully")

submit1 = st.button("Tell me about the resume")

submit2 = st.button("How can I Improve my skills")

submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with technical experience in field of Data Science, Machine learning, Big data Engineering, 
Full stack web development,
MLOPs, Data Analyst. Your task is to review the provided resume against the job description for the profiles.
Please share your professional evaluation on whether the candidates profile aligns with the roles.
Highlight the strength and weakness of the applicant in relation to specificed job requirements.

"""

input_prompt2 = """
You are an experienced HR with technical experience in field of Data Science, Machine learning, Big data Engineering,  
Full stack web development,MLOPs, Data Analyst. 
Your task is to review the provided resume against the job description for the profiles and try to match the required skills. 
Please compare the skills mentioned in the resume and Job description and let me know what skills need to be added.
Please share your professional evaluation that candiate need to focus on this skills to be successful to grab the job 
in the given profile.

"""

input_prompt3 = """
You are  skilled ATS (Applicant Tracking system) scanner with a deep understanding of data science, and ATS functionality.
your task is to evalutae the resume against the provided job description. Give me the percenatge match if the resume matches 
the job  description. First the output should come as percenatge and then keywords missing and last the final thoughts ans suggestion.

"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)

    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The resposne is :")
        st.write(response)

    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is : ")
        st.write(response)

    else:
        st.write("Please upload the resume")



