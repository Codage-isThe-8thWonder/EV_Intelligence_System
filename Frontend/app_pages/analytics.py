import streamlit as st
import pandas as pd

from services.analytics_service import (
    get_summary_card,
    get_operational_trends,
    get_battery_analytics,
    get_vehicle_performance
)


def show_analytics_page():

    token = st.session_state.get(
        "token"
    )

    vehicle_id = st.session_state.get(
        "current_vehicle_id"
    )

    if not token:

        st.error(
            "Please login first."
        )

        return

    if vehicle_id is None:

        st.error(
            "Please select a vehicle."
        )

        return

    summary_response = get_summary_card(
        vehicle_id,
        token
    )

    trends_response = get_operational_trends(
        vehicle_id,
        token
    )

    battery_response = get_battery_analytics(
        vehicle_id,
        token
    )

    performance_response = get_vehicle_performance(
        vehicle_id,
        token
    )

    if (
        summary_response.status_code != 200
        or trends_response.status_code != 200
        or battery_response.status_code != 200
        or performance_response.status_code != 200
    ):

        st.error(
            "Unable to load analytics."
        )

        return

    summary = summary_response.json()

    trends = trends_response.json()

    battery = battery_response.json()

    performance = performance_response.json()

    st.title(
        "📊 Analytics"
    )

    # ==================================
    # SUMMARY CARDS
    # ==================================

    st.subheader(
        "📋 Summary Overview"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average SoC",
            f"{summary['avg_soc']:.2f}%"
        )

    with col2:

        st.metric(
            "Average SoH",
            f"{summary['avg_soh']:.2f}%"
        )

    with col3:

        st.metric(
            "Max Battery Temp",
            f"{summary['max_battery_temperature']:.2f} °C"
        )

    col4, col5, col6 = st.columns(3)

    with col4:

        st.metric(
            "Average Speed",
            f"{summary['avg_driving_speed']:.2f} km/h"
        )

    with col5:

        st.metric(
            "Total Distance",
            f"{summary['total_distance']:.2f} km"
        )

    with col6:

        st.metric(
            "Average Power",
            f"{summary['avg_power_consumption']:.2f}"
        )

    st.divider()

    # ==================================
    # OPERATIONAL TRENDS
    # ==================================

    st.subheader(
        "📈 Operational Trends"
    )

    st.write("SoC Trend")

    df = pd.DataFrame(
        trends["soc"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Battery Temperature Trend"
    )

    df = pd.DataFrame(
        trends["battery_temperature"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Driving Speed Trend"
    )

    df = pd.DataFrame(
        trends["driving_speed"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Power Consumption Trend"
    )

    df = pd.DataFrame(
        trends["power_consumption"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Motor Temperature Trend"
    )

    df = pd.DataFrame(
        trends["motor_temperature"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.divider()

    # ==================================
    # BATTERY ANALYTICS
    # ==================================

    st.subheader(
        "🔋 Battery Analytics"
    )

    st.write(
        "State of Health (SoH)"
    )

    df = pd.DataFrame(
        battery["soh"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Battery Voltage"
    )

    df = pd.DataFrame(
        battery["battery_voltage"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Battery Current"
    )

    df = pd.DataFrame(
        battery["battery_current"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Charge Cycles"
    )

    df = pd.DataFrame(
        battery["charge_cycles"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.divider()

    # ==================================
    # VEHICLE PERFORMANCE
    # ==================================

    st.subheader(
        "🚗 Vehicle Performance"
    )

    st.write(
        "Distance Travelled"
    )

    df = pd.DataFrame(
        performance["distance_traveled"]
    )

    st.line_chart(
        df.set_index("timestamp")
    )

    st.write(
        "Speed vs Power Consumption"
    )

    df = pd.DataFrame(
        performance["speed_vs_power"]
    )

    st.scatter_chart(
        df,
        x="driving_speed",
        y="power_consumption"
    )

    st.write(
        "Ambient Temperature vs Battery Temperature"
    )

    df = pd.DataFrame(
        performance[
            "ambient_vs_battery_temperature"
        ]
    )

    st.scatter_chart(
        df,
        x="ambient_temperature",
        y="battery_temperature"
    )