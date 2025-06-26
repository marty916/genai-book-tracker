from fastapi import FastAPI, Query
from pydantic import BaseModel
from src.genai import get_book_response

app = FastAPI()

class BookRequest(BaseModel):
    query: str

@app.post("/book_request")
def book_request(request: BookRequest):
    result = get_book_response(request.query)
    return result
