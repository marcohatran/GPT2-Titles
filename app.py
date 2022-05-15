import time
import threading
import streamlit as st
import requests

def title_generator(text):
    url = f"http://localhost:8400/generate?query={text}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = response.json()
    return json_response['title']


text_input = st.text_input("Input keywords or tags")
if text_input:
    st.text('Titles:')
    text_output = title_generator(text_input)
    st.text(text_output)

