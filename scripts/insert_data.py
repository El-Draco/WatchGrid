import requests
from models.movie import Movie
from core.settings import settings
from loguru import logger

def insert_movies(movies):
    conn = settings.get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO Movie (movie_id, title, release_date, duration, language, image_url, avg_rating)
        VALUES (:1, :2, :3, :4, :5, :6, :7)
    """

    for movie in movies:
        try:
            cursor.execute(insert_query, [
                movie.movie_id,
                movie.title,
                movie.release_date,
                movie.duration,
                movie.language,
                movie.image_url,
                movie.avg_rating
            ])
        except Exception as e:
            logger.error(f"Failed to insert movie {movie.title}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("✅ All movies inserted and committed successfully.")

def fetch_movies_from_tmdb(limit=10):
    res = requests.get(settings.TMDB_URL, params={
        "api_key": settings.TMDB_API_KEY,
        "language": "en-US",
        "page": 1
    })

    if res.status_code != 200:
        raise Exception("Failed to fetch from TMDb")

    movies = res.json().get("results", [])[:limit]
    formatted = []

    for m in movies:
        try:
            movie = Movie(
                movie_id=m["id"],
                title=m["title"],
                release_date=m["release_date"],
                duration=None,  # TMDb doesn't provide it here
                language=m["original_language"],
                image_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m["poster_path"] else None,
                avg_rating=m["vote_average"]
            )
            formatted.append(movie)
        except Exception as e:
            logger.error(f"Skipping invalid movie: {m.get('title', '?')}. Reason: {e}")

    return formatted

def main():
    movies = fetch_movies_from_tmdb()
    logger.info(f"Fetched {len(movies)} movies from TMDb")
    insert_movies(movies)

if __name__ == "__main__":
    main()