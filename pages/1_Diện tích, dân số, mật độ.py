import streamlit as st
import pandas as pd
import plotly.express as px
import json
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


st.set_page_config(layout="wide")

# File: file1.py
from db_connection import connect_to_database, query_data, close_connection

# Kết nối đến cơ sở dữ liệu
conn = connect_to_database()

st.title("CHI CỤC DÂN SỐ - KẾ HOẠCH HÓA GIA ĐÌNH")
st.info("Diện tích dân số, mật độ dân số đơn vị hành chính")

# Query SQL để lấy dữ liệu từ bảng
query = "SELECT * FROM dientich_danso_matdo;"
df = query_data(conn, query)
# st.dataframe(df)
df['indicator_value'] = df['indicator_value'].astype(str).replace("nan", 0)
# Pivot dữ liệu để tạo các cột riêng biệt cho diện tích, dân số và mật độ
df_pivot = df.pivot(index='district', columns='indicator', values='indicator_value')
df_pivot = df_pivot.rename(columns={'dienTich': 'Diện tích', 'danSoTrungBinh': 'Dân số trung bình', 'matDoDanSo': 'Mật độ dân số','soPhuongXa': 'Số phường xã','soThiTran': 'Số thị trấn'})
# df_pivot = df_pivot[['', 'Diện tích', 'Dân số trung bình', 'Mật độ dân số','Số phường xã','Số thị trấn']]
# Hiển thị bảng thông tin
st.table(df_pivot)

col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
with col1:
    st.info("Diện tích theo quận/huyện")
    # Tạo DataFrame từ dữ liệu

# Lọc dữ liệu chỉ lấy thông tin về diện tích
df_dientich = df[df['indicator'] == 'dienTich']

# Tạo biểu đồ bar sử dụng Plotly Express
fig = px.bar(df_dientich, x='district', y='indicator_value')

# Chuyển tên trục x và y sang tiếng Việt
fig.update_layout(
    xaxis_title='Quận/Huyện',
    yaxis_title='Diện tích(km2)'
)
# Đặt góc quay của nhãn trục x
fig.update_xaxes(categoryorder='total descending', tickangle=45)
# Hiển thị biểu đồ trong Streamlit
col1.plotly_chart(fig)

# Đặt nội dung vào cột 2
with col2:
    st.info("Bản đồ theo diện tích(km2)")
     # Dữ liệu mẫu
data = {
    "Quận Huyện": ["Quận 1"],
    "Thông Tin": ["Diện tích"],
    "Value": [200],
}

# Thêm cột 'POLYGON' vào DataFrame
data["POLYGON"] = [
    [(10.765, 106.665), (10.775, 106.665), (10.775, 106.675), (10.765, 106.675)],
    # Thêm các điểm của POLYGON cho Quận 2 và Quận 3 tương ứng
]

# Tạo DataFrame từ dữ liệu
df2 = pd.DataFrame(data)

# Tạo ứng dụng Dash
app = dash.Dash(__name__)

# Giao diện ứng dụng Dash
fig = px.choropleth_mapbox(
    df,
    geojson=df2["POLYGON"],
    locations=df2["Quận Huyện"],
    color=df2["Value"],
    mapbox_style="carto-positron",
    zoom=12,
    center={"lat": 10.770, "lon": 106.670},
    opacity=0.5,
    labels={"Value": "Diện Tích"},
)

# Hiển thị bản đồ
col2.plotly_chart(fig)

  

col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
with col1:
    st.info("Mật độ dân số theo quận/huyện")
    # Tạo DataFrame từ dữ liệu

# Lọc dữ liệu chỉ lấy thông tin về diện tích
df_matdo = df[df['indicator'] == 'matDoDanSo']

# Tạo biểu đồ bar sử dụng Plotly Express
fig = px.bar(df_matdo, x='district', y='indicator_value',color_discrete_sequence=['green'] * len(df_matdo),)

# Chuyển tên trục x và y sang tiếng Việt
fig.update_layout(
    xaxis_title='Quận/Huyện',
    yaxis_title='Mật độ'
)
# Đặt góc quay của nhãn trục x
fig.update_xaxes(categoryorder='total descending', tickangle=45)
# Hiển thị biểu đồ trong Streamlit
col1.plotly_chart(fig)

# Đặt nội dung vào cột 2
with col2:
    st.info("Bản đồ mật độ dân số")
    # Giao diện ứng dụng Dash
fig = px.choropleth_mapbox(
    df,
    geojson=df2["POLYGON"],
    locations=df2["Quận Huyện"],
    color=df2["Value"],
    mapbox_style="carto-positron",
    zoom=12,
    center={"lat": 10.770, "lon": 106.670},
    opacity=0.5,
    labels={"Value": "Diện Tích"},
)

# Hiển thị bản đồ
col2.plotly_chart(fig)

col1, col2 = st.columns(2)

# Đặt nội dung vào cột 1
with col1:
    st.info("Dân số theo quận/huyện")
    # Tạo DataFrame từ dữ liệu

# Lọc dữ liệu chỉ lấy thông tin về diện tích
df_danso = df[df['indicator'] == 'danSoTrungBinh']

# Tạo biểu đồ bar sử dụng Plotly Express
fig = px.bar(df_danso, x='district', y='indicator_value' )

# Chuyển tên trục x và y sang tiếng Việt
fig.update_layout(
    xaxis_title='Quận/Huyện',
    yaxis_title='Dân số'
)
# Đặt góc quay của nhãn trục x
fig.update_xaxes(categoryorder='total descending', tickangle=45)
# Hiển thị biểu đồ trong Streamlit
col1.plotly_chart(fig)

# Đặt nội dung vào cột 2
with col2:
    st.info("Bản đồ dân số")   
    # Giao diện ứng dụng Dash
fig = px.choropleth_mapbox(
    df,
    geojson=df2["POLYGON"],
    locations=df2["Quận Huyện"],
    color=df2["Value"],
    mapbox_style="carto-positron",
    zoom=12,
    center={"lat": 10.770, "lon": 106.670},
    opacity=0.5,
    labels={"Value": "Diện Tích"},
)

# Hiển thị bản đồ
col2.plotly_chart(fig) 
  

# Đóng kết nối đến cơ sở dữ liệu
close_connection(conn)
