import streamlit as st

from services.vehicle_service import (
    add_vehicle,
    get_all_vehicles
)

from services.csv_service import (
    upload_csv
)


def show_linkEV_page():

    st.title("⚡ Link Your EV")

    token = st.session_state.get("token")

    if not token:

        st.error(
            "Please login first."
        )

        return

    # --------------------------------------------------
    # Fetch Vehicles
    # --------------------------------------------------

    response = get_all_vehicles(token)

    if response.status_code != 200:

        st.error(
            "Unable to fetch vehicles."
        )

        return

    vehicles = response.json()

    # --------------------------------------------------
    # Add Vehicle Section
    # --------------------------------------------------

    st.subheader(
        "🚗 Add Your Vehicle"
    )

    with st.form("vehicle_form"):

        manufacturer = st.text_input(
            "Manufacturer"
        )

        model = st.text_input(
            "Model"
        )

        nickname = st.text_input(
            "Nickname"
        )

        battery_capacity = st.number_input(
            "Battery Capacity (kWh)",
            min_value=0.0,
            step=1.0
        )

        add_btn = st.form_submit_button(
            "Add Vehicle",
            use_container_width=True
        )

        if add_btn:

            with st.spinner("Adding Vehicle..."):

                payload = {
                    "manufacturer": manufacturer,
                    "model": model,
                    "nickname": nickname,
                    "battery_capacity": battery_capacity
                }

                response = add_vehicle(
                    payload,
                    token
                )

                if response.status_code == 201:

                    st.success(
                        "Vehicle Added Successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        response.json()["detail"]
                    )

    st.divider()

    # --------------------------------------------------
    # Optional CSV Upload
    # --------------------------------------------------

    if len(vehicles) > 0:

        st.subheader(
            "📁 Upload Your EV Dataset"
        )

        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"]
        )

        if st.button(
            "Upload CSV",
            use_container_width=True
        ):

            if uploaded_file is None:

                st.error(
                    "Please select a CSV file."
                )

            else:

                vehicle_id = vehicles[0][
                    "vehicle_id"
                ]

                response = upload_csv(
                    vehicle_id,
                    uploaded_file,
                    token
                )

                if response.status_code == 200:

                    st.success(
                        "CSV Uploaded Successfully."
                    )

                else:

                    st.error(
                        response.json()["detail"]
                    )

    st.divider()

    # --------------------------------------------------
    # Continue To Dashboard
    # --------------------------------------------------

    if len(vehicles) == 0:

        st.warning(
            "Please add at least one vehicle to continue."
        )

    else:

        st.success(
            "Vehicle linked successfully. You can continue to the dashboard."
        )

        if st.button(
            "Continue To Dashboard",
            use_container_width=True
        ):

            st.session_state[
                "current_vehicle_id"
            ] = vehicles[0][
                "vehicle_id"
            ]

            st.session_state[
                "authenticated"
            ] = True

            st.rerun()