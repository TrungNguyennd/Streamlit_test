import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from db_connection import connect_to_database, query_data, close_connection

# Kết nối đến cơ sở dữ liệu
conn = connect_to_database()

st.set_page_config(layout="wide")

json1 = f"states_india.geojson"

# Chuyển đến Việt Nam
m = folium.Map(location=[14.0583, 108.2772], tiles='CartoDB positron', name="Light Map",
               zoom_start=5, attr="My Data attribution")

st.title("CHI CỤC DÂN SỐ - KẾ HOẠCH HÓA GIA ĐÌNH")
st.info("Số trẻ em sinh ra theo quận/huyện")

# Query SQL để lấy dữ liệu từ bảng
query = "SELECT * FROM so_tre_em_sinh_ra;"
india_covid_data = query_data(conn, query)

# Chọn năm
selected_year = st.selectbox("Select year", sorted(india_covid_data['year'].unique()))

# Lọc dữ liệu theo năm đã chọn
filtered_data = india_covid_data[india_covid_data['year'] == selected_year]

choice = ['indicator_value']
choice_selected = st.selectbox("Select choice", choice)

# Tạo bản đồ với dữ liệu được lọc
if choice_selected is not None:
    geojson = folium.features.GeoJson(json1)
    geojson.add_child(folium.Popup())
    geojson.add_to(m)

    folium.Choropleth(
        geo_data=json1,
        name="choropleth",
        data=india_covid_data,
        columns=["districtid", choice_selected],
        key_on="feature.districid",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=choice_selected
    ).add_to(m)
    folium.features.GeoJson(json1, name="popup_info",
                            style_function=lambda x: {'color': 'transparent', 'fillColor': 'transparent'},
                            tooltip=folium.features.GeoJsonTooltip(fields=['districtid', choice_selected],
                                                                     aliases=['District', 'Indicator Value'],
                                                                     labels=True,
                                                                     sticky=True)).add_to(m)

# Hiển thị bản đồ trong Streamlit
folium_static(m)

# Đóng kết nối cơ sở dữ liệu
close_connection(conn)
