from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.processing import router as whisper_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(whisper_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Whisper App!"}
