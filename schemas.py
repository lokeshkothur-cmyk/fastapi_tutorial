from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional


class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient", example = "P001")]
    name : Annotated[str, Field(..., description = "Name of the patient")]
    city : Annotated[str, Field(..., description = "City where the patient lives")]
    age : Annotated[int, Field(..., description = "Age of the patient")]
    gender : Annotated[Literal["male", "female", "others"], Field(..., description = "Gender of the patient")]
    height : Annotated[float, Field(..., gt = 0, description = "Heght of the patient in mtrs")]
    weight : Annotated[float, Field(..., gt = 0, description = "Weight of the patient in Kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  self.weight / (self.height ** 2)
        return round(bmi, 2)


    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obesse"
        

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default = "None")]
    city : Annotated[Optional[str], Field(default = "None")]
    age : Annotated[Optional[int], Field(default = "None", gt = 0)]
    gender : Annotated[Optional[Literal["male", "female"]], Field(default = "None")]
    height : Annotated[Optional[float], Field(default = "None", gt = 0)]
    weight : Annotated[Optional[float], Field(default = "None", gt = 0)]


class PatientCreate(Patient):
    id: str = Field(..., example="P001")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "patient"

class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"