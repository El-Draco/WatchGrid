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
                INSERT INTO Users (user_id, first_name, last_name, email, password_hash, date_of_birth)
                VALUES (:user_id, :fn, :ln, :email, :pw, TO_DATE(:dob, 'YYYY-MM-DD'))
            """, {
            "user_id": user_id,
            "fn": first_name,
            "ln": last_name,
            "email": email,
            "pw": hashed_pw,
            "dob": date_of_birth
        })

        # NEW: Insert blank UserProfileSettings row
        cursor.execute("""
                INSERT INTO UserProfileSettings (user_id)
                VALUES (:user_id)
            """, {"user_id": user_id})

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

def get_current_user():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None

    conn = settings.get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT U.user_id, U.first_name, U.last_name, U.email, U.date_of_birth,
               P.avatar_blob, P.avatar_mime_type
        FROM Users U
        LEFT JOIN UserProfileSettings P ON U.user_id = P.user_id
        WHERE U.user_id = :user_id
    """, {"user_id": user_id})
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return None
    avatar_blob = row[5]
    avatar_mime = row[6]
    if avatar_blob is not None:
        avatar_blob = avatar_blob.read()  # Convert from LOB to bytes
    cur.close()
    conn.close()
    return {
        "user_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "email": row[3],
        "date_of_birth": row[4],
        "avatar_blob": avatar_blob,
        "avatar_mime_type": avatar_mime,
    }

