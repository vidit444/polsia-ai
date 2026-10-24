from fastapi import FastAPI

app = FastAPI(title="Polsia-AI", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "polsia-ai"}

@app.get("/")
async def root():
    return {"message": "Polsia-AI API is running successfully"}
