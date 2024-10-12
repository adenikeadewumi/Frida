import streamlit as st
from general.get_location import locationCoordinates
from firebase_admin import firestore
import plyer

#Initialize the database 
# Igot how to use firestore from google and firestore documentation
db= firestore.client()

st.title("New orders will appear here")


def get_driver_location():
    dlat,dlong = locationCoordinates()
    if dlat is not None and dlong is not None:
       return dlat, dlong
    else:
        return 0,0

coordinates= get_driver_location()
if "coordinates" not in st.session_state:
    st.session_state.coordinates= coordinates
    
def update_availability():
    st.selectbox(":red[Update Availability Status]", ["Available", "Away", "Busy", "Out of service"])

st.write("My status")
availability= update_availability()
if availability not in st.session_state:
    st.session_state.availability= availability
# We have to know when a driver as been booked then notify him when this happens"""
uid = st.session_state.get("uid", None)
booked_docs= db.collection("drivers").document(uid).get().to_dict()
if "booked" in booked_docs:
    booked= booked_docs["booked"]
else:
    booked= None
st.session_state.booked= booked
if booked is None:
    st.markdown("No bookings yet")
else:
    plyer.notification.notify(
    title= "New Booking Received",
    message= "You just got an order",
    app_name= "Frida",
    app_icon= "🧊",
    timeout= 15,
    toast= False
)
    st.markdown("You just got an Order")

    pass
