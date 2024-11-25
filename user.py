# user.py

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models import User  # Import User model from models.py
from database import Session as db_session  # Import the Session from database.py

def register_user(username, password):
    # Hash the password before saving it
    hashed_password = generate_password_hash(password)  # Hash the password securely
    session = db_session()
    try:
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error during user registration: {e}")
        return False
    finally:
        session.close()

def login_user(username, password):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Compare the hash
            return True
        return False
    finally:
        session.close()

def logout_user():
    session.pop('user_id', None)  # Log out by removing user session

def is_logged_in():
    return 'user_id' in session  # Check if user is logged in
