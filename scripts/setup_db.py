import asyncio
from loguru import logger
from core.settings import settings
import os
async def setup():
    conn = await settings.get_connection()
    logger.info(os.getcwd())
    with open("scripts/schema.sql", "r") as f:
        sql = f.read()
        await conn.execute(sql)
    logger.info("Schema created.")

if __name__ == "__main__":
    asyncio.run(setup())
