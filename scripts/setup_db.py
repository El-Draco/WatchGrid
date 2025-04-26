from core.settings import settings
from loguru import logger
import os
import re
def setup():
    conn = settings.get_connection()
    cursor = conn.cursor()
    logger.info(f"Current working directory: {os.getcwd()}")

    with open("scripts/schema.sql", "r") as f:
        sql_script = f.read()
        sql_script = re.sub(r'--.*\n', '', sql_script) #this one's to remove comments


    statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
    for stmt in statements:
        try:
            logger.info(f"Executing: {stmt[:60]}...")  # Just preview start of statement
            cursor.execute(stmt)
        except Exception as e:
            logger.error(f"Error executing statement: {e}")
            raise

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("✅ Schema created successfully.")

if __name__ == "__main__":
    setup()
