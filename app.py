import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
client = AsyncIOMotorClient(os.environ.get("MONGODB_URL", "mongodb://localhost:27017/temperatur_db"))
db = client.temperatur_db
temp_collection = db.temperaturen
# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class TemperaturModel(BaseModel):
    temperatur: int

def serialize_temperatur(doc):
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@app.post("/temperatur/", response_description="Add new temperatur", status_code=status.HTTP_201_CREATED)
async def create_temperatur(temperatur: TemperaturModel = Body(...)):
    """
    Insert a new temperatur record.

    A unique `id` will be created and provided in the response.
    """
    if not isinstance(temperatur.temperatur, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Temperatur must be an integer.",
        )
    new_temperatur = await temp_collection.insert_one({"temperatur": temperatur.temperatur})
    created_temperatur = await temp_collection.find_one(
        {"_id": new_temperatur.inserted_id}
    )
    return serialize_temperatur(created_temperatur)

@app.get("/temperatur/", response_description="List all temperatur records")
async def list_temperatur():
    """
    List all temperatur records.
    """
    temperatur = await temp_collection.find().to_list(100)
    return {"temperatur": [serialize_temperatur(t) for t in temperatur]}