import json
from mapping_collectedinfo_to_schema import get_mapped_output

def agent_map_schema(state, config):
    with open("patient_data.json", "r") as f:
        patient_data = json.load(f)

    mapped_json = get_mapped_output(patient_data)
    state["mapped_json"] = mapped_json

    with open("mapped_output.json", "w") as f:
        if isinstance(mapped_json, str):
            f.write(mapped_json)
        else:
            f.write(json.dumps(mapped_json, indent=2))

    return state
