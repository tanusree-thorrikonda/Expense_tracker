from flask_sqlalchemy import SQLAlchemy

# Initialize the db instance
db = SQLAlchemy()

from .user import User
from .transaction import Transaction
