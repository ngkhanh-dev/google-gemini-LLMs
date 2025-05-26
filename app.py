import streamlit as st
import json
# from google import genai
import google.generativeai as genai
from user_function import initialize_ai
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Khởi tạo model
# model = "gemini-2.0-flash"
chat = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

# Giao diện chính
st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖")
st.title("🤖 Gemini AI Assistant")

# Lưu session chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "start_conversation" not in st.session_state:
    st.session_state.start_conversation = True
    st.session_state.chat_history = initialize_ai()
    response = chat.generate_content(json.dumps(st.session_state.chat_history))
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# Hiển thị lịch sử chat
for msg in st.session_state.chat_history:
    if msg["role"] != "system": # Bỏ qua phần instruction 
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Nhận câu hỏi từ người dùng
user_input = st.chat_input("Bạn muốn hỏi gì?")

if user_input:
    # Hiển thị câu hỏi
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Gửi đến Gemini
    try:
        # Gửi câu hỏi đến Gemini
        # response = chat.generate_content(user_input)
        # comment the line above and uncomment this below line if you want chat bot can remember the history
        response = chat.generate_content(json.dumps(st.session_state.chat_history))
        assistant_reply = response.text

        # Lưu câu trả lời vào sessions
        # Hiển thị câu trả lời
        st.chat_message("assistant").markdown(assistant_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    except Exception as e:
        # Xử lý lỗi nếu có
        st.error(f"Đã xảy ra lỗi: {e}")
        assistant_reply = "Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn."
        st.chat_message("assistant").markdown(assistant_reply)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    # Gửi câu hỏi đến Gemini