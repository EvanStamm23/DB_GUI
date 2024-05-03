import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

def get_patient_data():
    st.write("Please enter patient data")
    with st.form(key='patient_form'):
        name = st.text_input("*Patient Name: ")
        email = st.text_input("*Patient Email: ")
        phone_num = st.text_input("Phone Number: ")
        address = st.text_input("Home Address: ")
        dob = st.date_input("Date of Birth: ", value=None)
        gender = st.text_input("Gender (M/F): ")
        doctor = st.text_input("Assigned Doctor ID: ")
        submit = st.form_submit_button(label="Submit Patient Information")
    if (submit == True and (name is '' or email is '')):
        st.error("Please enter patient name and email")
    elif submit == True:
        st.success("Patient data has been successfully entered")
        #call function to input data into database
        add_patient(name, email, phone_num, address, dob, gender, doctor)
        st.session_state.form_submitted = True
    if "form_submitted" in st.session_state:
        active = st.toggle("Add medical history for this patient?")
        if active: #and st.session_state.show_patient_history:
            get_patient_history(name, email)

def get_patient_history(name, email):
    st.write("Please enter patient history")
    with st.form(key="patient_history"):
        cur.execute("SELECT Patient_ID FROM patient WHERE Patient_Name=? AND Patient_Email=?", (name, email))
        p_id = cur.fetchone()
        diseases = st.text_area("Enter any relevant disease information: ")
        surgeries = st.text_area("Enter any past surgeries: ")
        disabilities = st.text_area("Enter any disabilities patient has: ")
        predispositions = st.text_area("Enter any known genetic family medical issues:")
        concerns = st.text_area("Enter any other concerns or repreated issues")
        submit = st.form_submit_button(label="Submit Patient History")
    if(submit):
        st.success("Patient history successfully entered")
        add_patient_history(p_id[0], diseases, surgeries, disabilities, predispositions, concerns)

def add_patient_history(id, disease, surgery, disability, predisposition, concern):
    cur.execute("INSERT INTO patient_history VALUES (NULL,?,?,?,?,?,?)", (id, disease, surgery, disability, predisposition, concern))

def add_patient(name, email, phone, address, dob, gender, doctor):
    cur.execute("INSERT INTO patient VALUES (NULL,?,?,?,?,?,?,?)", (name, email, phone, address, dob, gender, doctor))

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

get_patient_data()

con.commit()
con.close()