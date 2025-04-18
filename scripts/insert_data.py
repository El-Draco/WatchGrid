import asyncio
import requests
from schemas.movie import Movie
from core.settings import settings
from loguru import logger
async def insert_movie(movie: Movie):
    conn = await settings.get_connection()
    await conn.execute("""
        INSERT INTO Movie (movie_id, title, release_date, duration, language, image_url, avg_rating)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (movie_id) DO NOTHING
    """,
        movie.movie_id,
        movie.title,
        movie.release_date,
        movie.duration,
        movie.language,
        movie.image_url,
        movie.avg_rating
    )

def fetch_movies_from_tmdb(limit=10):
    res = requests.get(settings.TMDB_URL, params={
        "api_key": settings.API_KEY,
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
                duration=None,                  # TMDb doesn't give runtime here...need to figure out what to do
                language=m["original_language"],
                image_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m["poster_path"] else None,
                avg_rating=m["vote_average"]
            )
            formatted.append(movie)
        except Exception as e:
            logger.error(f"Skipping invalid movie: {m.get('title', '?')}. Reason: {e}")

    return formatted

async def main():
    movies = fetch_movies_from_tmdb()
    logger.info(f"Fetched {len(movies)} movies from TMDb")
    for movie in movies:
        await insert_movie(movie)
    logger.info("All movies inserted.")

if __name__ == "__main__":
    asyncio.run(main())