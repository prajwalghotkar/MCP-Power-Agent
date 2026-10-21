# MCP Power Agent

----






https://github.com/user-attachments/assets/08ce646e-7a6d-4d6b-95eb-74903bd6c017














A LangGraph agent that uses ready-made MCP servers as tools and Grok (xAI) as the brain.

Tools included: calculator, date/time, web page fetch, and optional weather.

## How it works

You type a question. The model decides whether to call a tool. LangGraph runs the tool through MCP, sends the result back to the model, and the model writes the final answer. The agent also remembers the conversation.

The agent starts each MCP server itself, so you do not need extra terminals.

## Setup (VS Code)

1. Install Python 3.10+ and open this folder in VS Code.
2. Open a terminal (Ctrl+`) and create a virtual environment:

       python -m venv .venv
       .venv\Scripts\activate

3. Install packages:

       pip install -r requirements.txt

4. Copy `.env.example` to `.env` and put in your key:

       XAI_API_KEY=xai-...

5. In VS Code press Ctrl+Shift+P, choose "Python: Select Interpreter", pick `.venv`.
6. Run:

       python agent.py

## Try these

- What is 18% of 2450 plus 300?
- What time is it in Tokyo?
- Fetch https://example.com and summarize it.
- What is the weather in Pune? (needs weather setup)

## Optional: weather server

1. Install Go from https://go.dev/dl/
2. Build it:

       git clone https://github.com/mschneider82/mcp-openweather.git
       cd mcp-openweather
       go build -o mcp-weather.exe

3. Get a free key at https://openweathermap.org/api (can take a few hours to activate).
4. In `.env` set `OWM_API_KEY` and `WEATHER_MCP_PATH` to the full path of `mcp-weather.exe`.

## Add more MCP servers

Add an entry in `server_configs()` in `agent.py`. Public list: https://github.com/modelcontextprotocol/servers

