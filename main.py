import asyncio
from utils.load_env import load_environment
from agents.base import get_model_client
from agents.math_agent import get_math_agent
from agents.postgres_agent import get_postgres_agent
from agents.fetch_agent import get_fetch_agent
from agents.browser_agent import get_browser_agent
from agents.router_agent import get_router_agent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken

async def main():
    openai_key, _ = load_environment()
    model_client = get_model_client(openai_key)

    # Load all agents
    math_agent = await get_math_agent(model_client)
    postgres_agent = await get_postgres_agent(model_client)
    fetch_agent = await get_fetch_agent(model_client)
    browser_agent = await get_browser_agent(model_client)
    router_agent = get_router_agent(model_client)

    agent_map = {
        "MathAgent": math_agent,
        "PostgreSQLAgent": postgres_agent,
        "FetcherAgent": fetch_agent,
        "BrowserAgent": browser_agent,
    }

    async def route_and_execute(user_query: str):
        print(f"\n🤖 Routing query: {user_query}")
        response = await router_agent.run(task=f"Classify: {user_query}")
        router_text = response.output.strip() if hasattr(response, "output") else str(response).strip()
        print(f"🧭 Router Response: {router_text}")

        for key, agent in agent_map.items():
            if key in router_text:
                print(f"✅ Routing to {key}...\n")
                await Console(agent.run_stream(task=user_query, cancellation_token=CancellationToken()))
                return

        print("❌ Could not determine agent.")

    while True:
        query = input("\n📝 Enter query (or type 'exit'): ")
        if query.lower() == "exit":
            break
        await route_and_execute(query)

if __name__ == "__main__":
    asyncio.run(main())
