import os
from pprint import pprint
from dotenv import load_dotenv
# Define a state type for the application
# Note: you may also use pydantic
from typing_extensions import TypedDict
from IPython.display import display, Markdown, Image
from langgraph.graph import StateGraph, START, END
import random
from typing import Literal
from langchain_groq import ChatGroq


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

    llm = ChatGroq(model = "llama-3.1-8b-instant", temperature=0.9)

    # Gives incorrect answer for some reason!!! 
    print("Answer to 523*780236 without tool:")
    print(llm.invoke("What is 523*780236?").content)

    tools = [multiply]

    print("Answer to 523*780236 with tool:")
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke("What is 523*780236?")
    pprint(response.__dict__)


    





if __name__ == "__main__":
    main()