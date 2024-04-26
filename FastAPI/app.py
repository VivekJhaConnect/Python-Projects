from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students  = {
    1: {
        "name": "Vivek",
        "age": 30,
        "year": "10+ years"
    }
}

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

class Student(BaseModel):
    name: str
    age: int
    year: str 

@app.get('/')
def index():
    return {"name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="This is the student id, which record you want to view.", gt=0, lt=2)):
    return students[student_id]

@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None,  test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in student:
        return {'Error': "Student exists"}
    
    student[student_id] = students
    return students[student_id]

@app.put("/update=student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
     
    if student.name != None:
        students[student_id].name =  student.name

    if student.age != None:
        students[student_id].age =  student.age

    if student.year != None:
        students[student_id].year =  student.year
    #  students[student_id] = student

    return students[student_id]

@app.delete('/student_delete/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist."}
    
    del students[student_id]

    return {"Message": "Student is deletion Successfully."}