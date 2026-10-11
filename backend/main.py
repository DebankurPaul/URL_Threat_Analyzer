from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers.analyze import router

load_dotenv()

app = FastAPI(
    title="URL Threat Analyzer",
    description="Analyzes URLs using VirusTotal, SSL, and IP intelligence",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000","https://url-threat-analyzer-frontend.onrender.com",],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

@app.get("/")
def root():
    return {"status" : "ok", "message" : "API is running"}