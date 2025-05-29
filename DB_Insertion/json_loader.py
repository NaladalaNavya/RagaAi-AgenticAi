import json

def load_mapped_output(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
