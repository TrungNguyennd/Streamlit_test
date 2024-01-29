import streamlit as st
from streamlit_lottie import st_lottie
import json

# Tạo một session state để lưu trạng thái đăng nhập
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

def login(username, password):
    # Thực hiện xác thực đơn giản (có thể cần thay đổi)
    if username == "admin" and password == "admin":
        st.session_state.is_logged_in = True
        return True
    else:
        return False

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Cấu hình trang để chiếm toàn bộ màn hình
st.set_page_config(layout="wide")

# Trang đăng nhập
def show_login_page():
    st.title("Đăng nhập")

    # Hiển thị các ô nhập liệu và nút đăng nhập
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    login_button = st.button("Đăng nhập")

    # Xử lý sự kiện khi nút đăng nhập được nhấn
    if login_button:
        if login(username, password):
            st.success("Đăng nhập thành công!")
            st.session_state.is_logged_in = True        
            # Tải lại ứng dụng để hiển thị trang chính
            st.experimental_rerun()
        else:
            st.error("Đăng nhập không thành công. Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.")

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

# Kiểm tra trạng thái đăng nhập để hiển thị trang đăng nhập hoặc trang chính
if st.session_state.is_logged_in:
    # Nếu đã đăng nhập, hiển thị trang chính
    show_main_page()
else:
    # Nếu chưa đăng nhập, hiển thị trang đăng nhập
    show_login_page()
