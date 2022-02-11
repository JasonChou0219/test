from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from pydantic import PostgresDsn


SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql",
            user='postgres',
            password='DIB-central',
            host='db-backend-gateway',
            path=f"/backend-gateway",
        )


engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

print(db.query(text("1")).from_statement(text("SELECT 1")).all())

