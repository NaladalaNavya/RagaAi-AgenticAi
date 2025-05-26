from medical_history import retrieve_medical_history


def main():
    example_patient_id = 21  # Replace with valid patient_id from your DB
    result = retrieve_medical_history(example_patient_id)
    print(result)


if __name__ == "__main__":
    main()
