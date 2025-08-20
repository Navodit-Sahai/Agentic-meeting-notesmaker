from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(input_audio_path: str) -> str:
    audio = AudioSegment.from_file(input_audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export("converted.wav", format="wav")
    
    r = sr.Recognizer()
    with sr.AudioFile("converted.wav") as source:
        audio_data = r.record(source)
    
    text = r.recognize_google(audio_data)
    
    with open("transcripts.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    return text
