from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PASS = os.getenv("DATABASE_Pass")

DATABASE_URL = f"postgresql://postgres:{DATABASE_PASS}@localhost/snack_track"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
