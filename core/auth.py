import streamlit as st
import hashlib
from core.settings import settings
import uuid

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Check if a password matches the hash."""
    return hash_password(password) == hashed_password

def get_connection():
    return settings.get_connection()

def register_user(email: str, password: str, first_name: str, last_name: str, date_of_birth: str):
    """Register a new user in the database."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute("SELECT COUNT(*) FROM Users WHERE email = :1", (email,))

        if cursor.fetchone()[0] > 0:
            st.error("Email already registered. Please log in.")
            return False

        hashed_pw = hash_password(password)
        user_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO Users (user_id, first_name, last_name, email, date_of_birth, password_hash)
            VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6)
        """, (user_id, first_name, last_name, email, date_of_birth, hashed_pw))

        conn.commit()
        st.success("Account created successfully! Please login.")
        return True

    except Exception as e:
        st.error(f"Registration failed: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def login_user(email: str, password: str):
    """Log a user into the session."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT User_ID, password_hash
            FROM Users
            WHERE Email = :1
        """, (email,))

        user = cursor.fetchone()

        if not user:
            st.error("Email not found. Please register first.")
            return False

        user_id, stored_hash = user

        if verify_password(password, stored_hash):
            st.session_state["user_id"] = user_id
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Incorrect password. Please try again.")
            return False

    except Exception as e:
        st.error(f"Login failed: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def logout_user():
    """Log out the user."""
    if "user_id" in st.session_state:
        del st.session_state["user_id"]

def is_logged_in():
    """Check if user is logged in."""
    return "user_id" in st.session_state and st.session_state["user_id"] is not None
