
import streamlit as st
import clickhouse_connect

client = clickhouse_connect.get_client(host='14.177.238.175', username='vgm', password='vgm123', database='vgm')
result = client.query('SELECT * from dataRandom12m limit 1')
st.write(result.result_rows)

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# def check_password():
#     """Returns `True` if the user had a correct password."""

#     def login_form():
#         """Form with widgets to collect user information"""
#         with st.form("Credentials"):
#             st.text_input("Username", key="username")
#             st.text_input("Password", type="password", key="password")
#             st.form_submit_button("Log in", on_click=password_entered)

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if st.session_state["username"] in st.secrets[
#             "passwords"
#         ] and hmac.compare_digest(
#             st.session_state["password"],
#             st.secrets.passwords[st.session_state["username"]],
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # Don't store the username or password.
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False

#     # Return True if the username + password is validated.
#     if st.session_state.get("password_correct", False):
#         return True

#     # Show inputs for username + password.
#     login_form()
#     if "password_correct" in st.session_state:
#         st.error("😕 User not known or password incorrect")
#     return False


# if not check_password():
#     st.stop()

# # Main Streamlit app starts here
# st.write("Here goes your normal Streamlit app...")
# st.button("Click me")
