from fastapi import APIRouter, Path, HTTPException, Query, Depends
from schemas import PatientCreate, PatientUpdate
import crud.patients as patients
from auth import get_current_user, require_role

router = APIRouter(prefix = "/patients", tags = ["Patients"])

@router.get("/")
async def list_patients(current_user = Depends(get_current_user)):
    if current_user["role"] == "patient":
        p = await patients.get_patient_by_user_id(current_user["id"])
        return [p] if p else []
    # admin/doctor -> return all
    return await patients.get_all_patients()

@router.get("/{patient_id}")
async def get_patient(patient_id: str = Path(...), current_user = Depends(get_current_user)):
    rec = await patients.get_patient(patient_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Patient not found")
    if current_user["role"] == "patient":
        # enforce patient can view only their own record
        if rec["user_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Forbidden")
    return rec

@router.post("/", dependencies=[Depends(require_role(["admin", "doctor"]))])
async def create_patient(patient: PatientCreate):
    existing = await patients.get_patient(patient.id)
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists")
    await patients.create_patient(patient)
    return {"message": "Patient created successfully"}

@router.put("/{patient_id}", dependencies=[Depends(require_role(["admin", "doctor"]))])
async def update_patient(patient_id: str, patient_update: PatientUpdate):
    existing = await patients.get_patient(patient_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Patient not found")
    await patients.update_patient(patient_id, patient_update)
    return {"message": "Patient updated"}

@router.delete("/{patient_id}", dependencies=[Depends(require_role(["admin"]))])
async def delete_patient(patient_id: str):
    existing = await patients.get_patient(patient_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Patient not found")
    await patients.delete_patient(patient_id)
    return {"message": "Patient deleted"}