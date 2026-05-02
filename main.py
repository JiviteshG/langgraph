import os
from dotenv import load_dotenv
# Define a state type for the application
# Note: you may also use pydantic
from typing_extensions import TypedDict
from IPython.display import display, Markdown, Image
from langgraph.graph import StateGraph, START, END


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
    print(new_state)
    return {"my_state": new_state}

def node_3(state: State):
    print("node_3")
    print(state)
    new_state = state["my_state"] + "Italy."
    return {"my_state": new_state}

def main():
    load_dotenv()
    print("Welcome to LangGraph!")
    # create a graph
    
    # initialize state
    builder = StateGraph(State)

    # add nodes
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    # builder.add_node("node_3", node_3)

    # add edges
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    # builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    # builder.add_edge("node_3", END)

    graph = builder.compile()

    # Show the diagram (runs in Jupyter notebook)
    # display(Image(graph.get_graph().draw_mermaid_png()))

    # Save the diagram as a PNG file
    graph_png = graph.get_graph().draw_mermaid_png()
    with open("images\\graph_diagram.png", "wb") as f:
        f.write(graph_png)

    print("Diagram saved as graph_diagram.png - check your file explorer!")

    graph.invoke({"my_state": "Hello! I am Jivitesh. "})

if __name__ == "__main__":
    main()