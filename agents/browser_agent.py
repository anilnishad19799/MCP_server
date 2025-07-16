from autogen_ext.tools.mcp import StdioServerParams, create_mcp_server_session, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent

async def get_browser_agent(model_client):
    params = StdioServerParams(
        command="npx",
        args=["@playwright/mcp"],
        read_timeout_seconds=60,
    )

    async with create_mcp_server_session(params) as session:
        await session.initialize()
        tools = await mcp_server_tools(params, session=session)

        browser_agent = AssistantAgent(
            name="BrowserAgent",
            model_client=model_client,
            tools=tools,
            reflect_on_tool_use=True,
            system_message="You browse websites using Playwright."
        )

        # ✅ Don't return the session
        return browser_agent