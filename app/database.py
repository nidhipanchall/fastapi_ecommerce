from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ Replace 'yourpassword' with your actual PostgreSQL password
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Admin@localhost/ecommerce"

# ✅ Removed 'check_same_thread' because it's only for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
