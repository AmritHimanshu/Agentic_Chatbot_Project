# Agentic AI Chatbot

An **Agentic AI Chatbot** built while learning and exploring **AI Agents, LangChain, FastAPI, Streamlit, and tool-augmented LLM applications**.

The application allows users to interact with an AI agent, customize its behavior using a system prompt, select an LLM, and optionally give the agent access to **web search** so it can retrieve up-to-date information.

**Live Demo:** https://agentic-chatbot-project.streamlit.app/

---

## Features

- AI-powered conversational agent
- Customizable system prompt
- LLM integration through Groq
- Optional web-search capability using Tavily
- FastAPI backend for agent execution
- Streamlit frontend for the user interface
- Frontend-backend separation
- Environment/secrets-based API key configuration
- Deployed application

---

## Architecture

The project follows a simple frontend-backend-agent architecture:

```text
                         ┌──────────────────────┐
                         │      Streamlit       │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP POST /chat
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     AI Agent         │
                         │      LangChain       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         ▼                      ▼
                 ┌──────────────┐       ┌──────────────┐
                 │  Groq LLM    │       │ Tavily Search│
                 │              │       │   (Optional) │
                 └──────────────┘       └──────────────┘
```

### Request Flow

```text
User
 │
 ▼
Streamlit UI
 │
 │ User query + system prompt
 │ Model + provider + search setting
 ▼
FastAPI /chat endpoint
 │
 ▼
LangChain Agent
 │
 ├──────────────► Groq LLM
 │
 └──────────────► Tavily Web Search
                    (if enabled)
 │
 ▼
Agent Response
 │
 ▼
Streamlit UI
```

---

## How the AI Agent Works

The core agent is created dynamically based on the configuration received from the frontend.

The application:

1. Receives the user's query.
2. Receives the custom system prompt.
3. Initializes the selected LLM.
4. Optionally adds Tavily web search as a tool.
5. Creates a LangChain agent.
6. Sends the user's query to the agent.
7. The agent decides how to respond and whether to use the available tool.
8. The final response is returned to the frontend.

The agent uses LangChain's `create_agent()` abstraction to combine the model, tools, and system prompt.

```python
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)
```

Web search is optional:

```python
tools = [TavilySearch(max_results=2)] if allow_search else []
```

This means the agent can operate as a normal LLM-powered chatbot or as a **tool-augmented agent** with web-search capabilities.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🦜 LangChain | AI agent framework |
| ⚡ FastAPI | Backend API |
| 🎨 Streamlit | Frontend/UI |
| 🧠 Groq | LLM provider |
| 🔎 Tavily | Web-search tool |
| 🔐 python-dotenv | Environment variable management |
| 🚀 Uvicorn | ASGI server |

---

## Project Structure

```text
agentic-chatbot-project/
│
├── Backend
├      ├── ai_agent.py
├      ├── backend.py
├── frontend.py
│
├── requirements.txt
├── .env
├── .gitignore
│
└── README.md
```

### `frontend.py`

Contains the Streamlit user interface.

The frontend allows users to:

- Define the agent's system prompt
- Select the model provider
- Select the available model
- Enable/disable web search
- Enter their query
- Display the agent's response

The frontend sends the configuration and query to the FastAPI backend through an HTTP request.

---

### `backend.py`

Contains the FastAPI application.

The main API endpoint is:

```text
POST /chat
```

It receives:

```json
{
  "model_name": "qwen/qwen3.6-27b",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful AI assistant.",
  "messages": "What is artificial intelligence?",
  "allow_search": false
}
```

The backend then passes these parameters to the AI agent and returns the generated response.

---

### `ai_agent.py`

Contains the core agent logic.

Responsibilities include:

- Initializing the LLM
- Configuring Tavily search when enabled
- Creating the LangChain agent
- Passing the user query to the agent
- Returning the final agent response

---

## Why Use an AI Agent Instead of a Simple LLM Call?

A traditional LLM application might simply follow:

```text
User → LLM → Response
```

This project introduces a tool-using agent:

```text
User
  ↓
AI Agent
  ↓
 ┌───────────────┐
 │ Decide what   │
 │ action is     │
 │ needed        │
 └───────┬───────┘
         │
    ┌────┴────┐
    ▼         ▼
   LLM      Web Search
    │         │
    └────┬────┘
         ▼
      Response
```

When web search is enabled, the agent has access to an external tool and can use it when appropriate.

This makes the project a practical introduction to **tool-augmented AI agents**.

---

## Web Search Capability

The application integrates **Tavily Search** as an optional tool.

When the user enables:

