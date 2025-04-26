import pytest
from loguru import logger
from core.settings import settings


@pytest.mark.asyncio
async def test_oracle_connection() -> None:
    try:
        conn = settings.get_connection()

        cursor = conn.cursor()
        cursor.execute("SELECT 'Oracle connected successfully!' FROM dual")
        result = cursor.fetchone()
        logger.info(result)
        conn.close()

        assert result[0] == 'Oracle connected successfully!'

    except Exception as e:
        assert False, f"Oracle connection failed: {e}"
