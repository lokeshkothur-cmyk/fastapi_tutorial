from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserLogin, Token
from security import verify_password, create_access_token
from crud.users import get_user_by_username, create_user

router = APIRouter(prefix = "/users", tags = ["Users"])

@router.post("/signup", status_code = 201)
async def signup(user : UserCreate):
    existing = await get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    await create_user(user)
    return {"message" : "User created successfully"}


@router.post("/login")
async def login(user : UserLogin):
    db_user = await get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token_data = {"sub": db_user["username"], "role": db_user["role"], "id": db_user["id"]}
    token = create_access_token(token_data)
    return {"access_token" : token, "token_type" : "bearer"}