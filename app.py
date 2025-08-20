import streamlit as st
from audio_processing import transcribe_audio
from llm_handling import generate_summary
import requests
st.title("Upload Audio to Transcribe and Summarize")

uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    with st.spinner("Processing audio..."):
        temp_file = "temp_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
    payload={
        "audio_path": "temp_audio.wav"
    }
    API_URL="http://127.0.0.1:8000/notesmaker"

    with st.spinner("Generating summary..."):
        response=requests.post(API_URL,json=payload)
        if response.status_code == 200:
            summary = response.json()
            st.subheader("Summary")
            st.write(summary["summary"])
        else:
            st.error(f"Error: {response.status_code}")
