import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

def get_medication_data():
    st.write("Please Enter Medication Information")
    with st.form(key='medication_form'):
        prescription = st.text_input("*ID of relevant prescription")
        name = st.text_input("*Medication Name: ")
        cost = st.text_input("Cost: ")
        submit = st.form_submit_button(label="Add New Medication")
    if submit == True and (prescription is '' or name is ''):
        st.error("Please enter the prescription ID and medication name")
    elif submit == True:
        st.success("New medication has been successfully added")
        #call function to input data into database
        add_medication(prescription, name, cost)

def add_medication(presc_id, name, cost):
    cur.execute("INSERT INTO medication VALUES (?,?,?)", (presc_id, name, cost))

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

get_medication_data()

con.commit()
con.close()