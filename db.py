from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql://postgres:LAWChronos2023@db.jajssvkoatsxnwizajch.supabase.co:5432/postgres"

engine=create_engine(
    DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()