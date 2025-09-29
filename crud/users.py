from database import database
from models import users
from schemas import UserCreate

async def get_user_by_username(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

async def create_user(user: UserCreate):
    from security import get_password_hash
    hashed = get_password_hash(user.password)
    query = users.insert().values(
        username=user.username,
        email=user.email,
        password=hashed,
        role=user.role
    )
    await database.execute(query)