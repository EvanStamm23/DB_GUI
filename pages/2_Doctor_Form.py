import streamlit as st
import sqlite3

st.set_page_config(page_icon=":hospital:")

def get_doctor_data():
    st.write("Please Enter New Doctor Information")
    with st.form(key='doctor_form'):
        name = st.text_input("*Doctor's Name: ")
        gender = st.text_input("Gender (M/F): ")
        primary_role =  st.text_input("Primary Role: ")
        submit = st.form_submit_button(label="Submit Doctor Information")
    if submit == True and name is '':
        st.error("Please enter the doctor's name")
    elif submit == True:
        st.success("Doctor data has been successfully entered")
        add_doctor(name, gender, primary_role)

def add_doctor(name, gender, role):
    cur.execute("INSERT INTO doctor VALUES (NULL,?,?,?)", (name, gender, role))

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

get_doctor_data()

con.commit()
con.close()