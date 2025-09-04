import streamlit as st
from audio_processing import transcribe_audio
from llm_handling import generate_summary
import os
import tempfile

st.title("Upload Audio to Transcribe and Summarize")

uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file is not None:
    try:
        with st.spinner("Processing audio..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_file_path = tmp_file.name
        
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio(temp_file_path)
            
        with st.spinner("Generating summary..."):
            summary = generate_summary(transcript)
            
        st.subheader("Transcript")
        st.write(transcript)
        
        st.subheader("Summary")
        st.write(summary)
        
        os.unlink(temp_file_path)
        
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
