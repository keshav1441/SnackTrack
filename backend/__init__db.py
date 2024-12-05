# initdb.py
from database import engine, Base
from models import User, Order

# Create all tables in the database (this will create tables based on the models)
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
