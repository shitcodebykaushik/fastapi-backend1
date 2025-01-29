from fastapi import FastAPI
from app.routes import auth  # Ensure this import is correct

app = FastAPI()

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "FastAPI Backend with JWT Authentication is Running!"}
