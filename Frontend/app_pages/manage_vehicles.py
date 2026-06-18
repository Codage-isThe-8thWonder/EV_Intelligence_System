import streamlit as st

from services.vehicle_service import (
    get_all_vehicles,
    add_vehicle,
    delete_vehicle
)

from services.csv_service import (
    upload_csv
)


def show_manage_vehicles_page():

    st.title(
        "🚗 Manage Vehicles"
    )

    token = st.session_state.get(
        "token"
    )

    if not token:

        st.error(
            "Please login first."
        )

        return

    response = get_all_vehicles(
        token
    )

    if response.status_code != 200:

        st.error(
            "Unable to fetch vehicles."
        )

        return

    vehicles = response.json()

    # ==================================
    # LINKED VEHICLES
    # ==================================

    st.subheader(
        "Linked Vehicles"
    )

    if len(vehicles) == 0:

        st.info(
            "No vehicles linked yet."
        )

    else:

        for vehicle in vehicles:

            with st.container():

                st.info(
                    f"""
Manufacturer : {vehicle['manufacturer']}

Model : {vehicle['model']}

Nickname : {vehicle['nickname']}

Battery Capacity : {vehicle['battery_capacity']} kWh
                    """
                )

                if st.button(
                    f"Delete Vehicle {vehicle['vehicle_id']}"
                ):

                    delete_response = delete_vehicle(
                        vehicle["vehicle_id"],
                        token
                    )

                    if delete_response.status_code == 204:

                        st.success(
                            "Vehicle deleted."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to delete vehicle."
                        )

    st.divider()

    # ==================================
    # CSV UPLOAD
    # ==================================

    st.subheader(
        "📂 Upload EV Dataset"
    )

    if len(vehicles) > 0:

        vehicle_options = {

            f"{v['manufacturer']} - {v['model']}":
            v["vehicle_id"]

            for v in vehicles
        }

        selected_vehicle = st.selectbox(
            "Select Vehicle",
            options=list(
                vehicle_options.keys()
            )
        )

        csv_file = st.file_uploader(
            "Choose CSV File",
            type=["csv"]
        )

        if st.button(
            "Upload CSV"
        ):

            if csv_file is None:

                st.error(
                    "Please select a CSV file."
                )

            else:

                vehicle_id = (
                    vehicle_options[
                        selected_vehicle
                    ]
                )

                upload_response = upload_csv(
                    vehicle_id,
                    csv_file,
                    token
                )

                if upload_response.status_code == 200:

                    st.success(
                        "CSV uploaded successfully."
                    )

                else:

                    st.error(
                        upload_response.json()[
                            "detail"
                        ]
                    )

    st.divider()

    # ==================================
    # ADD NEW VEHICLE
    # ==================================

    st.subheader(
        "➕ Add New Vehicle"
    )

    with st.form(
        "add_vehicle_form"
    ):

        manufacturer = st.text_input(
            "Manufacturer"
        )

        model = st.text_input(
            "Model"
        )

        nickname = st.text_input(
            "Nickname"
        )

        battery_capacity = (
            st.number_input(
                "Battery Capacity (kWh)",
                min_value=0.0,
                step=1.0
            )
        )

        add_btn = st.form_submit_button(
            "Add Vehicle"
        )

        if add_btn:

            payload = {

                "manufacturer":
                    manufacturer,

                "model":
                    model,

                "nickname":
                    nickname,

                "battery_capacity":
                    battery_capacity
            }

            add_response = add_vehicle(
                payload,
                token
            )

            if add_response.status_code == 201:

                st.success(
                    "Vehicle added successfully."
                )

                st.rerun()

            else:

                st.error(
                    add_response.json()[
                        "detail"
                    ]
                )