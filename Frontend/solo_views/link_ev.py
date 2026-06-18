import streamlit as st

from services.vehicle_service import (
    add_vehicle,
    get_all_vehicles
)

from services.csv_service import upload_csv


def show_linkEV_page():

    st.title("⚡ My Vehicles")

    token = st.session_state.get("token")

    if not token:
        st.error("Please login first")
        return

    response = get_all_vehicles(token)

    vehicles = []

    if response.status_code == 200:

        vehicles = response.json()

        if len(vehicles) > 0:

            st.subheader("Linked Vehicles")

            for vehicle in vehicles:

                st.info(
                    f"""
Manufacturer : {vehicle['manufacturer']}

Model : {vehicle['model']}

Nickname : {vehicle['nickname']}

Battery Capacity : {vehicle['battery_capacity']}
"""
                )

    st.divider()

    # --------------------------------------------------
    # Add Vehicle Section
    # --------------------------------------------------

    st.subheader("Add New Vehicle")

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
                    "Vehicle Added Successfully"
                )

                st.rerun()

            else:

                st.error(
                    response.json()["detail"]
                )

    st.divider()

    # --------------------------------------------------
    # CSV Upload Section
    # --------------------------------------------------

    if len(vehicles) > 0:

        st.subheader("Upload EV Dataset")

        vehicle_options = {
            f"{vehicle['manufacturer']} - {vehicle['model']}":
            vehicle["vehicle_id"]
            for vehicle in vehicles
        }

        selected_vehicle = st.selectbox(
            "Select Vehicle",
            options=list(vehicle_options.keys())
        )

        st.session_state["current_vehicle_id"] = (
        vehicle_options[selected_vehicle]
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
                    "Please select a CSV file"
                )

            else:

                vehicle_id = vehicle_options[
                    selected_vehicle
                ]

                response = upload_csv(
                    vehicle_id,
                    uploaded_file,
                    token
                )

                if response.status_code == 201:

                    st.success(
                        "CSV Uploaded Successfully"
                    )

                else:

                    st.error(
                        response.json()["detail"]
                    )

    st.divider()

    # --------------------------------------------------
    # Dashboard Navigation
    # --------------------------------------------------

    if len(vehicles) > 0:

        if st.button(
            "Continue To Dashboard",
            use_container_width=True
        ):

            st.session_state["authenticated"] = True

            st.rerun()