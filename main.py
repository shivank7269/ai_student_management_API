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

# create student (POST)
@app.post('/students', response_model= Student)
def create_student(student: Student):   #student is the request body and its type is Student(JSON object)
    students.append(student.model_dump())
    return student

@app.get("/students")
def get_student():
    return {
        "length":len(students),
        "students":students
    }

@app.get("/students/{student_id}",response_model = Student)
def get_student(student_id : int):
    if student_id<0 or student_id >= len(students):
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id : int, updated_student: Student):
    if student_id<0 or student_id >= len(students):
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    students[student_id] = updated_student
    return {
        "message":"Student updated successfully",
        "data": updated_student
    }

@app.delete("/students/{student_id}")
def delete_student(student_id : int):
    if student_id<0 or student_id >= len(students):
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    deleted_student=students.pop(student_id)
    return {
        "message":"Student deleted successfully",
        "data": deleted_student
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
@app.get("/search")
def search_students(query : str):
    result = smart_search(students,query)

    if not result:
        raise HTTPException(status_code=404,detail="No matchin student found")

    return {
        "count" : len(result),
        "students" : result
    }