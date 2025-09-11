from pydub import AudioSegment
import speech_recognition as sr
import os
import tempfile

def transcribe_audio(input_audio_path: str) -> str:
    # Convert audio to the right format
    audio = AudioSegment.from_file(input_audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    # Use temporary file with proper cleanup
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio.export(temp_wav.name, format="wav")
        temp_wav_path = temp_wav.name
    
    try:
        r = sr.Recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = r.record(source)
        
        text = r.recognize_google(audio_data)
        return text
    
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
    
    finally:
        
        if os.path.exists(temp_wav_path):
            os.unlink(temp_wav_path)