from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def get_fetch_agent(model_client):
    fetch_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    fetch_tools = await mcp_server_tools(fetch_server)
    return AssistantAgent(
        name="FetcherAgent",
        model_client=model_client,
        tools=fetch_tools,
        reflect_on_tool_use=True,
        system_message = (
            "You summarize webpage content using the fetch tool.\n"
            "Only fetch when a valid URL is provided.\n"
            "Return clear, concise summaries based on the fetched content.\n"
            "Do not guess or generate your own text."
        )
    )
