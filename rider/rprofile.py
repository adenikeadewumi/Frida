import streamlit as st
from general.auth import *

# Retrieve uid and use it to access rider's name
uid= st.session_state.get("uid", None)
docs=  db.collection("riders").document(uid).get().to_dict()

if docs is not None:
    if "first_name" in docs:
        first_name= docs["first_name"]
    else:
        first_name= "User"
else:
    first_name="User"

st.title("My Profile")
st.write(f"Welcome back :red[{first_name}]")

# Create a form to collect user info and store it in the database
with st.form(key= "rprofile"):
    first_name= st.text_input("First Name")
    last_name= st.text_input("Last Name")
    if st.form_submit_button("Update"):
        riderid= st.session_state.get("riderid", None)
        riders_ref= db.collection("riders").document(uid)
        riders_ref.update({
            "first_name": first_name,
            "last_name": last_name,

        })
