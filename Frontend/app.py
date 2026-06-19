import streamlit as st

from solo_pages.login import show_login_page
from solo_pages.register import show_register_page
from solo_pages.link_ev import show_linkEV_page
from services.vehicle_service import get_all_vehicles
from app_pages.predictions import show_predictions_page
from app_pages.forecasting import show_forecasting_page
from app_pages.recommendations import show_recommendations_page
from app_pages.manage_vehicles import show_manage_vehicles_page

from app_pages.dashboard import show_dashboard_page
from app_pages.analytics import show_analytics_page


st.set_page_config(
    page_title="EV Pulse",
    page_icon="⚡",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "token" not in st.session_state:
    st.session_state["token"] = None

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_vehicle_id" not in st.session_state:
    st.session_state["current_vehicle_id"] = None

# -----------------------------
# BEFORE LOGIN
# -----------------------------

if not st.session_state["authenticated"]:

    if st.session_state["page"] == "login":
        show_login_page()

    elif st.session_state["page"] == "register":
        show_register_page()

    elif st.session_state["page"] == "linkEV":
        show_linkEV_page()

# -----------------------------
# AFTER LOGIN
# -----------------------------

else:

    st.sidebar.title("⚡ EV Pulse")

    token = st.session_state["token"]

    vehicle_response = get_all_vehicles(token)

    vehicles = vehicle_response.json()

    if len(vehicles) == 0:
        st.session_state["page"] = "linkEV"
        st.session_state["authenticated"] = False

        st.rerun()


    selected_page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Analytics",
            "Predictions",
            "Forecasting",
            "Recommendations",
            "Manage Vehicles",
            "Settings"
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()

    if selected_page == "Dashboard":
        show_dashboard_page()

    elif selected_page == "Analytics":
        show_analytics_page()
    
    elif selected_page == "Predictions":
        show_predictions_page()

    elif selected_page == "Forecasting":
        show_forecasting_page()

    elif selected_page == "Recommendations":
        show_recommendations_page()
    
    elif selected_page == "Manage Vehicles":
        show_manage_vehicles_page()

    else:
        st.title(selected_page)
        st.info(
            f"{selected_page} page will come soon, Not launched yet."
        )