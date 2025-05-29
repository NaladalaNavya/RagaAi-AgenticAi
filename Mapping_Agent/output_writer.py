import json

def save_output(content, output_file):
    try:
        parsed = json.loads(content)
        with open(output_file, "w") as f:
            json.dump(parsed, f, indent=2)
        print(f"✅ Mapped output saved to: {output_file}")
    except json.JSONDecodeError:
        print("❌ LLM response is not valid JSON. Here's the raw content:")
        print(content)
