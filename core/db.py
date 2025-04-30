import oracledb
from core.settings import settings
# def get_connection(settings):
#
#     return conn
def get_movie_by_title(title: str):
    conn = settings.get_connection()
    cursor = conn.cursor()

    query = "SELECT movie_id, title FROM Movie WHERE LOWER(title) = LOWER(:1)"
    cursor.execute(query, [title])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result  # returns (movie_id, title) or None
