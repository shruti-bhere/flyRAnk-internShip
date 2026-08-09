from typing import Literal
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.researcher import research_node
from app.agents.writer import writer_node
from app.agents.reviewer import reviewer_node

def should_continue(state: AgentState) -> Literal["writer", "__end__"]:
    if state["review_status"] == "APPROVED":
        return END
    return "writer"

workflow = StateGraph(AgentState)

workflow.add_node("researcher", research_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "writer": "writer",
        END: END
    }
)

app_graph = workflow.compile()