# main.py
import streamlit as st
from pathlib import Path
import importlib

st.set_page_config(page_title="Quy mô dân số", layout="wide")

# Tạo từ điển ánh xạ tên danh mục cấp 2 vào tên tệp dữ liệu Python
category_mapping = {
    'Quy mô và tốc độ tăng dân số bình quân': 'quymo',
    'Tốc độ tăng dân số tự nhiên (sinh-tử)': 'tangdan',
    'Tốc độ tăng dân số cơ học (đi-đến)': 'tangdancohoc',
    'Mật độ dân số': 'matdodanso',
    'Số sinh và tỷ suất sinh': 'sosinh',
    'Số sinh 3+ và tỷ lệ sinh 3+': 'sosinh3plus',
    'Cơ cấu về giới tính': '2_gioitinh',
    'Tổng số phụ nữ 15-49 và số phụ nữ 15-49 có chồng': '2_tongphunu',
    'Tổng số phụ nữ 15-49 và phụ nữ 30-49 chưa có chồng': '2_tongchuacochong',
    'Tổng số phụ nữ 15-49 có chồng và phụ nữ 35-49 có chồng có đủ 2 con': '2_tongcochong2con',
    'Dân số là người cao tuổi trên 60 tuổi': '2_dansotren60',
    'Dân số là người cao tuổi trên 60 và 80 tuổi': '2_dansotren80',
    'Tỷ lệ sàng lọc trước sinh': '3_tyle',
    'Tỷ lệ sàng lọc sơ sinh': '3_tylesang',
    'Tỷ số giới tính khi sinh': '3_tysogioitinh',
    'Tỷ lệ Người cao tuổi được khám sức khoẻ định kỳ': '3_tylekhamsk',
    'Tỷ lệ khám sức khoẻ trước khi kết hôn': '3_tylekham',
    'Dự báo dân số': 'du_bao',
}

def get_data_files(selected_category_level_1, selected_category_level_2):
    if selected_category_level_1 == 'Quy mô, phân bố và biến động dân số':
        return [f for f in Path("data").rglob("*.py")]
    else:
        selected_data_file = category_mapping.get(selected_category_level_2, selected_category_level_2)
        return [f"data/{selected_data_file}.py"]

def load_module(selected_category_level_2):
    selected_data_file = category_mapping.get(selected_category_level_2, selected_category_level_2)
    module_name = f"data.{selected_data_file}"
    return importlib.import_module(module_name)

def main():
    # Tạo layout với 2 cột
    col_menu = st.sidebar
    col_content = st

    # Menu bên trái
    col_menu.title('🏂 Atlas dân số Hà Nội')
    col_menu.write('Atlas dân số Hà Nội thể hiện sự phân bố dân số, diện tích, tỷ lệ tăng dân số tự nhiên tỷ lệ sinh, và các chỉ tiêu khác 10 năm từ 2014-2023 tại các quận/huyện thuộc Thành Phố Hà Nội')

    # Dựa trên lựa chọn của người dùng ở cấp 1, hiển thị cấp 2 phù hợp
    selected_category_level_1 = col_menu.selectbox('Chọn nhóm chỉ tiêu', ['Quy mô, phân bố và biến động dân số', 'Cơ cấu dân số', 'Chất lượng dân số'])
    
    selected_category_level_2_options = []
    if selected_category_level_1 == 'Quy mô, phân bố và biến động dân số':
        selected_category_level_2_options = ['Quy mô và tốc độ tăng dân số bình quân','Tốc độ tăng dân số tự nhiên (sinh-tử)','Tốc độ tăng dân số cơ học (đi-đến)','Mật độ dân số','Số sinh và tỷ suất sinh','Số sinh 3+ và tỷ lệ sinh 3+']
    elif selected_category_level_1 == 'Cơ cấu dân số':
        selected_category_level_2_options = ['Cơ cấu về giới tính', 'Tổng số phụ nữ 15-49 và số phụ nữ 15-49 có chồng', 'Tổng số phụ nữ 15-49 và phụ nữ 30-49 chưa có chồng', 'Tổng số phụ nữ 15-49 có chồng và phụ nữ 35-49 có chồng có đủ 2 con', 'Dân số là người cao tuổi trên 60 tuổi', 'Dân số là người cao tuổi trên 60 và 80 tuổi']
    elif selected_category_level_1 == 'Chất lượng dân số':
        selected_category_level_2_options = ['Tỷ lệ sàng lọc trước sinh', 'Tỷ lệ sàng lọc sơ sinh', 'Tỷ số giới tính khi sinh', 'Tỷ lệ Người cao tuổi được khám sức khoẻ định kỳ', 'Tỷ lệ khám sức khoẻ trước khi kết hôn']

    selected_category_level_2 = col_menu.selectbox('Chọn chỉ tiêu', selected_category_level_2_options)

    # Lấy danh sách tệp dữ liệu dựa trên lựa chọn cấp 2
    data_files = get_data_files(selected_category_level_1, selected_category_level_2)

    # Thêm selectbox để chọn năm
    selected_year = col_menu.selectbox('Chọn năm', [2019, 2021, 2022, 2023])

    # Lấy tên tệp dữ liệu Python dựa trên tên danh mục cấp 2
    selected_data_file = category_mapping.get(selected_category_level_2, selected_category_level_2)

    # Import module và gọi hàm xử lý dữ liệu
    selected_module = load_module(selected_category_level_2)
    selected_module.load_data(selected_year)

if __name__ == "__main__":
    main()
