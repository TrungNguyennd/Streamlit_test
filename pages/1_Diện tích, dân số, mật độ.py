# home.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import clickhouse_connect
import pydeck as pdk
from Main import check_password, st

if not check_password():
    st.stop()

# Trang chính sau khi đăng nhập
def show_home_page():
    st.set_page_config(layout="wide")
    st.title("CHI CỤC DÂN SỐ - KẾ HOẠCH HÓA GIA ĐÌNH")
    st.info("Diện tích, dân số, mật độ theo đơn vị hành chính")
    # Query SQL để lấy dữ liệu từ bảng
    client = clickhouse_connect.get_client(host='14.177.238.175', username='vgm', password='vgm123', database='vgm')
    result = client.query('SELECT * from duLieuDanSoHaNoi')
    df = pd.DataFrame(result.result_rows, columns=result.column_names)
    # Chuyển giá trị về số thập phân với 2 chữ số sau dấu phẩy

    df['indicator_value'] = df['indicator_value'].astype(int)
    # Lọc dữ liệu để chỉ lấy thông tin về diện tích và dân số
    df_dulieu = df[df['indicator'].isin(['dienTich', 'matDoDanSo', 'danSoTrungBinh','soPhuongXa','soThiTran'])]
    # Pivot dữ liệu để tạo các cột riêng biệt cho diện tích và dân số
    df_pivot = df_dulieu.pivot(index='district', columns='indicator', values='indicator_value')

    # Đổi tên cột 'Value' thành 'Diện Tích' và 'Dân Số'
    df_pivot = df_pivot.rename(columns={'dienTich': 'Diện tích(km2)', 'danSoTrungBinh': 'Dân số trung bình(1000 người)', 'matDoDanSo': 'Mật độ dân số (Người/km2)','soPhuongXa': 'Số phường xã','soThiTran': 'Số thị trấn'})

    # Hiển thị bộ lọc cho từng cột
    selected_columns = st.multiselect("Chọn cột để hiển thị", df_pivot.columns)

    # Nếu không có cột được chọn, hiển thị tất cả các cột
    if not selected_columns:
     selected_columns = df_pivot.columns

    # Lọc DataFrame theo cột được chọn
    df_filtered = df_pivot[selected_columns]
    df_pivot.index.name = 'Quận/Huyện'
    # Hiển thị bảng thông tin với thanh cuộn
    # Sử dụng CSS để đặt chiều rộng của bảng là 100%
    css = """
    <style>
    table {
        width: 100%;
    }
    </style>
"""

    # Hiển thị bảng thông tin với thanh cuộn
    st.markdown(css, unsafe_allow_html=True)
    st.table(df_filtered)
    # Lọc dữ liệu theo năm được chọn
    df_selected_year = df[df["year"] == 2022]
    # Lọc dữ liệu để chỉ lấy thông tin về diện tích
    df_dientich = df_selected_year[df_selected_year['indicator'] == 'dienTich']
    df_dansotrungbinh = df_selected_year[df_selected_year['indicator'] == 'danSoTrungBinh']
    df_dansomatdo = df_selected_year[df_selected_year['indicator'] == 'matDoDanSo']
    # Tạo biểu đồ cột cho dân số

    fig_danso = px.bar(
    df_dansomatdo,
    x='district',
    y='indicator_value',
    labels={'indicator_value': 'Mật độ dân số(người/km2)', 'district': 'Quận/Huyện','year' :'Năm'},
    hover_data={'year': True},
    color_discrete_sequence=['#66d9c6'],
    category_orders={"district": df_dansomatdo.sort_values("indicator_value")["district"]},  # Sắp xếp theo giá trị của indicator_value
)
    fig_dientich = px.bar(
    df_dientich,
    x='district',
    y='indicator_value',
    labels={'indicator_value': 'Diện tích(km2)', 'district': 'Quận/Huyện','year' :'Năm'},
    hover_data={'year': True},
    color_discrete_sequence=['#66d9c6'],
    category_orders={"district": df_dientich.sort_values("indicator_value")["district"]},  # Sắp xếp theo giá trị của indicator_value
)
    fig_dansotrungbinh = px.bar(
    df_dansotrungbinh,
    x='district',
    y='indicator_value',
    labels={'indicator_value': 'Dân số trung bình (1000người)', 'district': 'Quận/Huyện','year' :'Năm'},
    hover_data={'year': True},
    color_discrete_sequence=['#e1e37d'],
    category_orders={"district": df_dansotrungbinh.sort_values("indicator_value")["district"]},  # Sắp xếp theo giá trị của indicator_value
)
    # Đặt góc quay của nhãn trục x
    fig_dansotrungbinh.update_xaxes(categoryorder='total descending', tickangle=45)
    fig_dientich.update_xaxes(categoryorder='total descending', tickangle=45)
    fig_danso.update_xaxes(categoryorder='total descending', tickangle=45)
    # Load in the JSON data
    DATA_URL = "states_india.geojson"
    json = pd.read_json(DATA_URL)
    df_JSON = pd.DataFrame()
    # Custom color scale
    COLOR_RANGE = [
    [65, 182, 196],
    [127, 205, 187],
    [199, 233, 180],
    [237, 248, 177],
    [255, 255, 204],
    [255, 237, 160],
    [254, 217, 118],
    [254, 178, 76],
    [253, 141, 60],
    [252, 78, 42],
    [227, 26, 28],
    [189, 0, 38],
    [254, 217, 118],
    [254, 178, 76],
    [253, 141, 60],
    [252, 78, 42],
    [227, 26, 28],
    [189, 0, 38],
]
    # Tính giá trị tối đa của dienTich và danSoTrungBinh
    max_dienTich = json["features"].apply(lambda row: row["properties"]["dienTich"]).max()
    max_danSoTrungBinh = json["features"].apply(lambda row: row["properties"]["danSoTrungBinh"]).max()
    max_matDoDanSo = json["features"].apply(lambda row: row["properties"]["matDoDanSo"]).max()

    # Tính giá trị của BREAKS tùy thuộc vào giá trị tối đa của dienTich
    BREAKS = [max_dienTich * i / 10 for i in range(1, 11)]

    def calculate_elevation(val):
     return math.sqrt(val) * 10 
    # Parse the geometry out in Pandas
    df_JSON["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
    df_JSON["dienTich"] = json["features"].apply(lambda row: row["properties"]["dienTich"])
    df_JSON["danSoTrungBinh"] = json["features"].apply(lambda row: row["properties"]["danSoTrungBinh"])
    df_JSON["name"] = json["features"].apply(lambda row: row["properties"]["name"])
    df_JSON["matDoDanSo"] = json["features"].apply(lambda row: row["properties"]["matDoDanSo"])
    df_JSON["elevation_dienTich"] = json["features"].apply(lambda row: calculate_elevation(row["properties"]["dienTich"]))
    df_JSON["elevation_matDoDanSo"] = json["features"].apply(lambda row: calculate_elevation(row["properties"]["matDoDanSo"]))
    df_JSON["elevation_danSoTrungBinh"] = json["features"].apply(lambda row: calculate_elevation(row["properties"]["danSoTrungBinh"]))
    # Tính toán giá trị màu sắc tương ứng cho dienTich
    def get_fill_color_dienTich(value):
     for i, b in enumerate(BREAKS):
        if value < b:
            return COLOR_RANGE[i]
     return COLOR_RANGE[-1]

     df_JSON["fill_color_dienTich"] = df_JSON["dienTich"].apply(get_fill_color_dienTich)
     # Tính toán giá trị màu sắc tương ứng cho danSoTrungBinh
    def get_fill_color_danSoTrungBinh(value):
     return COLOR_RANGE[int((value / max_danSoTrungBinh) * (len(COLOR_RANGE) - 1))]

    df_JSON["fill_color_danSoTrungBinh"] = df_JSON["danSoTrungBinh"].apply(get_fill_color_danSoTrungBinh)

    # Tính toán giá trị màu sắc tương ứng cho matDoDanSo
    def get_fill_color_matDoDanSo(value):
     return COLOR_RANGE[int((value / max_matDoDanSo) * (len(COLOR_RANGE) - 1))]

    df_JSON["fill_color_matDoDanSo"] = df_JSON["matDoDanSo"].apply(get_fill_color_matDoDanSo)
    col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
    with col1:
     st.info("Diện tích theo quận/huyện")


    col1.plotly_chart(fig_dientich)

# Đặt nội dung vào cột 2
    with col2:
     st.info("Bản đồ theo diện tích(km2)")
        # Set up PyDeck
# Set up PyDeck for PolygonLayer with Tooltip
    polygon_layer = pdk.Layer(
     "PolygonLayer",
    df_JSON,
    id="geojson_dienTich",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="elevation_dienTich",
    get_fill_color="fill_color_dienTich",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
)
    tooltip = {"html": "<b>Diện tích(km2):</b> {dienTich} <br /><b>Quận/huyện:</b> {name}"}

# Set up PyDeck for Map with the PolygonLayer
    map_deck = pdk.Deck(
    layers=[polygon_layer],
     tooltip=tooltip,
    initial_view_state=pdk.ViewState(
        latitude=21.0285, longitude=105.8542, zoom=8, maxZoom=16, pitch=45, bearing=0
    ),
    effects=[
        {
            "@@type": "LightingEffect",
            "shadowColor": [0, 0, 0, 0.5],
            "ambientLight": {"@@type": "AmbientLight", "color": COLOR_RANGE[0], "intensity": 1.0},
            "directionalLights": [
                {"@@type": "_SunLight", "timestamp": 1564696800000, "color": COLOR_RANGE[0], "intensity": 1.0, "_shadow": True}
            ],
        }
    ],
)

# Display the map with PyDeck
    col2.pydeck_chart(map_deck)
  

    col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
    with col1:
     st.info("Dân số trung bình theo quận/huyện")
    # Tạo DataFrame từ dữ liệu

    col1.plotly_chart(fig_dansotrungbinh)

# Đặt nội dung vào cột 2
    with col2:
     st.info("Bản đồ dân số trung bình")
   # Set up PyDeck cho danSoTrungBinh
# Set up PyDeck for PolygonLayer with Tooltip
    polygon_layer = pdk.Layer(
    "PolygonLayer",
    df_JSON,
    id="geojson_danSoTrungBinh",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="elevation_danSoTrungBinh",
    get_fill_color="fill_color_danSoTrungBinh",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
)
    tooltip = {"html": "<b>Dân số trung bình(1000 Người):</b> {danSoTrungBinh} <br /><b>Quận/huyện:</b> {name}"}

# Set up PyDeck for Map with the PolygonLayer
    map_deck = pdk.Deck(
    layers=[polygon_layer],
     tooltip=tooltip,
    initial_view_state=pdk.ViewState(
        latitude=21.0285, longitude=105.8542, zoom=8, maxZoom=16, pitch=45, bearing=0
    ),
    effects=[
        {
            "@@type": "LightingEffect",
            "shadowColor": [0, 0, 0, 0.5],
            "ambientLight": {"@@type": "AmbientLight", "color": COLOR_RANGE[0], "intensity": 1.0},
            "directionalLights": [
                {"@@type": "_SunLight", "timestamp": 1564696800000, "color": COLOR_RANGE[0], "intensity": 1.0, "_shadow": True}
            ],
        }
    ],
)

# Display the map with PyDeck
    col2.pydeck_chart(map_deck)


    col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
    with col1:
     st.info("Mật độ dân số(người/km2)theo quận/huyện")
    
# Hiển thị biểu đồ dân số
    col1.plotly_chart(fig_danso)

# Đặt nội dung vào cột 2
    with col2:
     st.info("Bản đồ Mật độ dân số(người/km2)")   
 
# Set up PyDeck cho danSoTrungBinh
# Set up PyDeck for PolygonLayer with Tooltip
    polygon_layer = pdk.Layer(
    "PolygonLayer",
    df_JSON,
    id="geojson_matDoDanSo",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="elevation_matDoDanSo",
    get_fill_color="fill_color_matDoDanSo",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
)
    tooltip = {"html": "<b>Mật độ dân số(người/km2):</b> {matDoDanSo} <br /><b>Quận/huyện:</b> {name}"}

# Set up PyDeck for Map with the PolygonLayer
    map_deck = pdk.Deck(
    layers=[polygon_layer],
     tooltip=tooltip,
    initial_view_state=pdk.ViewState(
        latitude=21.0285, longitude=105.8542, zoom=8, maxZoom=16, pitch=45, bearing=0
    ),
    effects=[
        {
            "@@type": "LightingEffect",
            "shadowColor": [0, 0, 0, 0.5],
            "ambientLight": {"@@type": "AmbientLight", "color": COLOR_RANGE[0], "intensity": 1.0},
            "directionalLights": [
                {"@@type": "_SunLight", "timestamp": 1564696800000, "color": COLOR_RANGE[0], "intensity": 1.0, "_shadow": True}
            ],
        }
    ],
)

# Display the map with PyDeck
    col2.pydeck_chart(map_deck)


# Main Streamlit app starts here
show_home_page()