from fastapi import APIRouter
from groq import Groq
import os

router = APIRouter()
client = Groq(api_key="api_key")

@router.post("/chat")
def chat(data: dict):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You help only with stock and offers."},
            {"role": "user", "content": data["question"]}
        ]
    )
    return {"answer": response.choices[0].message.content}
