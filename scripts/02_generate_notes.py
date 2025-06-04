import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

load_dotenv()
client = OpenAI()

class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str = Field(..., example="Mean Value Theorem")
    summary: str = Field(..., max_length=150)
    page_ref: Optional[int] = Field(None, description="Page number in source PDF")

system = (
    "You are a study summarizer. "
    "Return exactly 10 unique notes that will help prepare for the exam. "
    "Respond *only* with valid JSON matching the Note[] schema."
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Summarize the attached calculus material into 10 exam prep notes."}
    ],
    response_format={"type": "json_object"}
)

print(response.choices[0].message.content)

try:
    data = json.loads(response.choices[0].message.content)
    with open("exam_notes.json", "w") as f:
        json.dump(data, f, indent=2)
except (ValidationError, KeyError, json.JSONDecodeError) as e:
    print("Failed to parse notes:", e)