# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from crud.users import get_user_by_username
from security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")  # used in docs

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(username)
    if not user:
        raise credentials_exception
    return user  # this is a Record/Mapping with keys from users table

def require_role(allowed_roles: list):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return role_checker
