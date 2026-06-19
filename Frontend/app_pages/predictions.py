import streamlit as st
from services.predictions_service import get_predictions

def show_predictions_page():

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

    response = get_predictions(
        vehicle_id,
        token
    )

    if response.status_code != 200:

        st.error(
            response.json()["detail"]
        )

        return

    prediction = response.json()

    st.title(
        "🔮 Predictions"
    )

    st.divider()

    # ----------------------------------
    # Prediction Cards
    # ----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Remaining Useful Life",
            f"{prediction['rul']:.0f} days"
        )

    with col2:

        st.metric(
            "Failure Probability",
            f"{prediction['failure_probability'] * 100:.2f}%"
        )

    with col3:

        st.metric(
            "Health Score",
            f"{prediction['component_health_score']:.2f}"
        )

    col4, col5 = st.columns(2)

    with col4:

        st.metric(
            "Estimated Driving Range",
            f"{prediction['estimated_driving_range']:.2f} km"
        )

    with col5:

        st.metric(
            "Estimated Charging Time",
            f"{prediction['estimated_charging_time']:.2f} hrs"
        )