```text
☑ Allow Web Search
```

the agent receives Tavily as an available tool.

When disabled, the agent operates without the search tool.

This demonstrates an important concept in agentic AI:

> **An LLM can be given access to external tools to extend its capabilities beyond its internal knowledge.**

---

## Configuration

The application uses environment variables/secrets for sensitive configuration.

Create a `.env` file for local development:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

For the Streamlit deployment, configure the required values using **Streamlit Secrets**.

The frontend expects the backend URL through:

```text
BACKEND_API_URL
```

For example:

```toml
BACKEND_API_URL = "https://your-backend-url.com"
```

> Never commit your `.env` file or API keys to GitHub.

---

## Run Locally

This project uses **uv** for Python environment and dependency management.

### 1. Clone the repository

```bash
git clone https://github.com/AmritHimanshu/Agentic_Chatbot_Project.git

cd <your-repository>
```

### 2. Install uv

If you don't already have `uv` installed, follow the official installation instructions.

### 3. Create the virtual environment

```bash
uv venv
```

Activate the environment on Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

If the repository contains a `pyproject.toml`:

```bash
uv sync
```

This will create/synchronize the project's virtual environment and install the required dependencies.

Alternatively, if you are using a `requirements.txt` file:

```bash
uv pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> Never commit your `.env` file or API keys to GitHub.

### 6. Start the FastAPI backend

```bash
uv run uvicorn backend:app --reload --port 5000
```

The backend will be available at:

```text
http://127.0.0.1:5000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:5000/docs
```

### 7. Configure the Streamlit frontend

For local development, configure the backend URL used by the Streamlit frontend.

If your application uses Streamlit secrets, create:

```text
.streamlit/
└── secrets.toml
```

with:

```toml
BACKEND_API_URL = "http://127.0.0.1:5000"
```

### 8. Start the Streamlit frontend

```bash
uv run streamlit run frontend.py
```

The application will then open in your browser.

---

## API

### `GET /`

Returns a simple welcome message.

### `POST /chat`

Main endpoint used to communicate with the AI agent.

#### Request

```json
{
  "model_name": "qwen/qwen3.6-27b",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful AI assistant.",
  "messages": "Explain RAG in simple terms.",
  "allow_search": false
}
```

#### Response

The endpoint returns the final response generated by the AI agent.

---

## Example Use Cases

### General AI Assistant

```text
System Prompt:
You are a helpful and concise AI assistant.

Query:
Explain LangGraph in simple terms.
```

### Programming Assistant

```text
System Prompt:
You are an experienced Python developer.
Provide simple explanations and production-quality code.

Query:
Explain Python decorators with an example.
```

### Research Assistant

Enable:

```text
☑ Allow Web Search
```

Then ask:

```text
What are the latest developments in AI agents?
```

The agent can use the Tavily search tool to retrieve web information.

---

## Learning Objectives

This project was built as part of my learning journey into **Generative AI and AI Agents**.

Through this project, I explored:

- Understanding AI agents
- LangChain agent creation
- LLM integration
- Tool calling
- Web-search tools
- System prompts
- FastAPI-based AI backends
- Streamlit-based AI interfaces
- Frontend-backend communication
- Environment/secrets management
- Deploying AI applications

---

## Future Improvements

Some possible improvements for the project:

- [ ] Add conversation memory
- [ ] Support multiple LLM providers
- [ ] Add more tools beyond web search
- [ ] Add streaming responses
- [ ] Add chat history
- [ ] Add structured tool calling
- [ ] Add authentication
- [ ] Improve error handling
- [ ] Add logging and monitoring
- [ ] Add LangSmith tracing
- [ ] Add more agent capabilities
- [ ] Improve UI/UX
- [ ] Add automated tests

---

## Live Demo

Try the deployed application:

### https://agentic-chatbot-project.streamlit.app/

---

## What I Learned

The biggest takeaway from this project was understanding that an **AI Agent is more than just an LLM call**.

Instead of building:

```text
Prompt → LLM → Response
```

we can build systems where:

```text
User
  ↓
Agent
  ↓
Reason about the task
  ↓
Use available tools when required
  ↓
Generate final response
```

This project was an important step in my journey from traditional full-stack development toward **Generative AI and AI Engineering**.

---

## Author

**Himanshu Kumar Amrit**

Full Stack Developer → Generative AI / AI Engineer

Interested in building practical applications using:

- Generative AI
- AI Agents
- RAG
- LangChain
- LangGraph
- FastAPI
- React / Next.js
- Python

---

## Support

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.

Feel free to explore the code, experiment with the agent, and build upon it!
