from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

class Patient(BaseModel):
    id: str = Field(..., description="ID of the patient", example="P001")
    name: str = Field(..., description="Name of the patient")
    city: str = Field(..., description="City where the patient lives")
    age: int = Field(..., description="Age of the patient")
    gender: Literal["male", "female", "Others"] = Field(..., description="Gender of the patient")
    height: float = Field(..., gt=0, description="Height in meters")
    weight: float = Field(..., gt=0, description="Weight in kilograms")
    bmi: Optional[float] = Field(None, description="BMI value")
    verdict: Optional[str] = Field(None, description="BMI verdict")

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[Literal["male", "female", "Others"]] = None
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "doctor", "patient"] = "patient"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str