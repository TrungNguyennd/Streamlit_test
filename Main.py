import hmac
import streamlit as st
from streamlit_lottie import st_lottie
import json
def check_password():
    """Returns `True` if the user had a correct password."""
    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"] and
            hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["username"]],
            )
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct") is True:
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

if not check_password():
    st.stop()

# Trang chính sau khi đăng nhập
def show_main_page():
    st.markdown("""
    # Atlas điện tử - Dân số Hà Nội
    ---
    ### Sử dụng dữ liệu của Chi cục dân số  - kế hoạch hóa gia đình để xây dựng lên các atlas điện tử.
    ---
    """)

    lottie2 = load_lottiefile("place2.json")
    st_lottie(lottie2, key='place', height=400, width=400)

# Main Streamlit app starts here
show_main_page()

# Ẩn widget đăng nhập khi đã đăng nhập thành công
st.text("")  # hoặc st.empty()
