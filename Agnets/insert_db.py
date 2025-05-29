import json
from inserting_JSON_to_DB import insert_data_from_mapped_json

def agent_insert_db(state, config):
    insert_data_from_mapped_json("mapped_output.json")
    state["db_inserted"] = True

    with open("booking_input.json", "w") as f:
        json.dump({
            "patient_data": state["patient_data"],
            "recommended_specialist": state["recommended_specialist"]
        }, f, indent=2)

    return state
