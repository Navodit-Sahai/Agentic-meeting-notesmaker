from pydantic import BaseModel
from fastapi import FastAPI
from audio_processing import transcribe_audio
from llm_handling import generate_summary

app = FastAPI()

class Input(BaseModel):
    audio_path: str

@app.post("/notesmaker")
def notesmaker(request: Input):
    transcript = transcribe_audio(request.audio_path)
    summary = generate_summary(transcript)
    return {"summary": summary}
