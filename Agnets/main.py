from langgraph.graph import StateGraph, END
from schema import PatientState

# Import agents
from collect_info import agent_collect_info
from map_schema import agent_map_schema
from insert_db import agent_insert_db
from booking import agent_booking

# Build LangGraph
graph = StateGraph(PatientState)
graph.add_node("CollectInfo", agent_collect_info)
graph.add_node("MapSchema", agent_map_schema)
graph.add_node("InsertDB", agent_insert_db)
graph.add_node("Booking", agent_booking)

graph.set_entry_point("CollectInfo")
graph.add_edge("InsertDB", "MapSchema")
graph.add_edge("MapSchema", "InsertDB")
graph.add_edge("InsertDB", "Booking")
graph.add_edge("Booking", END)

app = graph.compile()

if __name__ == "__main__":
    state = PatientState(
        patient_data=None,
        summary=None,
        followup_notes=None,
        recommended_specialist=None,
        specialist_rationale=None,
        mapped_json=None,
        db_inserted=False,
        booking_done=False,
        appointment_details=None,
    )
    print("🚦 Starting patient workflow...")
    result = app.invoke(state)
    print("🏁 Workflow complete.")
    print("Booking done:", result["booking_done"])
    print("Appointment Details:", result.get("appointment_details"))
