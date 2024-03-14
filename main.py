from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Asynchronous MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"  # Replace with your actual URL
client = AsyncIOMotorClient(MONGODB_URL)
db = client["students"]
collection = db["boys"]


# Dependency function for database connection
async def get_db():
    yield db


@app.post("/students/")
async def create_student(name: str, age: int, id: int, db: AsyncIOMotorClient = Depends(get_db)):
    result = await collection.insert_one({"name": name, "age": age, "id": id})
    if result.inserted_id:
        return {"message": "Student created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create student")


@app.get("/students/{student_id}")
async def get_student(student_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    try:
        # Convert student_id string to ObjectId
        student_id = ObjectId(student_id)

        # Retrieve student data from MongoDB
        student = await collection.find_one({"_id": student_id})

        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
