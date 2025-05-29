from config import connect_to_db
from insert_logic import insert_single_record, insert_multiple_records
from json_loader import load_mapped_output

def insert_data_from_mapped_json(file_path):
    data = load_mapped_output(file_path)
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        for item in data:
            table = item["table"]
            if "columns" in item:
                insert_single_record(cursor, table, item["columns"])
            elif "records" in item:
                insert_multiple_records(cursor, table, item["records"])
        conn.commit()
        print("✅ All data inserted into the database.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_data_from_mapped_json("mapped_output.json")
