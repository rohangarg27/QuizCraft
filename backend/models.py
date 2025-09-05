from pydantic import BaseModel

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5

class QuizResponse(BaseModel):
    questions: list
