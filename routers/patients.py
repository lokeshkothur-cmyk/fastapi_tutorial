from fastapi import APIRouter, Path, HTTPException, Query, Depends
from schemas import Patient, PatientUpdate
import crud.patients as patients_crud
from auth import get_current_user, require_role

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=list[Patient])
async def list_patients(
    sort_by: str = Query(None, enum=["age", "height", "weight"]),
    order: str = Query(None, enum=["asc", "desc"]),
    current_user=Depends(get_current_user)
):
    """
    List patients. Patients see only their record, others see all.
    Supports sorting by age, height, or weight.
    """
    if current_user["role"] == "patient":
        patient = await patients_crud.get_patient_by_user_id(current_user["id"])
        return [patient] if patient else []
    return await patients_crud.get_all_patients(sort_by, order)

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Get a patient by ID. Patients can only view their own record.
    """
    patient = await patients_crud.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if current_user["role"] == "patient" and patient["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return patient

@router.post("/", dependencies=[Depends(require_role(["admin", "doctor"]))], response_model=Patient)
async def create_patient(patient: Patient):
    """
    Create a new patient. Only admin/doctor allowed.
    """
    if await patients_crud.get_patient(patient.id):
        raise HTTPException(status_code=400, detail="Patient already exists")
    await patients_crud.create_patient(patient)
    return patient

@router.put("/{patient_id}", dependencies=[Depends(require_role(["admin", "doctor"]))])
async def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update patient details. Only admin/doctor allowed.
    """
    if not await patients_crud.get_patient(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    await patients_crud.update_patient(patient_id, patient_update)
    return {"message": "Patient updated"}

@router.delete("/{patient_id}", dependencies=[Depends(require_role(["admin"]))])
async def delete_patient(patient_id: str):
    """
    Delete a patient. Only admin allowed.
    """
    if not await patients_crud.get_patient(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    await patients_crud.delete_patient(patient_id)
    return {"message": "Patient deleted"}

@router.get("/filter", response_model=list[Patient])
async def filter_patients(
    min_age: int = Query(None),
    max_age: int = Query(None),
    min_height: float = Query(None),
    max_height: float = Query(None),
    min_weight: float = Query(None),
    max_weight: float = Query(None),
    city: str = Query(None),
    current_user=Depends(get_current_user)
):
    """
    Filter patients by age, height, weight, and city.
    """
    results = await patients_crud.filter_patients(
        min_age, max_age, min_height, max_height, min_weight, max_weight
    )
    if city:
        results = [p for p in results if p["city"].lower() == city.lower()]
    return results