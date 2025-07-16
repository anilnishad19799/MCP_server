from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def get_math_agent(model_client):
    math_server = StdioServerParams(command="python", args=["tools/math_server.py"])
    math_tools = await mcp_server_tools(math_server)
    return AssistantAgent(
        name="MathAgent",
        model_client=model_client,
        tools=math_tools,
        reflect_on_tool_use=True,
        system_message="You are a math assistant. Handle math-related questions using the math tool."
    )
