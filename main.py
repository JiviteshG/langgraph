import os
from dotenv import load_dotenv
# Define a state type for the application
# Note: you may also use pydantic
from typing_extensions import TypeDict
from IPython.display import display, Markdown 
from langgraph.graph import StateGraph, START, END


class State(TypeDict):
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

def main():
    

if __name__ == "__main__":
    main()