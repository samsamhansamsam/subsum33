import streamlit as st
import os
from PIL import Image
import openai
from dotenv import load_dotenv
import pytesseract

# .env 파일의 환경 변수 로드
load_dotenv()

#api키
openai.api_key = os.getenv("OPENAI_API_KEY")

# ChatGPT에 요청하는 함수 (임시로 간단한 답장 생성 기능)
def generate_response(dialogue_text):
    prompt = f"대화: {dialogue_text}\n\n위 대화를 기반으로 적절한 답장을 추천해줘."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Tesseract 실행 파일의 경로 명시 (Ubuntu에서는 보통 '/usr/bin/tesseract')
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# 이미지에서 텍스트를 추출하는 함수 (OCR)
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang="kor+eng")
    return text

# Streamlit 웹페이지 구성
st.title('연애가 서툰 당신을 위한 대화 코치')
st.write("이성과의 대화가 어렵다면, 대화 내역을 업로드하여 적절한 답장을 추천받으세요!")

# 파일 업로드 (텍스트나 이미지 파일 지원)
uploaded_file = st.file_uploader("대화 내역을 업로드하세요 (이미지 또는 텍스트 파일)", type=["txt", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 이미지 파일일 경우
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드된 이미지', use_column_width=True)
        dialogue_text = extract_text_from_image(image)
        st.write("이미지에서 추출된 대화 내역:")
        st.write(dialogue_text)
    # 텍스트 파일일 경우
    elif uploaded_file.type == "text/plain":
        dialogue_text = uploaded_file.read().decode("utf-8")
        st.write("업로드된 텍스트 대화 내역:")
        st.write(dialogue_text)
    
    # ChatGPT를 통해 답장 추천
    if dialogue_text:
        with st.spinner('대화 내용을 분석 중입니다...'):
            recommended_reply = generate_response(dialogue_text)
        st.success("추천된 답장:")
        st.write(recommended_reply)

st.write("Powered by ChatGPT")
