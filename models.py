from sqlalchemy import Table, Column, Integer, String, Float, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key = True, autoincrement = True),
    Column("name", String(100), unique = True, nullable = False),
    Column("email", String(150), unique = True, nullable = False),
    Column("password", String(255), nullable = False),
    Column("role", Enum("admin", "doctor", "patient"), nullable=False, default="patient"),
    Column("created_at", TIMESTAMP, server_default=func.now()),
)

patients = Table(
    "patients",
    metadata,
    Column("id", String(10), primary_key = True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=True),
    Column("name", String(100), nullable = False),
    Column("city", String(100), nullable = False),
    Column("age", Integer),
    Column("gender", Enum("male", "Female", "Others"), nullable = False),
    Column("height", Float),
    Column("weight", Float),
    Column("created_at", TIMESTAMP, server_default=func.now())
)