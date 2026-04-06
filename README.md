# bizverify-agents

BizVerify tool wrappers for LLM agent frameworks. Provides ready-to-use tools for [LangChain](https://python.langchain.com/) and [CrewAI](https://www.crewai.com/) that call the [BizVerify](https://bizverify.co) business verification API.

## Installation

```bash
# LangChain
pip install bizverify-agents[langchain]

# CrewAI
pip install bizverify-agents[crewai]

# Both
pip install bizverify-agents[langchain,crewai]
```

## Authentication

Set your API key as an environment variable:

```bash
export BIZVERIFY_API_KEY="bv_live_..."
```

Or pass it directly:

```python
tools = BizVerifyTools(api_key="bv_live_...")
```

Get an API key at [bizverify.co](https://bizverify.co) -- new accounts receive 50 free credits.

## Usage

### LangChain

```python
from bizverify_agents.langchain import BizVerifyTools

tools = BizVerifyTools().get_tools()

# Use with any LangChain agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
executor.invoke({"input": "Verify Acme Corp in Florida"})
```

### CrewAI

```python
from bizverify_agents.crewai import BizVerifyTools

tools = BizVerifyTools().get_tools()

# Use with any CrewAI agent
from crewai import Agent
agent = Agent(
    role="Business Analyst",
    tools=tools,
    goal="Verify business registrations",
)
```

## Available Tools

| Tool | Description | Credits |
|------|-------------|---------|
| `verify_business` | Verify a business entity against official government registries | 1-25 |
| `search_entities` | Search for business entities across jurisdictions | 2/jurisdiction |
| `check_job_status` | Poll an async verification job | Free |
| `get_entity` | Retrieve cached entity data by ID | Free |
| `get_entity_history` | Get historical verification snapshots | 1 |
| `get_account` | Returns account details and credit balance | Free |
| `get_config` | Returns supported jurisdictions, pricing, and features | Free |
| `list_jurisdictions` | Returns all jurisdictions with capabilities and status | Free |
| `purchase_credits` | Creates a Stripe checkout session for credit purchase | Free |

## Links

- [BizVerify Documentation](https://docs.bizverify.co)
- [AI Agents Guide](https://docs.bizverify.co/guides/ai-agents)
- [API Reference](https://api.bizverify.co/reference)
- [Python SDK](https://pypi.org/project/bizverify/)
