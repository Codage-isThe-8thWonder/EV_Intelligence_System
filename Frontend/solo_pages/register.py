from services.auth_service import register_user
import streamlit as st


# Custom Styling
st.markdown("""
<style>

.stApp {
    background-color: #F1F5F9;
}

</style>
""", unsafe_allow_html=True)


def show_register_page():
    # Center Layout
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
                EV Intelligence and Predictive Analytics Platform
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
                Create your account to get started
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        with st.form("register_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter email"
            )

            mobile_number = st.text_input(
                "Mobile Number",
                placeholder="Enter mobile number"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm password"
            )

            register_btn = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if register_btn:

                if not username:
                    st.error("Username is required.")

                elif not email:
                    st.error("Email is required.")

                elif not mobile_number:
                    st.error("Mobile number is required.")

                elif not password:
                    st.error("Password is required.")

                elif password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    payload = {
                        "username": username,
                        "email": email,
                        "mobile_number": mobile_number,
                        "password": password
                    }

                    response = register_user(payload)

                    if response.status_code == 201:

                        st.success("Registration Successful")

                        st.session_state["page"] = "login"

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
                Already have an account? Login
            </p>
            """,
            unsafe_allow_html=True
        )


        if st.button("Login"):
            st.session_state["page"] = "login"
            st.rerun()