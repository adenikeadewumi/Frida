# Import necessary libraries
import streamlit as st
from general.auth import *


st.title("My Profile")
st.write("Let your customers get to know you better")


# Using a streamlit form, get addition information from the user and save to his document
with st.form(key= "dprofile"):
    first_name= st.text_input("First Name")
    last_name= st.text_input("Last Name")
    pricekm= st.text_input("Enter your rate per kilometre")
    cartype= st.text_input("Vehicle brand e.g Toyota, Audi")
    #driver_picture= st.file_uploader("Add a Profile picture")
    st.write("Preferred Payment Details")
    acc_num= st.text_input("Enter your account number")
    bank_name= st.text_input("Bank name")
    acc_name= st.text_input("Account Name")
    if st.form_submit_button("Update"):
        # get userid
        uid= st.session_state.get("uid", None)
        # Update user's document
       # db= st.session_state.get('db', None)
        driver_ref= db.collection("drivers").document(uid)
        driver_ref.update({
            "first_name": first_name,
            "last_name": last_name,
            "pricekm": pricekm,
            "cartype": cartype,
            "account_number": acc_num,
            "bank_name": bank_name,
            "account_name": acc_name
        })
        st.success("Successfully Updated")



