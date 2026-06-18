import streamlit as st

from services.auth_service import login_user
from services.vehicle_service import get_all_vehicles


# Custom Styling
st.markdown("""
<style>

.stApp {
    background-color: #F1F5F9;
}

</style>
""", unsafe_allow_html=True)


def show_login_page():

    left, center, right = st.columns([2, 3, 2])

    with center:

        st.markdown(
            """
            <h1 style='
                text-align:center;
                color:#22C55E;
                margin-bottom:0;
                font-weight:700;
            '>
                ⚡ EV Pulse
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style='
                text-align:center;
                color:#475569;
                font-size:18px;
                margin-bottom:5px;
            '>
                AI Powered EV Intelligence Platform
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style='
                text-align:center;
                color:#64748B;
                font-size:15px;
            '>
                Welcome back. Login to continue.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        with st.form("login_form"):

            identifier = st.text_input(
                "Email or Mobile Number",
                placeholder="Enter email or mobile number"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            login_btn = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if login_btn:

                if not identifier:

                    st.error(
                        "Email or Mobile Number is required."
                    )

                elif not password:

                    st.error(
                        "Password is required."
                    )

                else:

                    payload = {
                        "identifier": identifier,
                        "password": password
                    }

                    response = login_user(
                        payload
                    )

                    if response.status_code == 200:

                        token = response.json()["token"]

                        st.session_state["token"] = token

                        vehicle_response = (
                            get_all_vehicles(token)
                        )

                        if vehicle_response.status_code != 200:

                            st.error(
                                "Unable to fetch vehicles."
                            )

                            return

                        vehicles = (
                            vehicle_response.json()
                        )

                        # New User
                        if len(vehicles) == 0:

                            st.session_state["page"] = (
                                "linkEV"
                            )

                        # Existing User
                        else:

                            st.session_state[
                                "current_vehicle_id"
                            ] = vehicles[0][
                                "vehicle_id"
                            ]

                            st.session_state[
                                "authenticated"
                            ] = True

                        st.rerun()

                    else:

                        st.error(
                            response.json()["detail"]
                        )

        st.divider()

        st.markdown(
            """
            <p style='
                text-align:center;
                color:#64748B;
            '>
                Don't have an account? Register
            </p>
            """,
            unsafe_allow_html=True
        )

        if st.button("Create Account"):

            st.session_state["page"] = (
                "register"
            )

            st.rerun()