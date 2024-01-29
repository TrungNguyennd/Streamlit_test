import streamlit as st

# Tạo một session state để lưu trạng thái đăng nhập
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

def login(username, password):
    # Thực hiện xác thực đơn giản (có thể cần thay đổi)
    if username == "admin" and password == "password":
        st.session_state.is_logged_in = True
        return True
    else:
        return False

# Trang đăng nhập
def show_login_page():
    st.title("Đăng nhập")

    # Hiển thị các ô nhập liệu và nút đăng nhập
    username = st.text_input("admin")
    password = st.text_input("admin", type="password")
    login_button = st.button("Đăng nhập")

    # Xử lý sự kiện khi nút đăng nhập được nhấn
    if login_button:
        if login(username, password):
            st.success("Đăng nhập thành công!")

            # Điều hướng đến trang chính (main.py) bằng cách thay đổi URL
            st.experimental_set_query_params(logged_in=True)
        else:
            st.error("Đăng nhập không thành công. Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.")

# Trang chính sau khi đăng nhập
def show_main_page():
    st.title("Trang chính")
    st.success("Bạn đã đăng nhập thành công!")

# Kiểm tra trạng thái đăng nhập để hiển thị trang đăng nhập hoặc trang chính
if st.session_state.is_logged_in:
    show_main_page()
else:
    show_login_page()
