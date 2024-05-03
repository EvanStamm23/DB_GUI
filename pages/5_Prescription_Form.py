import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

def get_prescription_data():
    st.write("Please Enter Prescription Information")
    with st.form(key='prescription_form'):
        patient = st.text_input("*ID of prescribed patient")
        refill = st.text_input("Refill Frequency: ")
        dose = st.text_input("Dosage: ")
        submit = st.form_submit_button(label="Create New Prescription")
    if submit == True and patient is '':
        st.error("Please enter the patient's ID")
    elif submit == True:
        st.success("New prescription has been successfully created")
        add_prescription(patient, refill, dose)

def add_prescription(p_id, refill, dose):
    cur.execute("INSERT INTO prescription VALUES (NULL,?,?,?)", (p_id, refill, dose))

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

get_prescription_data()

con.commit()
con.close()