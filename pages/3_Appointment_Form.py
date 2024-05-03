import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

def get_appointment_data():
    st.write("Enter Appointment Information")
    with st.form(key='appointment_form'):
        patient_id = st.text_input("*Enter the ID of the involved patient: ")
        doctor_id = st.text_input("*Enter the ID of the involved doctor: ")
        time = st.text_input("Enter the time of the appointment: ")
        date = st.date_input("Enter the date of the appointment: ", value=None)
        reason = st.text_area("Enter the reason for the appointment", max_chars=300)
        submit = st.form_submit_button(label="Create new appointment")
    if submit == True and (patient_id is '' or doctor_id is ''):
        st.error("Please enter the patient's ID and the doctor's ID")
    elif submit == True:
        st.success("New appointment created.")
        add_appointment(patient_id, doctor_id, time, date, reason)

def add_appointment(p_id, d_id, time, date, reason):
    cur.execute("INSERT INTO appointment VALUES (NULL,?,?,?,?,?)", (p_id, d_id, time, date, reason))

get_appointment_data()

con.commit()
con.close()