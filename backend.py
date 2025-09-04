from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from audio_processing import transcribe_audio
from llm_handling import generate_summary
import os

app = FastAPI()

class Input(BaseModel):
    audio_path: str

@app.post("/notesmaker")
def notesmaker(request: Input):
    try:
        if not os.path.exists(request.audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        transcript = transcribe_audio(request.audio_path)
        summary = generate_summary(transcript)
        return {"summary": summary}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Notes Maker API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
