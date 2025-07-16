from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def get_postgres_agent(model_client):
    postgres_server = StdioServerParams(command="python", args=["tools/postgres_tool_server.py"])
    postgres_tools = await mcp_server_tools(postgres_server)
    return AssistantAgent(
        name="PostgreSQLAgent",
        model_client=model_client,
        tools=postgres_tools,
        reflect_on_tool_use=True,
        system_message=(
            "You are a smart assistant that interacts with a PostgreSQL database using the `sql_query` tool.\n"
            "Always use this tool to answer database-related questions.\n"
            "If the user gives a natural language request (e.g., 'show all products'), convert it into SQL and run it.\n"
            "Only respond with actual results from the tool. Do not guess or simulate data.\n"
            "For risky queries (like DELETE), confirm or warn the user before proceeding.\n"
        ),
    )
