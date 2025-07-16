import asyncio
import streamlit as st
from utils.load_env import load_environment
from agents.base import get_model_client
from agents.math_agent import get_math_agent
from agents.postgres_agent import get_postgres_agent
from agents.fetch_agent import get_fetch_agent
from agents.browser_agent import get_browser_agent
from agents.router_agent import get_router_agent
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage

st.set_page_config(page_title="Multi-Agent Autogen", layout="centered")
st.title("🔗 Multi-Agent Query Router")

# --- Initialize Session State ---
for key in ["response", "history", "agent_map", "router_agent", "initialized"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "history" else []

# --- One-time Agent Setup ---
async def setup_agents_once():
    if st.session_state.initialized:
        return

    openai_key, _ = load_environment()
    model_client = get_model_client(openai_key)

    st.session_state.agent_map = {
        "MathAgent": await get_math_agent(model_client),
        "PostgreSQLAgent": await get_postgres_agent(model_client),
        "FetcherAgent": await get_fetch_agent(model_client),
        "BrowserAgent": await get_browser_agent(model_client),
    }
    st.session_state.router_agent = get_router_agent(model_client)
    st.session_state.initialized = True

# --- Route Query to Agent ---
async def route_query(user_query: str):
    router_agent = st.session_state.router_agent
    agent_map = st.session_state.agent_map

    router_response = await router_agent.run(task=f"Classify: {user_query}")
    router_text = router_response.output.strip() if hasattr(router_response, "output") else str(router_response).strip()

    for key, agent in agent_map.items():
        if key in router_text:
            st.markdown(f"🧭 Routed to: `{key}`")
            response = await agent.run(task=user_query, cancellation_token=CancellationToken())

            # Extract only final assistant message
            if hasattr(response, "messages"):
                for msg in reversed(response.messages):
                    if isinstance(msg, TextMessage) and msg.source != "user":
                        return msg.content.strip()
            return str(response)

    return "❌ Could not determine which agent should handle this query."

# --- Main Async Function ---
async def main():
    with st.spinner("🔄 Initializing agents..."):
        await setup_agents_once()

    user_query = st.text_input("Enter your query", placeholder="e.g., Summarize https://example.com or What is 24 * 6?")
    if st.button("Ask"):
        if not user_query.strip():
            st.warning("Please enter a query.")
            return

        with st.spinner("🧠 Processing..."):
            response = await route_query(user_query)

        st.session_state.history.append((user_query, response))
        st.session_state.response = response

    # --- Display Output ---
    if st.session_state.response:
        st.subheader("📥 Response")
        st.success(st.session_state.response)

    # --- Display History ---
    if st.session_state.history:
        with st.expander("📜 History"):
            for q, r in reversed(st.session_state.history):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {r}")
                st.markdown("---")

if __name__ == "__main__":
    asyncio.run(main())
