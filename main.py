import streamlit as st
from general.auth import sign_up, logout, login

# Set up the pages general configuration
st.set_page_config(page_title="Frida", page_icon="🧊", layout= "wide", initial_sidebar_state="auto")


#initiate the log in and log out pages
login_page= st.Page(login, title= "Log in", icon= ":material/login:", default= True)
logout_page= st.Page(logout, title= "Log Out", icon= ":material/logout:")
sign_up_page= st.Page(sign_up, title= "Log in", icon= ":material/login:")

# Initiate the dashboard page, rider profile and driver profile pages
dashboard= st.Page("driver/dashboard.py", title="Dashboard",icon=":material/dashboard:", default=True)
rprofile= st.Page("rider/rprofile.py", title="Profile", icon=":material/person:" )
dprofile= st.Page("driver/dprofile.py", title="Profile", icon=":material/person:" )
home= st.Page("rider/home.py", title="Book a Ride", icon=":material/house:", default= True)

#Create an option menu
def login_signup():
    choice= st.selectbox("Log in or Create Account", ["Login", "Create Account"])
    if choice== "Login":
        login()
    else:
        sign_up()

login_signup= st.Page(login_signup, icon= ":material/login:")

# Check if user is logged in and display app according to type of user using the boolean global variable sign_up_as_driver 
user_type= st.session_state.get("user_type", None)
if st.session_state.logged_in:
    if user_type== "Driver":
        app= st.navigation([dprofile, dashboard, logout_page])
    if user_type=="Rider":
        app= st.navigation([rprofile, home, logout_page])
    
else:
    app= st.navigation([login_signup])

# run the app
# Check if app is defined before running
if app is not None:
    app.run()
else:
    st.error("Application state could not be determined.")