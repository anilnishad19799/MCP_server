# postgres_tool_server.py

from mcp.server.fastmcp import FastMCP
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="63540@Post"
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
