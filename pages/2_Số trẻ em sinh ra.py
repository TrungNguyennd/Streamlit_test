import streamlit as st
import pandas as pd
import plotly.express as px
import json
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# File: file1.py
from db_connection import connect_to_database, query_data, close_connection

# Kết nối đến cơ sở dữ liệu
conn = connect_to_database()

st.set_page_config(layout="wide")

st.title("CHI CỤC DÂN SỐ - KẾ HOẠCH HÓA GIA ĐÌNH")
st.info("Số trẻ em sinh ra theo quận/huyện")

json1 = f"states_india.geojson"
# Query SQL để lấy dữ liệu từ bảng
query = "SELECT * FROM so_tre_em_sinh_ra;"
df = query_data(conn, query)



# Xây dựng bảng theo quận huyện và năm
table = pd.pivot_table(df, values='indicator_value', index='district', columns='year', aggfunc='first')

# Hiển thị bảng trong Streamlit
st.table(table)


## Widget để chọn năm
selected_year = st.selectbox('Chọn Năm', df['year'].unique())

# Lọc dữ liệu theo năm được chọn
filtered_df = df[df['year'] == selected_year]

# Chia layout thành hai cột
col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
with col1:
    st.info("Biểu đồ số trẻ sinh ra theo Quận/Huyện")
    # Tạo biểu đồ cột dọc sử dụng Plotly Express
    fig = px.bar(filtered_df, x='district', y='indicator_value',
                 labels={'indicator_value': 'Số trẻ sinh ra', 'Quận Huyện': 'Quận/Huyện'})
    # Chuyển tên trục x và y sang tiếng Việt
    fig.update_layout(xaxis_title='Quận/Huyện', yaxis_title='Số trẻ sinh ra')
    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig)

# Đặt nội dung vào cột 2
with col2:
    st.info("Bản đồ số trẻ sinh ra theo Quận/Huyện")
    # Chuyển đến Việt Nam
m = folium.Map(location=[14.0583, 108.2772], tiles='CartoDB positron', name="Light Map",
               zoom_start=5, attr="My Data attribution")


# Query SQL để lấy dữ liệu từ bảng
query = "SELECT * FROM so_tre_em_sinh_ra;"
india_covid_data = query_data(conn, query)

choice = ['indicator_value']
choice_selected = st.selectbox("Select choice", choice)

# Tạo bản đồ với dữ liệu được lọc
if choice_selected is not None:
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
folium.features.GeoJson('states_india.geojson',
                        name="States", popup=folium.features.GeoJsonPopup(fields=["name"])).add_to(m)
# Hiển thị bản đồ trong Streamlit
with col2:
    folium_static(m)
