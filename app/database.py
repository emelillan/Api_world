from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


username = "ezequielmelillan"
password = "new_password"
ip_address_hostname = 'localhost'
database_name = "Fastapi_1"

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{ip_address_hostname}/{database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

