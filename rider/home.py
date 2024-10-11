import streamlit as st
from general.get_location import locationCoordinates, nearest_drivers
from firebase_admin import firestore

#Initialize the database
db= firestore.client()

# Get the rider's realtime location
def get_rider_location():
    rlat,rlong= locationCoordinates()
    if rlat is not None and rlong is not None:
       return rlat, rlong
    else:
        return 0,0

# Initiate the coordinates session state
coordinates= get_rider_location()
if "coordinates" not in st.session_state:
    st.session_state.coordinates= coordinates

#Retrieve the user uid and use this to access the userid in the database
uid= st.session_state.get("uid",None)
riderid= db.collection("riders").document(uid).get().to_dict()["userid"]

# Get list of near drivers
list_near_drivers= nearest_drivers(riderid)


st.title("Book a ride")


# Function to show availbale drivers near a rider
def show_avail_drivers(key="available driver"):
    from plyer import notification
    riderid= st.session_state.get("uid",None)
    num_drivers= len(list_near_drivers)
    if num_drivers== 0:
        st.write("No available drivers nearby")

    counter=0
    while counter<num_drivers:
        cols= st.columns(num_drivers)
        for i in cols:
            with i:
                for j in list_near_drivers:
                    drivers_ref= db.collection("drivers").document(j)
                    driver_name= drivers_ref.get().to_dict()["first_name"]
                    vehicle_type= drivers_ref.get().to_dict()["cartype"]
                    price_km= drivers_ref.get().to_dict()["pricekm"]
                    st.write(f"{driver_name}")
                    st.write(f"{vehicle_type}")
                    st.write(f"Price per km: #{price_km}")
                if st.button("Book", key= "get_drivers"):
                    db.collection("drivers").document(j).update({
                        "book_status": "booked"
                    })
                    # Notify the driver
        counter+= 1
    
show_avail_drivers()






