import streamlit as st

from services.vehicle_service import get_vehicle_by_id
from services.analytics_service import get_summary_card
from services.recommendations_service import get_recommendations



def show_dashboard_page():

    token = st.session_state.get("token")

    vehicle_id = st.session_state.get("current_vehicle_id")

    if not token:
        st.error("Please login first.")
        return

    if vehicle_id is None:
        st.warning("Please select a vehicle first.")
        return

    vehicle_response = get_vehicle_by_id(
        vehicle_id,
        token
    )

    summary_response = get_summary_card(
        vehicle_id,
        token
    )

    recommendation_response = get_recommendations(
        vehicle_id,
        token
    )

    if vehicle_response.status_code != 200:

        st.error(
            "Unable to fetch vehicle details."
        )

        return

    if summary_response.status_code != 200:

        st.error(
            "Unable to fetch dashboard data."
        )

        return

    vehicle = vehicle_response.json()

    summary = summary_response.json()

    recommendations = []

    if recommendation_response.status_code == 200:
        recommendations = recommendation_response.json()["recommendations"]


    st.title("⚡ EV Pulse Dashboard")

    st.divider()

    # ----------------------------------
    # Vehicle Information
    # ----------------------------------

    st.subheader(
        "🚗 Vehicle Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
            Nickname : {vehicle['nickname']}

            Battery Capacity : {vehicle['battery_capacity']} kWh
            """
        )

    with col2:

        st.info(
            f"""
            Manufacturer : {vehicle['manufacturer']}

            Model : {vehicle['model']}
        """
        )

    st.divider()

    # ----------------------------------
    # Vehicle Summary
    # ----------------------------------

    st.subheader(
        "📊 Vehicle Summary"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average SoC",
            f"{summary['avg_soc']*100:.2f}%"
            if summary["avg_soc"] is not None
            else "-"
        )

    with col2:

        st.metric(
            "Total Distance",
            f"{summary['total_distance']:.2f} km"
            if summary["total_distance"] is not None
            else "-"
        )

    with col3:

        st.metric(
            "Average Driving Speed",
            f"{summary['avg_driving_speed']:.2f} km/h"
            if summary["avg_driving_speed"] is not None
            else "-"
        )

    st.divider()

    # ----------------------------------
    # Critical Alerts
    # ----------------------------------

    st.subheader(
        "🚨 Priority Actions Recommended"
    )

    critical_found = False

    for item in recommendations:

        if item["severity"] == "critical":

            critical_found = True

            st.error(item["message"])

    if not critical_found:

        st.success("No critical issues detected.")