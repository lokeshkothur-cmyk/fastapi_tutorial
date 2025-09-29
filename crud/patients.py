from database import database
from models import patients
from schemas import Patient, PatientUpdate
from sqlalchemy import asc, desc
from typing import Optional, List, Dict, Any

async def get_all_patients(sort_by: Optional[str] = None, order: Optional[str] = None) -> List[Dict[str, Any]]:
    query = patients.select()
    if sort_by in {"age", "height", "weight"} and order in {"asc", "desc"}:
        direction = asc if order == "asc" else desc
        query = query.order_by(direction(getattr(patients.c, sort_by)))
    return await database.fetch_all(query)

async def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    query = patients.select().where(patients.c.id == patient_id)
    return await database.fetch_one(query)

async def get_patient_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    query = patients.select().where(patients.c.user_id == user_id)
    return await database.fetch_one(query)

async def calculate_bmi(height: float, weight: float) -> tuple[Optional[float], Optional[str]]:
    if not height or not weight:
        return None, None
    bmi = round(weight / (height ** 2), 2)
    if bmi < 18.5:
        verdict = "Underweight"
    elif bmi < 25:
        verdict = "Normal"
    elif bmi < 30:
        verdict = "Overweight"
    else:
        verdict = "Obese"
    return bmi, verdict

async def create_patient(patient: Patient) -> None:
    bmi, verdict = await calculate_bmi(patient.height, patient.weight)
    query = patients.insert().values(
        id=patient.id,
        name=patient.name,
        city=patient.city,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight,
        bmi=bmi,
        verdict=verdict,
    )
    await database.execute(query)

async def update_patient(patient_id: str, patient_update: PatientUpdate) -> None:
    updated_data = {k: v for k, v in patient_update.model_dump(exclude_unset=True).items()}
    if "height" in updated_data or "weight" in updated_data:
        existing = await get_patient(patient_id)
        height = updated_data.get("height", existing["height"])
        weight = updated_data.get("weight", existing["weight"])
        bmi, verdict = await calculate_bmi(height, weight)
        updated_data["bmi"] = bmi
        updated_data["verdict"] = verdict
    query = patients.update().where(patients.c.id == patient_id).values(updated_data)
    await database.execute(query)

async def delete_patient(patient_id: str) -> None:
    query = patients.delete().where(patients.c.id == patient_id)
    await database.execute(query)

async def filter_patients(
    min_age: Optional[int] = None, max_age: Optional[int] = None,
    min_height: Optional[float] = None, max_height: Optional[float] = None,
    min_weight: Optional[float] = None, max_weight: Optional[float] = None
) -> List[Dict[str, Any]]:
    query = patients.select()
    if min_age is not None:
        query = query.where(patients.c.age >= min_age)
    if max_age is not None:
        query = query.where(patients.c.age <= max_age)
    if min_height is not None:
        query = query.where(patients.c.height >= min_height)
    if max_height is not None:
        query = query.where(patients.c.height <= max_height)
    if min_weight is not None:
        query = query.where(patients.c.weight >= min_weight)
    if max_weight is not None:
        query = query.where(patients.c.weight <= max_weight)
    return await database.fetch_all(query)