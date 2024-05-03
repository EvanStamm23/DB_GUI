import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

def get_insurance_data():
    st.write("Please enter insurance information, ensure patient ID is correctly entered")
    with st.form(key='insurance_form'):
        patient = st.text_input("*Patient ID for whom is insured:")
        provider_name = st.text_input("*Provider Name: ")
        coverage_plan = st.text_input("Coverage Plan: ")
        expiration_date = st.date_input("Expiration Date: ", value=None)
        submit = st.form_submit_button(label="Submit Insurance Information")
    if submit == True and (patient is '' or provider_name is ''):
        st.error("Please enter the patient's ID and the provider name")
    elif submit == True:
        st.success("Patient data has been successfully entered")
        add_insurance(patient, provider_name, coverage_plan, expiration_date)

def add_insurance(p_id, provider, coverage, expiration):
    cur.execute("INSERT INTO insurance VALUES (?,?,?,?)", (p_id, provider, coverage, expiration))

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

get_insurance_data()

con.commit()
con.close()