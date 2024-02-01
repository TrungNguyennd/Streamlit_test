import pandas as pd
import pydeck as pdk
import streamlit as st
import math
import json
import plotly.graph_objects as go
import altair as alt


DATA_URL = "states_india.geojson"
json = pd.read_json(DATA_URL)

data2 = {
    "districid": [1,2,3,4,5,6,7,8,9,16,17,18,19,20,21,250,268,269,271,272,273,274,275,276,277,277,278,279,280,281,282],
    "indicator": ['dienTich','dienTich', 'dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich', 'dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich', 'dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich','dienTich',],
    "indicator_value": [200000, 300000,4000,70000,80000,65201,87520,20000,10000,15200,84203,200000, 300000,70000,80000,65201,87520,20000,10000,15200,84203,200000, 300000,70000,80000,65201,87520,20000,10000,15200,84203],
    "year": [2022, 2022,2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022,2022, 2022]
}

        # Duyệt qua các feature trong json
for feature in json["features"]:
    districid = feature["properties"]["districid"]
    
    # Tìm vị trí của districid trong data2["districid"]
    index = data2["districid"].index(districid)
    
    # Thêm giá trị dienTich vào properties của feature
    feature["properties"]["dienTich"] = data2["indicator_value"][index]

df_JSON = pd.DataFrame()


# Custom color scale
COLOR_RANGE = [
    [65, 182, 196],
    [127, 205, 187],
    [199, 233, 180],
    [255, 255, 204],
    [252, 78, 42],
]
max_dienTich = json["features"].apply(lambda row: row["properties"]["dienTich"]).max()

# Tính giá trị của BREAKS tùy thuộc vào giá trị tối đa của dienTich
BREAKS = [max_dienTich * i / 5 for i in range(1, 6)]

def calculate_elevation(val):
    return math.sqrt(val) * 10

# Parse the geometry out in Pandas
df_JSON["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
df_JSON["name"] = json["features"].apply(lambda row: row["properties"]["name"])
df_JSON["dienTich"] = json["features"].apply(lambda row: row["properties"]["dienTich"])
df_JSON["elevation_dienTich"] = json["features"].apply(lambda row: calculate_elevation(row["properties"]["dienTich"]))

# Tính toán giá trị màu sắc tương ứng cho dienTich
def get_fill_color_dienTich(value):
    for i, b in enumerate(BREAKS):
        if value < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[-1]

df_JSON["fill_color_dienTich"] = df_JSON["dienTich"].apply(get_fill_color_dienTich)
# Set up PyDeck for PolygonLayer with Tooltip
polygon_layer = pdk.Layer(
    "PolygonLayer",
    df_JSON,
    id="geojson_dienTich",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    wireframe=True,
    get_elevation="elevation_dienTich",
    get_fill_color="fill_color_dienTich",
    get_line_color=[255, 255, 255],
    elevation_scale=0, 
    extruded=False, 
    pickable=True,
)
tooltip = {"html": "<b>Dân số trung bình:</b> {dienTich} <br /><b>Quận/huyện:</b> {name}"}

# Set up PyDeck for Map with the PolygonLayer
map_deck = pdk.Deck(
    layers=[polygon_layer],
     tooltip=tooltip,
    initial_view_state=pdk.ViewState(
        latitude=21.0285, longitude=105.8542, zoom=8, maxZoom=16, pitch=0.0, bearing=0
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


def load_data(selected_year):
  st.markdown(f"")

    # Bổ sung code xử lý dữ liệu cho quy mô dân số ở đây
col = st.columns((1.5, 4.5, 2), gap='medium')
with col[0]:
    st.markdown('#### Dân số tự nhiên')
    data2 = {
    "district": [1, 2, 3, 4, 1, 2],
    "indicator": ['dienTich', 'danSoTrungBinh', 'matDoDanSo', 'soPhuongXa', "dienTich", "danSoTrungBinh"],
    "indicator_value": [200000.0, 500000.0, 4.8, 123456.0, 500, 600],
    "year": [2022, 2020, 2022, 2022, 2022, 2022]
   }

    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame(data2)

    # Lọc dữ liệu cho năm 2022
    df_2022 = df[df['year'] == 2022]

    # Tính tổng của từng chỉ số
    tong_dienTich = df_2022[df_2022['indicator'] == 'dienTich']['indicator_value'].sum()
    tong_danSoTrungBinh = df_2022[df_2022['indicator'] == 'danSoTrungBinh']['indicator_value'].sum()
    # Tạo biểu đồ số lớn với 4 ô vuông trên mỗi hàng
    fig = go.Figure()

    # Thêm ô vuông cho Diện Tích
    fig.add_trace(go.Indicator(
    mode="number",
    value=tong_dienTich,
    title="Dân số trung bình",
    domain={'row': 0, 'column': 0},
    number={'suffix': ' Người/km2'},
    gauge={'axis': {'visible': False}},
    
  ))

    # Cấu hình layout để chia đều thành 4 ô trên mỗi hàng
    fig.update_layout(grid={'rows': 1, 'columns': 4}, height=200)

    # Đặt màu cho ô vuông
    fig.update_layout(
    template="plotly_dark",
    margin=dict(l=0, r=0, b=0, t=0),
    showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=False)
with col[1]:
    st.markdown('#### Bản đồ dân số tự nhiên')
    st.pydeck_chart(map_deck)
  
    

with col[2]:
    st.markdown('#### Tốc Độ tự nhiên (%)')
       # Dữ liệu mẫu
    data = {
    "Quận/Huyện": ["Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ"],
    "2022": [1.5, 2.0, 1.8, 1.2, 0.5],
    "2021": [1.6, 1.8, 1.7, 1.1, 0.6],  
    }

    df = pd.DataFrame(data)
# Tạo biểu đồ đường
    fig = go.Figure()

    for quan_huyen in df["Quận/Huyện"]:
     fig.add_trace(go.Scatter(
        x=df.columns[1:],
        y=df[df["Quận/Huyện"] == quan_huyen].iloc[0, 1:],
        mode='lines+markers',
        name=quan_huyen
    ))
# Cài đặt layout của biểu đồ
    fig.update_layout(
    xaxis_title='Năm',
    yaxis_title='Tốc Độ Tăng Bình Quân (%)',
    legend=dict(title='Quận/Huyện'),
    )

# Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig, use_container_width=True, height=400)


  # Đọc dữ liệu từ tệp CSV
file_path = "data/1.2.csv"
df = pd.read_csv(file_path)
st.markdown("#### Bảng liệu dân số tăng tự nhiên")
# Hiển thị bảng trong Streamlit
st.table(df)
if __name__ == "__main__":
    selected_year = 2022  # Bạn có thể thay đổi năm theo ý muốn
    load_data(selected_year)



