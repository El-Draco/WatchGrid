from io import BytesIO
from PIL import Image
from core.settings import settings

def get_avatar_from_db(user_id):
    conn = settings.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT avatar_blob, avatar_mime_type FROM Users WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row if row and row[0] else None


def save_avatar_to_db(uploaded_file, user_id):
    img = Image.open(uploaded_file)
    img = img.convert("RGB")
    img.thumbnail((256, 256))  # Resize while maintaining aspect ratio

    # Create a clean 256x256 white background
    canvas = Image.new('RGB', (256, 256), (255, 255, 255))
    img_position = (
        (256 - img.width) // 2,
        (256 - img.height) // 2
    )
    canvas.paste(img, img_position)

    buffer = BytesIO()
    canvas.save(buffer, format="JPEG", optimize=True, quality=70)
    binary_data = buffer.getvalue()

    conn = settings.get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE UserProfileSettings
        SET avatar_blob = :avatar_blob, avatar_mime_type = :avatar_mime_type
        WHERE user_id = :user_id
    """, {
        "avatar_blob": binary_data,
        "avatar_mime_type": "image/jpeg",
        "user_id": user_id
    })
    conn.commit()
    cur.close()
    conn.close()

