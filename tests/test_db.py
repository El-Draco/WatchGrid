from core.db import get_connection
import pytest
from loguru import logger

@pytest.mark.asyncio
async def test_pg_connection():
    try:
        logger.info("Getting connection...")
        conn = await get_connection()
        logger.info("Running query...")
        result = await conn.fetchval("SELECT 'Postgres connected!'")
        await conn.close()
        assert result == 'Postgres connected!'
    except Exception as e:
        assert False, f"PostgreSQL connection failed: {e}"
