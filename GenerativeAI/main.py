from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import google.generativeai as palm

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Set up API key and defaults
palm.configure(api_key="replace with your api token")
defaults = {
    "model": "models/text-bison-001",
    "temperature": 0.7,
    "candidate_count": 1,
    "top_k": 40,
    "top_p": 0.95,
    "max_output_tokens": 1024,
    "stop_sequences": [],
}


@app.get("/", response_class=JSONResponse)
async def get_chatbot(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})


@app.post("/generate_text", response_class=JSONResponse)
async def generate_text(prompt: str = Form(...)):
    response = palm.generate_text(**defaults, prompt=prompt)
    return {"result": response.result}
