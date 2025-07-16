from autogen_agentchat.agents import AssistantAgent

def get_router_agent(model_client):
    return AssistantAgent(
        name="RouterAgent",
        model_client=model_client,
        tools=[],
        system_message = (
            "You are a routing assistant. Classify the user's query and decide which agent should handle it.\n\n"
            "Agents:\n"
            "- MathAgent: Math problems or calculations.\n"
            "- PostgreSQLAgent: SQL or database-related queries.\n"
            "- FetcherAgent: Summarize content from a given URL.\n"
            "- BrowserAgent: Navigate or interact with websites using Playwright.\n\n"
            "Reply ONLY in this format:\n"
            "ROUTE_TO: <agent_name>\n"
            "Example: ROUTE_TO: MathAgent\n\n"
            "Do not answer or explain the query. Just route it."
        )
    )
