import streamlit as st
# Google (How to store and access real-time data )
import firebase_admin
from firebase_admin import credentials,auth, firestore
import pyrebase
# Library to get the timestamp a user signs up in order to use it to generate a userid
from datetime import datetime


# Setup firebase credential
cred = credentials.Certificate("frida-ride-system-0562e0aca56e.json")

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
   firebase_admin.initialize_app(cred)  #This has to be commented after runnung the app once to prevent any error

# Initialize Firestore
db = firestore.client()

# Youtube
firebaseConfig = {
  "apiKey": "AIzaSyB6hzhW4oMWFnN0jyAdmLeLK8XCf4O8Viw",
  "authDomain": "frida-ride-system.firebaseapp.com",
  "projectId": "frida-ride-system",
  "storageBucket": "frida-ride-system.appspot.com",
  "messagingSenderId": "256066214357",
  "appId": "1:256066214357:web:c077afa67f806cca26c55c",
  "measurementId": "G-58HHNRPN8F",
  "databaseURL": "https://frida-ride-system-default-rtdb.firebaseio.com/"
}

# Initialize firebase
firebase= pyrebase.initialize_app(firebaseConfig)
auth= firebase.auth()


                    
# define the sign up function that also uses firebase to store user's info by creating collections and documents for each information set

def sign_up():

    # Create a form to collect user input
    with st.form(key="signup"):
        st.title("Welcome to :blue[FRIDA]")
        st.write("Create My Account")
        email= st.text_input("Email Address")
        password= st.text_input("Password", type="password")
        user_type= st.selectbox("Sign Up as: ", ["Driver", "Rider"])
        
        if st.form_submit_button("Create Account"):
            try:
                user= auth.create_user_with_email_and_password(email, password)
                
                if user_type== "Driver":
                    uid = user["localId"]
                    driverid= password + str(datetime.now().microsecond)
                    # My aim is to create a collection "users" with subcollections "riders" and " drivers" and store the user data in a document using their local ID but I just can't seem to get the hang of it
                    # So I went for four separate collections drivers, riders, riders_location and drivers_location
                    drivers_ref= db.collection("drivers").document(user['localId'])
                    drivers_ref.set({
                     'user_type': user_type,
                     'userid': driverid,
                     "uid": uid
                    })
                else:
                    uid = user["localId"]
                    riderid= password + str(datetime.now().microsecond)
                    riders_ref= db.collection("riders").document(user['localId'])
                    riders_ref.set({
                       'user_type': user_type,
                       'userid': riderid,
                       "uid": uid   
                })
                
                st.success("Your account as been created. \nLogin to proceed")
            # Handle any error that may occur
            except Exception as e :
                st.error(e)




# Initialize session states for the  following
if "logged_in" not in st.session_state:
    st.session_state.logged_in= False

if "user_type" not in st.session_state:
    st.session_state.user_type= None

if "uid" not in st.session_state:
    st.session_state.uid= None

def login():
    with st.form(key="login"):
        st.title("Welcome to :blue[FRIDA]")
        st.write("Log-in")
        email= st.text_input("Email Address")
        password= st.text_input("Password", type="password")
        st.write("Please pick the same option as when you signed up")
        user_type= st.selectbox("Driver/Rider", ["Rider", "Driver"])
        if st.form_submit_button("Login"):
            
            try:
                user= auth.sign_in_with_email_and_password(email,password)
                uid= user["localId"]
                st.session_state.logged_in= True
                # Retrieve user_type and userid for every log in session
                st.session_state.user_type= user_type
                st.session_state.uid= uid
                st.success("Login successful")
            except Exception:
                st.warning("Invalid email or password")
                st.session_state.logged_in= False




# Define the log out function
def logout():
    st.title("Thank you for using Frida.")
    if st.button("Log Out"):
        st.session_state.logged_in= False
        st.success("Logged Out successful")
        st.success("We hope to see you soon")
        st.rerun()
                                                             
