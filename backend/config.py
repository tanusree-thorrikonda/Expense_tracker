import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

class Config:
    SECRET_KEY ='dev-secret-key-12345'
    # We will store the database in the backend/instance directory
    # SQLAlchemy will search relative to the app instance folder if sqlite://// relative path is used
    # e.g. sqlite:///expense_tracker.db goes to backend/instance/expense_tracker.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expense_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
