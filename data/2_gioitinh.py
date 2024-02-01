# Trong quymo.py
import streamlit as st

def main(selected_year):
    st.write(f"Quy mô, phân bố và biến động dân số cho nămddd {selected_year}")
    # Bổ sung code xử lý dữ liệu cho quy mô dân số ở đây

if __name__ == "__main__":
    selected_year = 2022  # Bạn có thể thay đổi năm theo ý muốn
    main(selected_year)
