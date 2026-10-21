"""
MCP Power Agent
LangGraph + ready-made MCP servers + Grok (xAI) or Groq via an OpenAI-compatible API.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools: weather, calculator, "
    "date/time and web page fetching. Use a tool whenever it gives a more "
    "accurate answer than guessing. Never do arithmetic in your head: use the "
    "calculator. If a tool fails, say so clearly and suggest what to try next."
)

# Provider presets. Pick automatically from the key prefix, or set LLM_PROVIDER.
PROVIDERS = {
    "xai": {"base_url": "https://api.x.ai/v1", "model": "grok-4.5"},
    "groq": {"base_url": "https://api.groq.com/openai/v1", "model": "openai/gpt-oss-120b"},
}


def build_llm() -> ChatOpenAI:
    key = os.getenv("LLM_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("No API key found. Set XAI_API_KEY (or GROQ_API_KEY) in .env")

    provider = os.getenv("LLM_PROVIDER") or ("groq" if key.startswith("gsk_") else "xai")
    preset = PROVIDERS[provider]

    return ChatOpenAI(
        api_key=key,
        base_url=os.getenv("LLM_BASE_URL", preset["base_url"]),
        model=os.getenv("LLM_MODEL", preset["model"]),
        temperature=0,
    )


def server_configs() -> dict:
    """Ready-made MCP servers. All run as local subprocesses (stdio)."""
    servers = {
        "calculator": {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["-m", "mcp_server_calculator"],
        },
        "time": {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["-m", "mcp_server_time"],
        },
        "fetch": {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["-m", "mcp_server_fetch"],
        },
    }

    # Weather is optional: needs the Go-built binary + OpenWeatherMap key.
    weather_path = os.getenv("WEATHER_MCP_PATH")
    owm_key = os.getenv("OWM_API_KEY")
    if weather_path and owm_key and os.path.exists(weather_path):
        servers["weather"] = {
            "transport": "stdio",
            "command": weather_path,
            "args": [],
            "env": {"OWM_API_KEY": owm_key},
        }
    else:
        print("[info] Weather server disabled (set WEATHER_MCP_PATH and OWM_API_KEY to enable).")

    return servers


async def load_tools() -> list:
    """Load tools server by server so one broken server doesn't kill the agent."""
    tools = []
    for name, cfg in server_configs().items():
        try:
            server_tools = await MultiServerMCPClient({name: cfg}).get_tools()
            tools.extend(server_tools)
            print(f"[ok]   {name}: {[t.name for t in server_tools]}")
        except Exception as exc:
            print(f"[skip] {name} failed to start: {exc}")
    if not tools:
        raise RuntimeError("No MCP tools loaded. Check your installs (see README).")
    return tools


def build_graph(llm: ChatOpenAI, tools: list):
    llm_with_tools = llm.bind_tools(tools)  # bind once, not on every call

    def call_model(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        return {"messages": [llm_with_tools.invoke(messages)]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")

    return builder.compile(checkpointer=MemorySaver())  # remembers the chat


async def main():
    llm = build_llm()
    tools = await load_tools()
    graph = build_graph(llm, tools)
    config = {"configurable": {"thread_id": "session-1"}}

    print("\nAgent ready. Type 'exit' to quit.")
    while True:
        question = input("\nYou → ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        try:
            result = await graph.ainvoke({"messages": [("user", question)]}, config)
            print("\nAgent →", result["messages"][-1].content)
        except Exception as exc:
            print(f"\n[error] {exc}")


if __name__ == "__main__":
    asyncio.run(main())
