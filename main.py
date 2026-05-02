import os
from pprint import pprint
from dotenv import load_dotenv
# Define a state type for the application
# Note: you may also use pydantic
from typing_extensions import TypedDict
from IPython.display import display, Markdown, Image
from langgraph.graph import StateGraph, START, END, MessagesState
import random
from typing import Literal
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition


# User defined state type for the graph which is a TypedDict with a single key "my_state" of type str. This will be the state that is passed between nodes in the graph.
class State(TypedDict):
    my_state: str



# nodes
# Nodes are essentially python functions
def node_1(state: State):
    print("node_1")
    print(state)
    new_state = state["my_state"] + "I want to travel to "
    return {"my_state": new_state}

def node_2(state: State):
    print("node_2")
    print(state)
    new_state = state["my_state"] + "Japan."
    return {"my_state": new_state}

def node_3(state: State):
    print("node_3")
    print(state)
    new_state = state["my_state"] + "Italy."
    return {"my_state": new_state}

def decide_node(state: State) -> Literal["node_2", "node_3"]:
    print("decide_node")
    print(state)
    return random.choice(["node_2", "node_3"])



# nodes for LanggGraph
def llm_node(state: MessagesState) -> MessagesState:
    print("\n" + "*" * 80)
    print("Inside llm_node")
    print(state)
    # MessagesState stores a list of messages
    response = llm_with_tools.invoke(state["messages"])
    
    print("Exiting llm_node")
    # Return a list to append the new message to the history
    return {"messages": [response]}

# Tool function
def multiply(a: int, b: int) -> int:
    # Important to have a docstring for tool functions, as it helps LLMs understand their purpose and how to use them effectively.
    """
    Multiplies two numbers.
    
    Args: 
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of the two numbers.
    """
    return a * b

load_dotenv()
llm = ChatGroq(model = "llama-3.1-8b-instant", temperature=0.9)
tools = [multiply]
llm_with_tools = llm.bind_tools(tools)

def main():
    load_dotenv()
    print("Welcome to LangGraph!")
    # create a graph
    
    # initialize state
    builder = StateGraph(State)

    # add nodes
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    # add edges
    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", decide_node)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    graph = builder.compile()

    # Show the diagram (runs in Jupyter notebook)
    # display(Image(graph.get_graph().draw_mermaid_png()))

    # Save the diagram as a PNG file
    graph_png = graph.get_graph().draw_mermaid_png()
    with open("images\\graph_diagram_full.png", "wb") as f:
        f.write(graph_png)

    print("Diagram saved as graph_diagram_full.png - check your file explorer!")

    final_state = graph.invoke({"my_state": "Hello! I am Jivitesh. "})

    # Print the final state after invoking the graph
    print("--- Final Result ---")
    print(final_state)

    

    # Gives incorrect answer for some reason!!! 
    print("Answer to 523*780236 without tool:")
    print(llm.invoke("What is 523*780236?").content)

    print("Answer to 523*780236 with tool:")
    
    response = llm_with_tools.invoke("What is 523*780236?")
    pprint(response.__dict__)

    llm_node({"messages": [{"role": "user", "content": "What is 523*780236?"}]})

    builder = StateGraph(MessagesState)
    builder.add_node("llm_node", llm_node)
    builder.add_edge(START, "llm_node")
    builder.add_edge("llm_node", END)
    
    graph = builder.compile()

    # Mermaid diagram for the graph
    graph_png = graph.get_graph().draw_mermaid_png()
    with open("images\\graph_diagram_llm.png", "wb") as f:
        f.write(graph_png)

    inputs = {"messages": 
              [
                  {
                      "role": "system", "content": "You are Sherlock Holmes. Always answer sarcastically."
                    },
                  {
                      "role": "user", "content": "How do you solve a mystery?"
                    }   
            ]}

    final_state = graph.invoke(inputs)

    print("Final state from graph with llm_node:")
    pprint(final_state)

    for message in final_state["messages"]:
        print(message.pretty_print())

    # Tooll call with LangGraph
    builder = StateGraph(MessagesState)
    
    builder.add_node("llm_node", llm_node)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "llm_node")
    builder.add_conditional_edges("llm_node", tools_condition)

    builder.add_edge("tools", END)
    
    graph = builder.compile()

    # Mermaid diagram for the graph
    graph_png = graph.get_graph().draw_mermaid_png()
    with open("images\\graph_diagram_llm_tools.png", "wb") as f:
        f.write(graph_png)

    





if __name__ == "__main__":
    main()