# MCP Power Agent

https://github.com/prajwalghotkar/Agentic-AI-

----


https://github.com/user-attachments/assets/51472f06-61a5-45f9-b968-66ac5276e8d0


-----




https://github.com/user-attachments/assets/bfac57ee-3ddf-4839-84ed-6809ae88a009






----

## Demo

The demo video shows only a few example questions. GitHub does not allow large
video files to be embedded directly in a README, so I kept the video short.

The agent can handle many more questions in a single session. Below is a list
of questions you can try yourself. In my testing, the agent answered them
quickly, and it remembers earlier answers during the conversation.

Response speed depends on your model, your internet connection and which
tools the question needs.

----

## Example Questions

### Calculator
- What is 18% of 2450 plus 300?
- If I invest 50,000 at 7% yearly for 10 years, what is the final amount?
- Convert 72 km/h to meters per second.
- What is the square root of 1764 multiplied by 15?
- Split a bill of 4,860 between 6 people with a 5% tip.

### Date and Time
- What time is it in Tokyo right now?
- What is the time difference between Pune and New York?
- If a meeting is at 3 PM in London, what time is it in India?
- What time is it in Dubai, and how many hours are left until midnight there?

### Web Fetch
- Fetch https://example.com and summarize it in two lines.
- Read https://github.com/modelcontextprotocol/servers and list five servers.
- Fetch https://example.com and count the words in your summary.

### Weather (needs the optional weather server)
- What is the weather in Pune right now?
- Compare the weather in Mumbai and Delhi. Which one is hotter?
- What is the temperature in London in Fahrenheit?

### Multi-Tool Questions
- What is the weather in Pune? Convert the temperature to Fahrenheit.
- What time is it in Sydney, and what is 9 hours added to that time?
- Fetch https://example.com, count the words, and multiply the count by 12.

### Memory Test (ask one after another)
1. What is 245 times 12?
2. Now divide that by 4.
3. Add 100 to the result.

### Error Handling
- What is the weather in a made-up city like Zzxqland?
- Fetch https://thisdoesnotexist12345.com

-----














----

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

