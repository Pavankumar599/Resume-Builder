from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import json

Base = declarative_base()
engine = create_engine("sqlite:///students.db")
SessionLocal = sessionmaker(bind=engine)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile_json = Column(Text)

Base.metadata.create_all(engine)