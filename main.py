from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Student, Feedback
from database import students
from nlp_utils import analyze_sentiment, smart_search


app = FastAPI(
    title = "AI-Powerd Student RESTful API",
    version = "1.0.0"
)

#Home API

@app.get("/")
def home():
    return{
        "message":"running sucessfully"
    }



# ---ADD STUDENT---

@app.post("/students")
def create_students(student : Student):
    students.append(student.model_dump())

#--- GET ALL STUDENT---
@app.get("/students")
def get_all_students():
    return students

# --- GET STUDENT BY ID ---
@app.get("/students/{student_id}")
def get_student(student_id : int):
    result = [s for s in students if s["id"] == student_id]
    return {
        "result" : result
    }


# ----ANALYZE-FEEDBACK ---
@app.post("/analyze-feedback")
def analyze_feedback(feed: Feedback):
    result = analyze_sentiment(feed.text)
    return{
        "text":feed.text,
        "analysis":result
    }

#---- SEARCH -----
@app.post("/search")
def search_students(query : str):
    result = smart_search(students,query)

    if not result:
        raise HTTPException(status_code=404,detail="No matchin student found")

    return {
        "count" : len(result),
        "students" : result
    }