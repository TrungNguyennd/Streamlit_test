import streamlit as st
import pandas as pd
import plotly.express as px
import json
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import clickhouse_connect
import math
import pydeck as pdk

from Main import check_password, st

if not check_password():
    st.stop()
# Trang chính sau khi đăng nhập
def show_home_page():
 st.set_page_config(layout="wide")

 st.title("CHI CỤC DÂN SỐ - KẾ HOẠCH HÓA GIA ĐÌNH")
 st.info("Tỷ suất chết thô phân theo quận/huyện")

 json1 = f"states_india.geojson"
 client = clickhouse_connect.get_client(host='14.177.238.175', username='vgm', password='vgm123', database='vgm')
 result = client.query('SELECT * from duLieuDanSoHaNoi')
 df = pd.DataFrame(result.result_rows, columns=result.column_names)
 df['indicator_value'] = df['indicator_value'].round(2)
 df['indicator_value'] = df['indicator_value'].astype(str).replace("nan", 0)
 df_selected = df[df['indicator'].isin(['tySuatChetTho'])]
 # Xây dựng bảng theo quận huyện và năm
 df_pivot = df_selected.pivot(index='district', columns='year', values='indicator_value')

 # Hiển thị bảng trong Streamlit
 st.table(df_pivot)
 # Tiện ích lọc theo năm
 selected_year = st.slider("Chọn Năm", min_value=int(df["year"].min()), max_value=int(df["year"].max()), value=int(df["year"].max()))
 # Lọc dữ liệu theo năm được chọn
 df_selected_year = df[df["year"] == selected_year]
 # Lọc dữ liệu để chỉ lấy thông tin về diện tích
 df_tysuat = df_selected_year[df_selected_year['indicator'] == 'tySuatChetTho']
 # Tạo biểu đồ cột cho dân số
 fig_tysuat = px.bar(
    df_tysuat,
    x='district',
    y='indicator_value',
    labels={'indicator_value': 'Tỷ suất chết thô', 'district': 'Quận/Huyện','year' :'Năm'},
    hover_data={'year': True},
    category_orders={"district": df_tysuat.sort_values("indicator_value")["district"]},  # Sắp xếp theo giá trị của indicator_value
 )
 fig_tysuat.update_xaxes(categoryorder='total descending', tickangle=45)
 # Chia layout thành hai cột
 col1, col2 = st.columns(2)

 # Đặt nội dung vào cột 1
 with col1:
    st.info("Biểu đồ Tỷ suất chết thô theo Quận/Huyện")
    col1.plotly_chart(fig_tysuat)

 # Đặt nội dung vào cột 2
 with col2:
    st.info("Bản đồ Tỷ suất chết thô theo Quận/Huyện")
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
 ]
 # Tính giá trị tối đa của tySuatChetTho và danSoTrungBinh
 max_tySuatChetTho = json["features"].apply(lambda row: row["properties"]["tySuatChetTho"]).max()

 # Tính giá trị của BREAKS tùy thuộc vào giá trị tối đa của tySuatChetTho
 BREAKS = [max_tySuatChetTho * i / 10 for i in range(1, 11)]
 
 def calculate_elevation(val):
    return math.sqrt(val) * 10

 # Parse the geometry out in Pandas
 df_JSON["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
 df_JSON["tySuatChetTho"] = json["features"].apply(lambda row: row["properties"]["tySuatChetTho"])
 df_JSON["name"] = json["features"].apply(lambda row: row["properties"]["name"])
 df_JSON["elevation_tySuatChetTho"] = json["features"].apply(lambda row: calculate_elevation(row["properties"]["tySuatChetTho"]))

 # Tính toán giá trị màu sắc tương ứng cho tySuatChetTho
 def get_fill_color_tySuatChetTho(value):
    for i, b in enumerate(BREAKS):
        if value < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[-1]

 df_JSON["fill_color_tySuatChetTho"] = df_JSON["tySuatChetTho"].apply(get_fill_color_tySuatChetTho)
 # Set up PyDeck for PolygonLayer with Tooltip
 polygon_layer = pdk.Layer(
    "PolygonLayer",
    df_JSON,
    id="geojson_tySuatChetTho",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="elevation_tySuatChetTho",
    get_fill_color="fill_color_tySuatChetTho",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
 )
 tooltip = {"html": "<b>Tỷ suất chết thô:</b> {tySuatChetTho} <br /><b>Quận/huyện:</b> {name}"}

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

