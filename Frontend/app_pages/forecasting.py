import streamlit as st
from services.forecasting_service import get_forecast


def show_forecasting_page():

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

    response = get_forecast(
        vehicle_id,
        token
    )

    if response.status_code != 200:

        st.error(
            response.json()["detail"]
        )

        return

    forecast = response.json()

    st.title(
        "📈 Forecasting"
    )

    st.divider()

    # =================================
    # SoC Forecast
    # =================================

    st.subheader(
        "🔋 SoC Forecast"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "1 Hour",
            f"{forecast['soc_forecast']['one_hour']:.2f}%"
        )

    with col2:

        st.metric(
            "6 Hours",
            f"{forecast['soc_forecast']['six_hours']:.2f}%"
        )

    with col3:

        st.metric(
            "24 Hours",
            f"{forecast['soc_forecast']['twenty_four_hours']:.2f}%"
        )

    st.divider()

    # =================================
    # Voltage Forecast
    # =================================

    st.subheader(
        "⚡ Battery Voltage Forecast"
    )

    col4, col5, col6 = st.columns(3)

    with col4:

        st.metric(
            "1 Hour",
            f"{forecast['voltage_forecast']['one_hour']:.2f} V"
        )

    with col5:

        st.metric(
            "6 Hours",
            f"{forecast['voltage_forecast']['six_hours']:.2f} V"
        )

    with col6:

        st.metric(
            "24 Hours",
            f"{forecast['voltage_forecast']['twenty_four_hours']:.2f} V"
        )

    st.divider()

    # =================================
    # Forecast Summary
    # =================================

    st.subheader(
        "📝 Forecast Summary"
    )

    soc_24 = (
        forecast["soc_forecast"]
        ["twenty_four_hours"]
    )

    voltage_24 = (
        forecast["voltage_forecast"]
        ["twenty_four_hours"]
    )

    if soc_24 < 20:

        st.warning(
            "SoC is forecasted to fall below 20% within 24 hours."
        )

    else:

        st.success(
            "SoC forecast remains within a healthy range."
        )

    if voltage_24 < 300:

        st.warning(
            "Battery voltage is forecasted to drop below 300 V."
        )

    else:

        st.success(
            "Battery voltage forecast remains stable."
        )