from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./backend.db"  # SQLite Database

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Ensure all models are created
def init_db():
    from app.models import user, product,bid  # Import models before table creation
    Base.metadata.create_all(bind=engine)

init_db()  # Run this to create tables
