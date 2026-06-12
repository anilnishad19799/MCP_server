# postgres_tool_server.py

import os
from mcp.server.fastmcp import FastMCP
import psycopg2

# Connect to PostgreSQL using environment variables with defaults
conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    database=os.getenv("PGDATABASE", "postgres"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "63540@Post")
)

mcp = FastMCP("PostgreSQL")

@mcp.tool()
def sql_query(query: str) -> list:
    """
    Execute a SQL query on the PostgreSQL database and return the result.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            try:
                return cur.fetchall()
            except psycopg2.ProgrammingError:
                return ["Query executed successfully, no rows returned."]
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    mcp.run(transport="stdio")
