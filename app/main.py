import os
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from app.llm_client import get_llm_response  # Import LLM function

# Initialize FastAPI
app = FastAPI()

# Get absolute path to the "static" directory
static_path = os.path.join(os.path.dirname(__file__), "static")

# Mount the 'static' directory for serving CSS and JS files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="app/templates")

# Serve the homepage (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chatbot API for AJAX requests (without Pinecone)
@app.post("/get")
async def chat_response(request: Request):
    data = await request.json()
    user_input = data.get("msg", "").strip()

    if not user_input:
        return JSONResponse(content={"response": "Please enter a valid query."}, status_code=400)

    # Generate response from the LLM
    bot_response = get_llm_response(user_input)
    return {"response": bot_response}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Render's provided port or default to 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
