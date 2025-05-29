import json
from google.generativeai import GenerativeModel
from schema import get_db_schema_text

def build_prompt(raw_data):
    schema = get_db_schema_text()
    return f"""
You are an expert medical data mapper.

Given this database schema:

{schema}

And the following patient intake JSON:

{json.dumps(raw_data, indent=2)}

Map the data to this format, following valid table-column mappings only:

[
  {{
    "table": "patients",
    "columns": {{
      "full_name": "...",
      "age": ...,
      ...
    }}
  }},
  {{
    "table": "symptoms",
    "records": [
      {{
        "symptom_description": "...",
        "severity": "...",
        ...
      }},
      ...
    ]
  }}
]

Skip unrelated or unknown fields. Output valid JSON only.
"""

def get_mapped_output(raw_data):
    prompt = build_prompt(raw_data)
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    content = response.text.strip()

    # Clean markdown code block if present
    if content.startswith("```"):
        parts = content.split("```")
        if len(parts) > 2:
            content = parts[1].strip()
            if content.startswith("json"):
                content = content[len("json"):].strip()
        else:
            content = parts[1].strip()
    return content
