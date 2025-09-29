from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "mysql+aiomysql://example_user:password@localhost/patient_management"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL.replace("+aiomysql", ""))