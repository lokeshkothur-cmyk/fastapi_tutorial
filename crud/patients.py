from database import database
from models import patients
from schemas import PatientCreate, PatientUpdate
from sqlalchemy import select, func


async def get_all_patients():
    query = patients.select()
    return await database.fetch_all(query)


async def get_patient(patient_id : str):
    query = patients.select().where(patients.c.id == patient_id)
    return await database.fetch_one(query)

async def get_patient_by_user_id(user_id: int):
    query = patients.select().where(patients.c.user_id == user_id)
    return await database.fetch_one(query)


async def create_patient(patient : PatientCreate):
    query = patients.insert().values(
        id = patient.id,
        name = patient.name,
        city = patient.city,
        age = patient.age,
        gender = patient.gender,
        height = patient.height,
        weight = patient.weight
    )
    await database.execute(query)


async def update_patient(patient_id : str, patient_update : PatientUpdate):
    query = patients.update().where(patients.c.id == patient_id).values(
        {k : v for k, v in patient_update.model_dump(exclude_unset = True).items()}
    )
    return await database.execute(query)


async def delete_patient(patient_id : str):
    query = patients.delete().where(patients.c.id == patient_id)
    return await database.execute(query)



async def filter_patients(
        min_age: int = None, max_age : float = None,
        min_height : float = None, max_height: float = None,
        min_weight : float = None, max_weight : float = None 
):
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