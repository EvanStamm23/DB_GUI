import streamlit as st
import sqlite3

st.set_page_config(page_title="Home Page", page_icon=":hospital:")

con = sqlite3.connect('healthcare.db')
cur = con.cursor()

def make_base_schema():
    cur.execute("""CREATE TABLE IF NOT EXISTS patient(
        Patient_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	    Patient_Name TEXT NOT NULL,
	    Patient_Email TEXT,
	    Patient_PhoneNum TEXT,
	    Home_Address TEXT,
	    Birth_Date TEXT,
	    Gender char,
	    Assigned_Doctor INTEGER,
	    FOREIGN KEY(Assigned_Doctor) REFERENCES doctor(Doctor_ID))""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctor(
	    Doctor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	    Doctor_Name TEXT NOT NULL,
	    Gender char,
	    Primary_Role TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS appointment(
	    Appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	    Patient_ID INT,
	    Doctor_ID INTEGER,
	    Appointment_Time TEXT,
	    Appointment_Date TEXT,
	    Reason TEXT,
	    FOREIGN KEY(Patient_ID) REFERENCES patient(Patient_ID),
	    FOREIGN KEY(Doctor_ID) REFERENCES doctor(Doctor_ID))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS prescription(
	    Prescription_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	    Patient_ID INTEGER,
	    Refill_Frequency TEXT,
	    Dose TEXT,
	    FOREIGN KEY(Patient_ID) REFERENCES patient(Patient_ID))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS insurance(
	    Patient_ID INTEGER,
		Provider_Name TEXT,
	    Coverage_Plan TEXT,
	    Expiration_Date TEXT,
	    PRIMARY KEY(Provider_Name, Coverage_Plan, Patient_ID),
	    FOREIGN KEY(Patient_ID) REFERENCES patient(Patient_ID))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS patient_history(
	    Record_ID INTEGER,
	    Patient_ID INTEGER,
	    Diseases TEXT,
	    Surgeries TEXT,
	    Disabilities TEXT,
	    Predispositions TEXT,
	    Repeated_Concerns TEXT,
	    PRIMARY KEY(Record_ID AUTOINCREMENT),
	    FOREIGN KEY(Patient_ID) REFERENCES patient(Patient_ID))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS medication(
	    Prescription_ID INTEGER,
	    Medication_Name TEXT,
	    Cost REAL,
	    PRIMARY KEY(Medication_Name, Prescription_ID),
	    FOREIGN KEY(Prescription_ID) REFERENCES prescription(Prescription_ID))""")
	
		##IF OUR DATABASE IS CURRENTLY EMPTY, POPULATE SOME DEFUALT VALUES TO SHOW FUNCTIONALITY
    cur.execute("SELECT * FROM patient LIMIT 1")
    if (not cur.fetchone()):
        insert_patient()
        insert_doctor()
        insert_appointments()
        insert_insurance()
        insert_prescriptions()
        insert_medications()
        insert_history()
	
