import requests
from pprint import pformat
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from database import get_data
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Load personalized data
converted_string = get_data()

# -------------------- Weather & News Tools --------------------

def fetch_weather(city: str, api_key: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."
        else:
            return f"Error: {data.get('message', 'Failed to fetch weather')}"
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_news(topic: str, api_key: str) -> str:
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            articles = data.get('articles', [])
            if not articles:
                return f"No news found for {topic}."
            headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5])]
            return f"Top news for '{topic}':\n" + "\n".join(headlines)
        else:
            return f"Error: {data.get('message', 'Failed to fetch news')}"
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------- Gait and Activity Tools --------------------


def fetch_gait_posture_data(api_base: str = "http://localhost:8002") -> str:
    """
    Fetches gait posture data blocks from /gait_data_ endpoint.
    Each block should include:
    Start Time, End Time, Gait Speed, Step Length, Step Width, Cadence (Steps/min)
    """
    try:
        response = requests.get(f"{api_base}/gait_data")
        if response.status_code == 200:
            data = response.json()
            if not data:
                return "No gait posture data available."

            formatted = "\n".join(
                [
                    f"{i+1}. ⏱ {block.get('Start Time', 'N/A')} → {block.get('End Time', 'N/A')}\n"
                    f"   ➤ Gait Speed: {block.get('Gait Speed', 'N/A')}\n"
                    f"   ➤ Step Length: {block.get('Step Length', 'N/A')}\n"
                    f"   ➤ Step Width: {block.get('Step Width', 'N/A')}\n"
                    f"   ➤ Cadence: {block.get('Cadence (Steps/min)', 'N/A')} Steps/min"
                    for i, block in enumerate(data)
                ]
            )
            return f"📉 Gait Posture Data (Time Blocks):\n{formatted}"
        return "⚠ Failed to fetch gait posture data."
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"



def fetch_activity_data(api_base: str = "http://localhost:8002") -> str:
    try:
        response = requests.get(f"{api_base}/activities/all")
        if response.status_code == 200:
            data = response.json()
            if not data:
                return "No activity data available."
            formatted = "\n".join(
                [f"{i+1}. {block['Activity']} in {block['Place']} "
                 f"(Start: {block['Start_Time']} → End: {block['End_Time']})"
                 for i, block in enumerate(data)]
            )
            return f"🏃 Daily Life Activity Blocks:\n{formatted}"
        return "⚠ Failed to fetch activity data."
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

def fetch_last_activity_data(api_base: str = "http://localhost:8002") -> str:
    try:
        response = requests.get(f"{api_base}/activities/all")
        if response.status_code == 200:
            data = response.json()
            if not data:
                return "No activity data available."
            last = data[-1]
            return f"🕘 Your last activity was '{last['Activity']}' in {last['Place']} from {last['Start_Time']} to {last['End_Time']}."
        return "⚠ Failed to fetch activity data."
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# -------------------- Tools Binding --------------------

class EmptyInput(BaseModel):
    dummy: str = ""

weather_api_key = os.getenv("WEATHER_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
     # Replace with your NewsAPI key

# Tool Functions
def weather_tool_func(city: str) -> str:
    return fetch_weather(city, api_key=weather_api_key)

def news_tool_func(topic: str) -> str:
    return fetch_news(topic, api_key=news_api_key)

def gait_tool_func(dummy: str = "") -> str:
    print("[Tool HIT] Gait posture tool invoked.")
    return fetch_gait_posture_data()

def activity_tool_func(dummy: str = "") -> str:
    print("[Tool HIT] Activity data tool invoked.")
    return fetch_activity_data()

# def last_activity_tool_func(dummy: str = "") -> str:
#     print("[Tool HIT] Last activity tool invoked.")
#     return fetch_last_activity_data()

def answer_based_on_userdata(query: str) -> str:
    return converted_string

# Define Tools
weather_tool = Tool.from_function(
    func=weather_tool_func,
    name="fetch_weather",
    description="Fetches current weather for a city. Input: city name."
)

news_tool = Tool.from_function(
    func=news_tool_func,
    name="fetch_news",
    description="Fetches top news headlines for a topic. Input: topic name."
)

gait_posture_tool = Tool(
    name="fetch_gait_posture_data",
    func=gait_tool_func,
    description="Fetches overall gait posture data for user.",
    args_schema=EmptyInput
)

daily_activity_tool = Tool(
    name="fetch_activity_data",
    func=activity_tool_func,
    description="Fetches today's daily activity log. Have to share activities when ever asking for activity query.",
    args_schema=EmptyInput
)

# last_activity_tool = Tool(
#     name="fetch_last_activity",
#     func=last_activity_tool_func,
#     description="Fetches user's most recent activity today.",
#     args_schema=EmptyInput
# )

knowledge_tool = Tool(
    name="personalized_user_data_QA",
    func=answer_based_on_userdata,
    description="Use this tool to answer any question about user's personal profile and preferences."
)

# toolbox = [weather_tool, news_tool, knowledge_tool, daily_activity_tool, gait_posture_tool, last_activity_tool]
toolbox = [weather_tool, news_tool, knowledge_tool, daily_activity_tool, gait_posture_tool]

# -------------------- LLM and LangGraph Setup --------------------

openai_api_key = os.getenv("OPENAI_API_KEY")
simple_llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
llm_with_tools = simple_llm.bind_tools(toolbox)

assistant_system_message = SystemMessage(content="""
Only give answeres in 1-2 line not more long than that.
You are a healthcare conversational assistant designed to provide users with quick, relevant, and personalized responses.
You can fetch weather updates, news, activity logs, gait posture data, and provide personalized responses based on stored user data.
Use tools where necessary. Be concise, contextual, and helpful.
""")

def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([assistant_system_message] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(toolbox))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
react_graph_with_memory = builder.compile(checkpointer=memory)

# -------------------- Chatbot Function --------------------

def chatbot_with_memory(user_request: str, thread_id="1", verbose=False):
    config = {"configurable": {"thread_id": thread_id}}
    messages = react_graph_with_memory.invoke({"messages": [HumanMessage(content=user_request)]}, config)

    # Extract the last message
    final_message = messages['messages'][-1]

    # if verbose:
    #     for message in messages['messages']:
    #         message.pretty_print()
    # else:
    #     final_message.pretty_print()

    return  messages['messages'][-1].content 

# -------------------- CLI --------------------
chatbot_with_memory("Return all the user info")
# if __name__ == "__main__":
#     print("Healthcare Assistant Ready. Type 'exit' to quit.")
#     while True:
#         user_query = input("\nAsk your question: ")
#         if user_query.lower() == "exit":
#             print("Goodbye!")
#             break
#         response = chatbot_with_memory(user_query, verbose=False)
#         print("Response:", response)
