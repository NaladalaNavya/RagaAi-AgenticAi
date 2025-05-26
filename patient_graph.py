from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from agents import (
    collect_patient_input,
    format_and_store_data,
    retrieve_history,
    recommend_and_book
)

from typing import TypedDict, Optional, Dict, Any

# Define shared state for graph
class PatientState(TypedDict):
    input_data: Optional[str]
    structured_data: Optional[dict]
    patient_id: Optional[int]
    medical_history: Optional[dict]
    appointment_confirmation: Optional[str]

# Define nodes (LLMs or tools)
graph = StateGraph(PatientState)

graph.add_node("InputCollector", collect_patient_input)
graph.add_node("FormatterAndStorage", format_and_store_data)
graph.add_node("Retriever", retrieve_history)
graph.add_node("Router", recommend_and_book)

# Edges
graph.set_entry_point("InputCollector")
graph.add_edge("InputCollector", "FormatterAndStorage")
graph.add_edge("FormatterAndStorage", "Retriever")
graph.add_edge("Retriever", "Router")
graph.add_edge("Router", END)

app = graph.compile()
