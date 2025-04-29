from PIL import Image
import streamlit as st
from io import BytesIO
from core.settings import settings
from core.auth import get_current_user
from core.profile_settings import save_avatar_to_db
import imghdr
import datetime
from core.auth import is_logged_in

def is_allowed_image(file_bytes):
    kind = imghdr.what(None, file_bytes)
    return kind in ["jpeg", "png", "jpg"]

# --- Page Config ---
st.set_page_config(page_title="Profile Settings", page_icon="👤")
st.markdown("## 👤 Profile Settings")

with st.sidebar:
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/watchlist.py", label="🎬 Watchlists")
    st.page_link("pages/profile_settings.py", label="⚙️ Settings")


if not is_logged_in():
    st.warning("Please login to access your access your profile settings.")
    st.stop()


# --- Auth Check ---
user = get_current_user()
if user is None:
    st.warning("Please log in to access your profile.")
    st.stop()

# --- Show Avatar ---
if user["avatar_blob"]:
    st.image(user["avatar_blob"], width=128)
else:
    st.image("static/avatars/default_avatar.jpg", width=128)

# --- File Upload ---
uploaded_avatar = st.file_uploader("Upload new avatar", type=["jpg", "jpeg", "png"])

# --- Profile Form ---
# --- Profile Form ---
with st.form("profile_form"):
    fn = st.text_input("First Name", value=user["first_name"])
    ln = st.text_input("Last Name", value=user["last_name"])

    today = datetime.date.today()
    min_dob = datetime.date(today.year - 100, 1, 1)  # 100 years ago
    max_dob = datetime.date(today.year - 10, today.month, today.day)  # must be at least 10 y/o

    # Fix type mismatch (datetime -> date)
    existing_dob = user["date_of_birth"]
    if isinstance(existing_dob, datetime.datetime):
        existing_dob = existing_dob.date()

    # Clamp if out of bounds
    if existing_dob < min_dob or existing_dob > max_dob:
        existing_dob = datetime.date(today.year - 18, 1, 1)  # default to 18 y/o

    dob = st.date_input(
        "Date of Birth",
        value=existing_dob,
        min_value=min_dob,
        max_value=max_dob
    )
    submit = st.form_submit_button("Save Changes")
    if submit:
        if not fn.strip():
            st.error("First name cannot be empty.")
            st.stop()

        if not ln.strip():
            st.error("Last name cannot be empty.")
            st.stop()
        import datetime

        if dob > datetime.date.today():
            st.error("Date of birth cannot be in the future.")
            st.stop()

        # Save avatar if uploaded
        if uploaded_avatar:
            file_bytes = uploaded_avatar.read()

            if not is_allowed_image(file_bytes):
                st.error("Uploaded file must be a valid JPEG or PNG image.")
                st.stop()

            if uploaded_avatar.size > 1_000_000:  # 1MB
                st.error("Avatar must be less than 1MB.")
                st.stop()
            save_avatar_to_db(uploaded_avatar, user["user_id"])

        # Save name & DOB
        conn = settings.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Users
            SET first_name = :fn,
                last_name = :ln,
                date_of_birth = TO_DATE(:dob, 'YYYY-MM-DD')
            WHERE user_id = :user_id
        """, {
            "fn": fn,
            "ln": ln,
            "dob": dob.strftime("%Y-%m-%d"),
            "user_id": user["user_id"]
        })

        conn.commit()
        cur.close()
        conn.close()
        st.success("Profile updated.")
        st.rerun()
