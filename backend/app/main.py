from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

# Models
class ChatRequest(BaseModel):
    message: str
    case_context: str

# Routes
@app.get("/cases")
def get_cases():
    return [
        {"id": 1, "name": "Fever and Fatigue", "specialty": "Internal Medicine", "difficulty": "Easy"},
        {"id": 2, "name": "Chest Pain", "specialty": "Cardiology", "difficulty": "Medium"},
        {"id": 3, "name": "Shortness of Breath", "specialty": "Pulmonology", "difficulty": "Hard"},
    ]

@app.post("/chat")
def chat(request: ChatRequest):
    prompt = f"You are simulating a patient for this medical case:\n{request.case_context}\n\nStudent: {request.message}\nPatient:"
    response = model.generate_content(prompt)
    return {"reply": response.text}
