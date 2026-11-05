    
from fastapi import FastAPI

from app.routes.knowledge_routes import router as knowledge_router
from app.routes.question_routes import router as question_router

app = FastAPI(
    title="Quizora API",
    version="1.0.0"
)

app.include_router(knowledge_router)
app.include_router(question_router)


@app.get("/")
def home():
    return {"message": "Welcome to Quizora API"}