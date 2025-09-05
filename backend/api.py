import os
from fastapi import FastAPI, UploadFile, Form
from backend.rag import load_pdf, chunk_text, build_faiss_index, retrieve_chunks
from backend.llm import generate_quiz
from backend.models import QuizRequest, QuizResponse

app = FastAPI(title="QuizLLM API")

@app.post("/ingest/upload")
async def ingest_pdf(file: UploadFile):
    file_path = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    build_faiss_index(chunks)
    return {"status": "indexed", "chunks": len(chunks)}

@app.post("/quiz", response_model=QuizResponse)
async def generate_quiz_api(req: QuizRequest):
    context = " ".join(retrieve_chunks(req.topic))
    quiz_text = generate_quiz(context, req.topic, req.num_questions)
    return QuizResponse(questions=quiz_text.split("\n"))