def insert_patient():
	names = ["Albert", "Rachel", "Alex", "Sally", "Luke", "Olivia", "James", "Emma", "Daniel", "Sophia"]
	emails = ["abert@gmail.com", "rachel94@yahoo.com", "alex1247@hotmail.com", "s_sally@gmail.com", "lucas2m@gmail.com", "olive8439@yahoo.com", "jamesjones@gmail.com", "emmmmmma@outlook.com","dannyd@gmail.com", "sophia27@aol.com"]
	phone_nums = ["3148724318", "5763192431", "4862419247", "6368209943", "82730044342", "9138279938", "3145303939", "5734887606", "9087264488", "8059906651"]
	addresses = ["321 Maple Avenue", "456 Elm Street", "789 Oak Lane", "101 Pinecrest Drive", "234 Cedar Road", "567 Willow Lane", "890 Birch Street", "112 Sycamore Avenue", "345 Aspen Court", "678 Hawthorn Lane"]
	dobs = ["01/15/1975", "03/28/1980", "07/10/1985", "11/03/1990","04/22/1995","08/17/2000","12/05/2005","05/08/2010","09/20/2010","02/12/2012"]
	genders = ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F','M', 'F']
	doctors = ['2', '1', '3', '3', '1', '2', '1', '3', '2', '2']
	for i in range(10):
		cur.execute("INSERT INTO patient VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (names[i], emails[i], phone_nums[i], addresses[i], dobs[i], genders[i], doctors[i]))

def insert_history():
	p_ids = ["1", "2", "3", "4", "5"]
	diseases = ["Polio","Measles","Tuberculosis (TB)","Smallpox","Rickets"]
	surguries = ["Appendectomy","Cholecystectomy","Lumbar Discectomy", "Cataract Surgery", "Total Knee Arthroplasty"]
	disabilities = ["Parkinson's Disease", "Spinal Cord Injury", "Multiple Sclerosis (MS)", "Cerebral Palsy", "Muscular Dystrophy"]
	predispositions = ["Familial Hypercholesterolemia", "Cystic Fibrosis", "Sickle Cell Anemia", "Alzheimer's Disease","Type 1 Diabetes"]
	concerns = ["Back Pain","Headaches","Skin Rash","Fatigue","Allergies"]
	for i in range(5):
		cur.execute("INSERT INTO patient_history VALUES (NULL,?,?,?,?,?,?)", (p_ids[i], diseases[i], surguries[i], disabilities[i], predispositions[i], concerns[i]))

def insert_doctor():
	names = ["Dr. Samantha Lopez", "Dr. Christopher Nguyen", "Dr. Maya Patel"]
	genders = ['F', 'M', 'F']
	roles = ["Primary Care Physician","Emergency Medicine Specialist","Pediatrician"]
	for i in range(3):
		cur.execute("INSERT INTO doctor VALUES (NULL, ?, ?, ?)", (names[i], genders[i], roles[i]))

def insert_appointments():
	p_ids = ["3", "7", "2", "4", "8", "10"]
	d_ids = ["1", "3", "1", "1", "2", "1"]
	times = ["3:00 PM", "12:00PM", "1:30PM", "11:30AM", "12:30PM", "10:00AM"]
	dates = ["2024/05/20","2024/03/15","2024/09/28","2024/01/01","2024/12/31","2024/07/10"]
	reasons = ["Routine check-up to monitor overall health and well-being.","Addressing persistent cough and breathing difficulties.","Managing chronic hypertension condition","Consultation for prenatal care and monitoring during pregnancy.","Seeking advice for mental health concerns like anxiety or depression.","Follow-up appointment after a surgical procedure for wound care and recovery assessment."]
	for i in range(6):
		cur.execute("INSERT INTO appointment VALUES (NULL, ?,?,?,?,?)", (p_ids[i], d_ids[i], times[i], dates[i], reasons[i]))

def insert_insurance():
	p_ids = ["1", "2", "4", "7", "9"]
	provider_names = ["SafeGuard Health Assurance","EverCare Assurance Group","Unity Insurance Solutions","SecureHealth Coverage Providers","Harmony HealthGuard Corporation"]
	coverages = ["DentaCare Dental Coverage","VisionClear Vision Insurance","OrthoFlex Orthodontic Plan","RxRelief Prescription Coverage","DermAid Dermatology Insurance"]
	exp_dates = ["2026/08/15","2025/04/03","2027/11/22","2024/10/07","2026/01/20"]
	for i in range(5):
		cur.execute("INSERT INTO insurance VALUES (?,?,?,?)", (p_ids[i], provider_names[i], coverages[i], exp_dates[i]))

def insert_prescriptions():
	p_ids = ["8", "1", "2", "5", "6"]
	refills = ["Monthly", "Weekly", "Every Two Weeks", "Monthly", "Every Two Months"]
	doses = ["125mcg","250mg","50ml","75 units","200 mg"]
	for i in range(5):
		cur.execute("INSERT INTO prescription VALUES (NULL, ?,?,?)", (p_ids[i], refills[i], doses[i]))

def insert_medications():
	presc_ids = ["1", "2", "3", "4", "5", "1", "1", "2", "3"]
	names = ["Lunacor","Painolax","Tranquilityrex","Vitazyme","Energix", "Aspirin","Ibuprofen","Acetaminophen","Naproxen"]
	costs = ["$25", "$30", "$65", "$40", "$20", "$10", "$15", "$25", "$35"]
	for i in range(9):
		cur.execute("INSERT INTO medication VALUES (?,?,?)", (presc_ids[i], names[i], costs[i]))

def home_page():
	st.title("Healthcare Database Manager")
	search_option = st.selectbox(
		"What information would you like to search for?", 
		("Patient Information", "Doctor Information", "Appointments", "Prescriptions"),
		index=None,
		placeholder="Select Category...")
	st.write("Searching for:", search_option)
	view_all = st.checkbox("View All")

	if search_option=="Patient Information":
		search_name = st.text_input("Patient Name: ")
		search_email = st.text_input("Patient Email: ")
		search_patients(search_name, search_email)
		if view_all:
			view_all_patients()
	elif search_option=="Doctor Information":
		doc_id = st.text_input("Doctor ID: ")
		doc_name = st.text_input("Doctor Name: ")
		search_doctors(doc_id, doc_name)
		if view_all:
			view_all_doctors()
	elif search_option == "Appointments":
		appt_id = st.text_input("Appointment ID: ")
		search_appointments(appt_id)
		if view_all:
			view_all_appointments()
	elif search_option == "Prescriptions":
		presc_id = st.text_input("Prescription ID: ")
		search_prescriptions(presc_id)
		if view_all:
			view_all_prescriptions()

def view_all_patients():
	cur.execute("SELECT * FROM patient LIMIT 20")
	patients = cur.fetchall()
	st.dataframe(patients, column_config={"0" : "Patient ID", "1":"Name", "2":"Email","3":"Phone #","4":"Address","5":"Birth Date", "6":"Gender","7":"Assigned Doctor"})
	st.write("Note: Viewing first 20 entries")

def view_all_doctors():
	cur.execute("SELECT * FROM doctor LIMIT 20")
	doctors = cur.fetchall()
	st.dataframe(doctors, column_config={"0":"Doctor ID", "1":"Name", "2": "Gender", "3":"Role"})
	st.write("Note: Viewing first 20 entries")
     
def view_all_appointments():
	cur.execute("SELECT * FROM appointment LIMIT 20")
	appointments = cur.fetchall()	
	st.dataframe(appointments, column_config={"0":"Appointment ID", "1":"Patient ID", "2":"Doctor ID", "3":"Time", "4":"Date", "5":"Reason"})
	st.write("Note: Viewing first 20 entries")

def view_all_prescriptions():
	cur.execute("SELECT * FROM prescription LIMIT 20")
	prescriptions = cur.fetchall()
	st.dataframe(prescriptions, column_config={"0":"Prescription ID", "1":"Patient ID", "2":"Refill Frequency", "3" : "Dose"})
	st.write("Note: Viewing first 20 entries")

def search_patients(name, email):
	#Retrieve patient searched for based on which value is given
	if (email == '' or name == ''):
		cur.execute("SELECT * FROM patient WHERE Patient_Name=? OR Patient_Email=?", (name, email))
	else:
		cur.execute("SELECT * FROM patient WHERE Patient_Name=?	AND Patient_Email=?", (name, email))
	patients = cur.fetchall()
	#If a patient matches the search, display thier info, and ask if they would like to see patient history
	if(len(patients) > 0):
		st.dataframe(patients, column_config={"0" : "Patient ID", "1":"Name", "2":"Email","3":"Phone #","4":"Address","5":"Birth Date", "6":"Gender","7":"Assigned Doctor"})
		st.session_state.search_patient = True
		p_id = patients[0][0]
		col1, col2, col3, col4 = st.columns(4)
		if "search_patient" in st.session_state:
			history_active = col1.toggle("View patient history")
			insurance_active = col2.toggle("View patient insurance")
			edit = col3.toggle("Edit Patient")
			delete = col4.button("Delete Patient", type="primary")
			if edit:
				update_patient_form(p_id)
			if history_active:
				search_patient_history(p_id)
			if insurance_active:
				search_insurance(p_id)
			if delete:
				delete_patient(p_id)

#MAKE NEW FORM TO INPUT VALUES THAT USER WANTS TO UPDATE
#Note: ANY VALUES THAT AREN"T ENTERED WILL REMAIN THE SAME
def update_patient_form(id):
    st.write("Please enter patient data you wish to update")
    with st.form(key='update_patient'):
        name = st.text_input("*Patient Name: ")
        email = st.text_input("*Patient Email: ")
        phone_num = st.text_input("Phone Number: ")
        address = st.text_input("Home Address: ")
        dob = st.date_input("Date of Birth: ", value=None)
        gender = st.text_input("Gender (M/F): ")
        doctor = st.text_input("Assigned Doctor ID: ")
        submit = st.form_submit_button(label="Submit Patient Update")
    if submit == True:
        st.success("Patient data has been successfully updated")
		#this part is neccessary to process entered data, as defualt blank input is '', which sqlite doesn't recognize as the same as NULL or NONE
        input = [name, email, phone_num, address, dob, gender, doctor]
        for i, var in enumerate(input):
            if var == '':
                input[i] = None
                name, email, phone_num, address, dob, gender, doctor = input
		#After input is recieved and processesed, we can call function to update database
        update_patient(id, name, email, phone_num, address, dob, gender, doctor)

def update_patient(id, name, email, phone_num, address, dob, gender, doctor):
	cur.execute("UPDATE patient SET Patient_Name=coalesce(?,Patient_Name), Patient_Email=coalesce(?,Patient_Email), Patient_PhoneNum=coalesce(?, Patient_PhoneNum), Home_Address=coalesce(?,Home_Address),Birth_Date=coalesce(?,Birth_Date),Gender=coalesce(?,Gender),Assigned_Doctor=coalesce(?, Assigned_Doctor) WHERE Patient_ID=?", (name, email, phone_num, address, dob, gender, doctor, id))

def delete_patient(id):
	cur.execute("DELETE FROM patient WHERE Patient_ID=?", (id,))
	con.commit()
	st.experimental_rerun()

def search_insurance(id):
	cur.execute("SELECT * FROM insurance WHERE Patient_ID=?", (id,))
	ins = cur.fetchall()
	st.dataframe(ins, column_config={"0":"Patient ID", "1":"Provider Name", "2":"Coverage","3":"Expiration Date"})

def search_patient_history(id):
	cur.execute("SELECT * FROM patient_history WHERE Patient_ID=?", (id,))
	history = cur.fetchall()
	st.dataframe(history, column_config={"0" : "Record ID", "1":"Patient ID", "2":"Diseases","3":"Surgeries","4":"Disabilities","5":"Genetic Predispositions", "6":"Concerns"})
		
def search_doctors(id, name):
	if (id == '' or name == ''):
		cur.execute("SELECT * FROM doctor WHERE Doctor_ID=? OR Doctor_Name=?", (id, name))
	else:
		cur.execute("SELECT * FROM doctor WHERE Doctor_ID=? AND Doctor_Name=?", (id, name))
	doctors = cur.fetchall()
	if len(doctors) > 0:
		st.dataframe(doctors, width=800, column_config={"0":"Doctor ID", "1":"Name", "2": "Gender", "3":"Role"})
		cur.execute("SELECT COUNT(Assigned_Doctor) FROM patient WHERE Assigned_Doctor=?", (id,))
		num_patients = cur.fetchone()
		st.write("Number of Patients:",num_patients[0])
		col1, col2 = st.columns(2)
		edit = col1.toggle("Edit Doctor")
		delete = col2.button("Delete Doctor", type="primary")
		if edit:
			edit_doctor_form(id)
		if delete:
			delete_doctor(id,name)

def edit_doctor_form(id):
	st.write("Please Enter New Doctor Information")
	with st.form(key='edit_doctor_form'):
		name = st.text_input("*Doctor's Name: ")
		gender = st.text_input("Gender (M/F): ")
		primary_role =  st.text_input("Primary Role: ")
		submit = st.form_submit_button(label="Submit Updated Doctor Information")
	if submit == True:
		st.success("Doctor data has been successfully updated")
		input = [name, gender, primary_role]
		for i, var in enumerate(input):
			if var == '':
				input[i] = None
				name, gender, primary_role = input
		edit_doctor(id, name, gender, primary_role)

def edit_doctor(id, name, gender, role):
    cur.execute("UPDATE doctor SET Doctor_Name=coalesce(?, Doctor_Name), Gender=coalesce(?, Gender), Primary_Role=coalesce(?, Primary_Role) WHERE Doctor_ID=?", (name, gender, role, id))

def delete_doctor(id, name):
	cur.execute("DELETE FROM doctor WHERE Doctor_ID=? OR Doctor_Name=?", (id,name))
	con.commit()
	st.experimental_rerun()

def search_appointments(id):
	cur.execute("SELECT * FROM appointment WHERE Appointment_ID=?", (id,))
	appointments = cur.fetchall()
	if len(appointments) > 0:
		st.dataframe(appointments, width=800, column_config={"0":"Appointment ID", "1":"Patient ID", "2":"Doctor ID", "3":"Time", "4":"Date", "5":"Reason"})
		col1, col2 = st.columns(2)
		edit = col1.toggle("Edit Appointment")
		delete = col2.button("Delete Appointment", type="primary")
		if edit:
			edit_appointment_form(id)
		if delete:
			delete_appointment(id)

def edit_appointment_form(id):
	st.write("Enter Appointment Information")
	with st.form(key='edit_appointment_form'):
		patient_id = st.text_input("*Enter the ID of the involved patient: ")
		doctor_id = st.text_input("*Enter the ID of the involved doctor: ")
		time = st.text_input("Enter the time of the appointment: ")
		date = st.date_input("Enter the date of the appointment: ", value=None)
		reason = st.text_area("Enter the reason for the appointment", max_chars=300)
		submit = st.form_submit_button(label="Submit Appointment Edit")
	if submit == True:
		st.success("Appointment updated.")
		input = [patient_id, doctor_id, time, date, reason]
		for i, var in enumerate(input):
			if var == '':
				input[i] = None
				patient_id, doctor_id, time, date, reason = input
		edit_appointment(id, patient_id, doctor_id, time, date, reason)

def edit_appointment(id, p_id, d_id, time, date, reason):
    cur.execute("UPDATE appointment SET Patient_ID=coalesce(?, Patient_ID), Doctor_ID=coalesce(?,Doctor_ID), Appointment_Time=coalesce(?, Appointment_Time), Appointment_Date=coalesce(?,Appointment_Date), Reason=coalesce(?,Reason) WHERE Appointment_ID=?", (p_id, d_id, time, date, reason, id))

def delete_appointment(id):
	cur.execute("DELETE FROM appointment WHERE Appointment_ID=?", (id,))
	con.commit()
	st.experimental_rerun()

def search_prescriptions(id):
	cur.execute("SELECT * FROM prescription WHERE Prescription_ID=?", (id,))
	prescriptions = cur.fetchall()
	if(len(prescriptions) > 0):
		st.dataframe(prescriptions, width=500, column_config={"0":"Prescription ID", "1":"Patient ID", "2":"Refill Frequency", "3" : "Dose"})
		st.session_state.search_presc = True
		pres_id = prescriptions[0][0]
		if "search_presc" in st.session_state:
			cur.execute("SELECT COUNT(Prescription_ID) FROM medication WHERE Prescription_ID=?", (id,))
			num_meds = cur.fetchone()
			st.write("Number of Medications:",num_meds[0])
			col1, col2, col3 = st.columns(3)
			history_active = col1.toggle("View medications in this prescription?")
			edit = col2.toggle("Edit Prescription")
			delete = col3.button("Delete Prescription", type="primary")
			if history_active:
				search_medications(pres_id)
			if edit:
				edit_prescription_form(pres_id)
			if delete:
				delete_prescription(pres_id)

def edit_prescription_form(id):
	st.write("Please Enter Prescription Information")
	with st.form(key='edit_prescription_form'):
		patient = st.text_input("*ID of prescribed patient")
		refill = st.text_input("Refill Frequency: ")
		dose = st.text_input("Dosage: ")
		submit = st.form_submit_button(label="Update Prescription")
	if submit == True:
		st.success("Prescription has been successfully updated")
		input = [patient, refill, dose]
		for i, var in enumerate(input):
			if var == '':
				input[i] = None
				patient, refill, dose = input
		edit_prescription(id, patient, refill, dose)

def edit_prescription(id, p_id, refill, dose):
    cur.execute("UPDATE prescription SET Patient_ID=coalesce(?, Patient_ID), Refill_Frequency=coalesce(?, Refill_Frequency), Dose=coalesce(?, Dose) WHERE Prescription_ID=?", (p_id, refill, dose, id))

def delete_prescription(id):
	cur.execute("DELETE FROM prescription WHERE Prescription_ID=?", (id,))
	con.commit()
	st.experimental_rerun()
	
def search_medications(pres_id):
	cur.execute("SELECT * FROM medication WHERE Prescription_ID=?", (pres_id,))
	meds = cur.fetchall()
	st.dataframe(meds, column_config={"0":"Prescription ID", "1":"Medication Name", "2": "Cost"})

make_base_schema()
home_page()

con.commit()
con.close()