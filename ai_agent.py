import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

load_dotenv()

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)

    tools = [TavilySearch(max_results=2)] if allow_search else []

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )


    state = {"messages": [{"role": "user", "content": query}]}

    response = agent.invoke(state)

    # messages = response["messages"]
    # ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    # print(ai_messages)

    # print(response["messages"][-1].content)
    return response['messages'][-1].content