import streamlit as st
from patient_graph import app, PatientState
import booking  # Import the whole module

import json
import os

st.set_page_config(page_title="Patient Workflow", layout="centered")
st.title("🏥 Patient Workflow Automation")

st.write(
    """
    Welcome! This app will guide you through a patient intake workflow, map the data to the database schema, insert it into the database, and book an appointment with a recommended specialist.
    """
)

def run_booking(result):
    # Write the result to the expected JSON file
    with open("final_patient_summary.json", "w") as f:
        json.dump(result, f)
    # Call the main booking logic
    booking.main()
    # Optionally, you can parse logs or return a simple status
    return "Booking attempted. Check database or logs for details."

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if st.button("Start Patient Intake Workflow"):
    initial_state = PatientState(
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
    with st.spinner("Running patient workflow..."):
        result = app.invoke(initial_state)
        # Run booking using the workflow result
        booking_status = run_booking(result)
        result["booking_status"] = booking_status
        st.session_state.workflow_result = result

if st.session_state.workflow_result:
    result = st.session_state.workflow_result
    st.success("Workflow complete!")
    st.write("### Full Result Dictionary:")
    st.json(result)
    st.write("### Booking Status:")
    st.write(result.get("booking_status"))
    st.write("### Patient Data:")
    st.json(result.get("patient_data"))
    st.write("### Summary:")
    st.write(result.get("summary"))
    st.write("### Followup Notes:")
    st.write(result.get("followup_notes"))
    st.write("### Recommended Specialist:")
    st.write(result.get("recommended_specialist"))
    st.write("### Specialist Rationale:")
    st.write(result.get("specialist_rationale"))
else:
    st.info("Click the button above to start the workflow.")