import streamlit as st
from services.recommendations_service import get_recommendations


def show_recommendations_page():

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

    response = get_recommendations(
        vehicle_id,
        token
    )

    if response.status_code != 200:

        st.error(
            response.json()["detail"]
        )

        return

    data = response.json()

    recommendations = (
        data["recommendations"]
    )

    st.title(
        "💡 Recommendations"
    )

    if not recommendations:

        st.success(
            "No recommendations available."
        )

        return

    # ----------------------------------
    # Recommendation Counts
    # ----------------------------------

    critical_count = 0
    warning_count = 0
    info_count = 0

    for item in recommendations:

        if item["severity"] == "critical":

            critical_count += 1

        elif item["severity"] == "warning":

            warning_count += 1

        else:

            info_count += 1

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Critical",
            critical_count
        )

    with col2:

        st.metric(
            "Warning",
            warning_count
        )

    with col3:

        st.metric(
            "Info",
            info_count
        )

    st.divider()

    # ----------------------------------
    # Critical Recommendations
    # ----------------------------------

    if critical_count > 0:

        st.subheader(
            "🚨 Critical Recommendations"
        )

        for item in recommendations:

            if item["severity"] == "critical":

                st.error(
                    item["message"]
                )

        st.divider()

    # ----------------------------------
    # Warning Recommendations
    # ----------------------------------

    if warning_count > 0:

        st.subheader(
            "⚠️ Warning Recommendations"
        )

        for item in recommendations:

            if item["severity"] == "warning":

                st.warning(
                    item["message"]
                )

        st.divider()

    # ----------------------------------
    # Informational Recommendations
    # ----------------------------------

    if info_count > 0:

        st.subheader(
            "ℹ️ Informational Recommendations"
        )

        for item in recommendations:

            if item["severity"] == "info":

                st.info(
                    item["message"]
                )