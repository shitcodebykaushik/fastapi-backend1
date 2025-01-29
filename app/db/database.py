from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./backend.db"  # SQLite Database File

# ✅ Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ✅ Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()

# ✅ Ensure all models are registered and tables are created
def init_db():
    from app.models import user, product, bid, order, notification  # Import all models
    Base.metadata.create_all(bind=engine)

# ✅ Initialize database when the app starts
init_db()
