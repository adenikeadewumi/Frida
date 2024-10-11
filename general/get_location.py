# install required libraries

import streamlit as st
import requests
from math import *
from firebase_admin import firestore

db= firestore.client()

# define funstion to get user's latitude and longitude
def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        return lat, long
    except:
        #Displaying ther error message
        return None, None
    
# Assign coordinates to database
def assign_coordinates_to_database():
    user_type = st.session_state.get("user_type", None)
    uid= st.session_state.get("uid", None)

    if user_type== 'Driver':
       dlat, dlong= st.session_state.get("coordinates", (None,None))
       # get driverid
       driver_id= db.collection("drivers").document(uid).get().to_dict()['userid']
       
       locations= db.collection("drivers_location").document(driver_id)
       locations.set({
        "dlat": dlat,
        "dlong": dlong,
        "driverid": uid
        })
    if user_type== 'Rider':
       rlat, rlong = st.session_state.get("coordinates", (None,None))
       # get riderid
       rider_id= db.collection("riders").document(uid).get().to_dict()['userid']
       locations= db.collection("riders_location").document(rider_id)
       locations.set({
        "rlat": rlat,
        "rlong": rlong,
        "riderid": uid})
       
# Initiate coordinates in streamlit session_state
if 'coordinates' not in st.session_state:
    st.session_state.coordinates = locationCoordinates()

# Call the function
assign_coordinates_to_database()


# get the distance between the rider and driver using acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371
def get_distance(dlat,dlong,rlat,rlong):
    r= 6371 # distance of the earth
    c= acos(sin(dlat)*sin(rlat)+cos(dlat)*cos(rlat)*cos(rlong-dlong))
    distance= r*c
    return distance


# check for the nearest driver
def nearest_drivers(riderid):
    list_near_driverid=[]

    drivers_location= db.collection("drivers_location").stream()
    for driver_location in drivers_location:
       dloc= driver_location.to_dict()
       dlat,dlong, driverid= dloc["dlat"], dloc["dlong"], dloc["driverid"]
    rloc= db.collection("riders_location").document(riderid).get().to_dict()
    rlat, rlong= rloc["rlat"], rloc["rlong"]
    distance= get_distance(dlat,dlong,rlat,rlong)
    if distance<= 10:
        list_near_driverid.append(driverid)

    return list_near_driverid


