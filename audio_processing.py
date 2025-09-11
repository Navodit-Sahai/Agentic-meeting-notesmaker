from pydub import AudioSegment
import speech_recognition as sr
import os

def transcribe_audio(input_audio_path: str) -> str:
    
    audio = AudioSegment.from_file(input_audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    
    temp_wav = "temp_converted.wav"
    audio.export(temp_wav, format="wav")
    
    try:
        r = sr.Recognizer()
        with sr.AudioFile(temp_wav) as source:
            audio_data = r.record(source)
        
        text = r.recognize_google(audio_data)
        
        
        with open("transcripts.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        return text
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_wav):
            os.unlink(temp_wav)