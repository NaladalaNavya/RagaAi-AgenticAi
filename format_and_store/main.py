from format_store import format_and_store_data_from_file
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide the path to the JSON file.")
    else:
        file_path = sys.argv[1]
        result = format_and_store_data_from_file(file_path)
        print("📦 Final Result:", result)
