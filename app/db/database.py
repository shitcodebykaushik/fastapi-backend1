from sqlalchemy import create_engine, MetaData
from databases import Database

# SQLite Database URL
DATABASE_URL = "sqlite:///./backend.db"

# Async Database Connection
database = Database(DATABASE_URL)

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
