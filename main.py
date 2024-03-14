from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["students"]
collection = db["boys"]


@app.post("/students/")
async def create_student(name: str, age: int):
    # Insert student data into MongoDB
    result = collection.insert_one({"name": name, "age": age})
    if result.inserted_id:
        return {"message": "Student created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create student")


@app.get("/students/{student_id}")
async def get_student(student_id: str):
    # Retrieve student data from MongoDB
    student = collection.find_one({"_id": student_id})
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")