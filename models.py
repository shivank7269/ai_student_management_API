from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    id : int
    name: str
    age: int
    course: str
    email: Optional[str] = None


class Feedback(BaseModel):
    text : str