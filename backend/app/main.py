from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Quizora Backend",
        "status": "Backend is running"
    }