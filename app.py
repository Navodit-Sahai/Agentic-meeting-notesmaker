import streamlit as st
from audio_processing import transcribe_audio
from llm_handling import generate_summary
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="Audio Transcriber & Summarizer",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Audio Transcriber & Summarizer")
st.markdown("Upload an audio file to get a transcript and intelligent summary!")

# Check for API key
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY environment variable not found. Please add it to your Streamlit secrets.")
    st.info("Go to your Streamlit app settings → Secrets and add: `GROQ_API_KEY = 'your-api-key-here'`")
    st.stop()

uploaded_file = st.file_uploader(
    "Choose an audio file", 
    type=["wav", "mp3", "m4a", "ogg", "flac"],
    help="Supported formats: WAV, MP3, M4A, OGG, FLAC"
)

if uploaded_file is not None:
    # Display file info
    st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size} bytes)")
    
    try:
        # Create temporary file
        with st.spinner("📤 Uploading and preparing audio..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_file_path = tmp_file.name
        
        # Transcribe audio
        with st.spinner("🎙️ Transcribing audio... This may take a few minutes."):
            transcript = transcribe_audio(temp_file_path)
            
        # Generate summary
        with st.spinner("🤖 Generating intelligent summary..."):
            summary = generate_summary(transcript)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Transcript")
            st.text_area("Full transcript:", transcript, height=300)
            
        with col2:
            st.subheader("📊 Summary")
            st.markdown(summary)
        
        # Download option
        st.download_button(
            label="💾 Download Transcript",
            data=transcript,
            file_name=f"transcript_{uploaded_file.name}.txt",
            mime="text/plain"
        )
        
        # Clean up
        os.unlink(temp_file_path)
        
    except Exception as e:
        st.error(f"❌ Error processing audio: {str(e)}")
        
        # Detailed error information in expander
        with st.expander("🔍 Error Details"):
            st.code(str(e))
            
        # Clean up on error
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# Add footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Groq")