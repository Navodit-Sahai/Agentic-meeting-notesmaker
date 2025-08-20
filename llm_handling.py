from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

def generate_summary(transcript_text: str) -> str:
    template = """
    From the following transcript:
    {transcript}

    - Give a 5-line summary of the meeting.
    - List all action items: who is responsible, what they need to do, and by when.
    - Mention any key decisions made.
    - Highlight any risks or blockers discussed.
    """

    prompt = PromptTemplate(input_variables=["transcript"], template=template)
    llm = ChatGroq(model_name="llama3-70b-8192")
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"transcript": transcript_text})
    return response
