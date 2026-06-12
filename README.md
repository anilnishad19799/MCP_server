# Multi-Agent MCP Server

This project implements a multi-agent system using Microsoft's AutoGen framework and Model Context Protocol (MCP) servers. The system provides specialized agents for:

- **MathAgent**: Performs mathematical calculations
- **PostgreSQLAgent**: Interacts with a PostgreSQL database
- **FetcherAgent**: Summarizes webpage content from URLs
- **BrowserAgent**: Navigates and interacts with websites using Playwright

The agents are coordinated by a RouterAgent that directs user queries to the appropriate specialized agent.

## Features

- Modular agent architecture
- MCP integration for tool access
- Streamlit web interface for easy interaction
- Docker support for containerized deployment
- Environment variable configuration

## Prerequisites

- Python 3.10 or higher
- Node.js (for Playwright MCP server)
- PostgreSQL database (optional, for PostgreSQLAgent)
- OpenAI API key
- Apify API key (for BrowserAgent)

## Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MCP_server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   APIFY_API_KEY=your_apify_api_key
   PGHOST=localhost          # Optional, defaults to localhost
   PGDATABASE=postgres       # Optional, defaults to postgres
   PGUSER=postgres           # Optional, defaults to postgres
   PGPASSWORD=your_password  # Optional, defaults to 63540@Post
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t mcp-server .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 \
     -e OPENAI_API_KEY=your_openai_api_key \
     -e APIFY_API_KEY=your_apify_api_key \
     -e PGHOST=localhost \
     -e PGDATABASE=postgres \
     -e PGUSER=postgres \
     -e PGPASSWORD=your_password \
     mcp-server
   ```

## Usage

### Running Locally

Start the Streamlit application:
```bash
streamlit run app.py
```

Then navigate to `http://localhost:8501` in your web browser.

### Running with Docker

After starting the container as shown above, access the application at `http://localhost:8501`.

## Available Agents

1. **MathAgent**: Handles mathematical queries using the math MCP server (addition, multiplication)
2. **PostgreSQLAgent**: Executes SQL queries against a PostgreSQL database
3. **FetcherAgent**: Fetches and summarizes content from URLs using the mcp-server-fetch tool
4. **BrowserAgent**: Uses Playwright to navigate and interact with websites
5. **RouterAgent**: Determines which specialized agent should handle a user query

## Project Structure

```
MCP_server/
├── .git/
├── .gitignore
├── .kimchi/
├── agents/
│   ├── base.py
│   ├── browser_agent.py
│   ├── fetch_agent.py
│   ├── math_agent.py
│   ├── postgres_agent.py
│   └── router_agent.py
├── tools/
│   ├── __init__.py
│   ├── math_server.py
│   └── postgres_tool_server.py
├── utils/
│   ├── __init__.py
│   └── load_env.py
├── app.py              # Streamlit web interface
├── main.py             # Console-based interface
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build instructions
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `APIFY_API_KEY` | Apify API key for BrowserAgent (required) | - |
| `PGHOST` | PostgreSQL host | `localhost` |
| `PGDATABASE` | PostgreSQL database name | `postgres` |
| `PGUSER` | PostgreSQL username | `postgres` |
| `PGPASSWORD` | PostgreSQL password | `63540@Post` |

## Notes

- The BrowserAgent requires the `@playwright/mcp` package, which is installed via `npx` at runtime.
- The FetcherAgent uses the `mcp-server-fetch` package, installed via `uvx` at runtime.
- Math and PostgreSQL agents use local MCP servers implemented in Python.

## Troubleshooting

- If you encounter issues with Playwright, ensure you have run `playwright install`
- Database connection errors: Verify your PostgreSQL credentials and that the database is running
- MCP server issues: Ensure required packages are installed (`uvx mcp-server-fetch` should work)

## License

This project is licensed under the MIT License.
```
