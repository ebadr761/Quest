from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict


load_dotenv() # loads environment variables from a .env file

#load the LLM model
llm = init_chat_model("gemini-1.5-flash", model_provider="google_genai")

#set up the state graph
class State(TypedDict):
    messages: Annotated[list, add_messages] # messages will be of type list and will be annotated with add_messages to allow for message addition

#—————MAKING A SIMPLE NODE————————
graph_builder = StateGraph(State) # Create StateGraph with State class

def chatbot(state: State): #takes in a state and returns a modified state response
    return {"messages": [llm.invoke(state["messages"])]} # invokes the LLM with the messages in the state and returns a new state with the response

graph_builder.add_node("chatbot", chatbot) # adds the chatbot node to the graph
#—————————————————————————————————
graph_builder.add_edge(START, "chatbot") # adds an edge from the start node to the chatbot node
graph_builder.add_edge("chatbot", END) # adds an edge from the chatbot node to... now we have built a simple state graph with a single node that invokes the LLM.


graph = graph_builder.compile() # compiles the graph into a callable function

user_input = input("Enter your message: ")
state = graph.invoke({"messages": [{"role": "user", "content": user_input}]}) # invokes the graph with the user input as the initial state w/ role as user & content as user input

print(state["messages"][-1].content) # prints the last message in the state, which is the response from the LLM