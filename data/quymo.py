import pandas as pd
import pydeck as pdk
import streamlit as st
import math
import json
import plotly.graph_objects as go
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
            """, unsafe_allow_html=True)
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
    height=400,
)
# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)
df_reshaped = pd.read_csv('data/us-population-2010-2019-reshaped.csv')
def load_data(selected_year):
    col = st.columns((1.5, 4.5, 2), gap='medium')
    
    with col[0]:
        st.markdown('#### Dân số tự nhiên')
        df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)
        first_state_name = df_population_difference_sorted.states.iloc[0]
        first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
        first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
        st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)
        last_state_name = df_population_difference_sorted.states.iloc[-1]
        last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
        last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
        st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)
    
    with col[1]:
        st.markdown('#### Bản đồ dân số trung bình') 
        st.pydeck_chart(map_deck)
        with col[2]:
            st.markdown('#### Tốc độ tăng bình quân (%)')
            
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



    # Tạo một hàng mới cho "Phần Tử 4"
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Bảng dữ liệu dân số tăng tự nhiên")
        # Thêm các thành phần của bố cục 2 ở đây
        file_path = "data/1.2.csv"
    df = pd.read_csv(file_path)

# Chuyển DataFrame thành chuỗi HTML
    html_table = df.style.set_table_styles([{'selector': 'thead tr th', 'props': 'position: sticky; top: 0; background-color: #323538;'}]).render()


# Hiển thị DataFrame với thanh cuộn chiều dọc
    col1.markdown(
    f"""
    <div style="max-height: 450px; overflow-y: auto; width:700px;">
        {html_table}
    """,
    unsafe_allow_html=True
   )

    with col2:
        st.markdown("#### Biểu đồ biến động dân số theo quận/huyện")
        file_path = "data/1.2.csv"
        df = pd.read_csv(file_path)

# Sắp xếp DataFrame theo cột "2023"
        df_sorted = df.sort_values(by="2023")
# Tạo biểu đồ cột
        fig = px.bar(df_sorted, x="Tên đơn vị", y="2023", text="2023",
             labels={"Tên đơn vị": "Quận/Huyện", "2023": "Tốc độ tăng dân số tự nhiên"},
             height=500)
        # Đặt góc nghiêng của chữ trên trục x
        fig.update_layout(xaxis_tickangle=-45)

# Hiển thị biểu đồ trong Streamlit
    col2.plotly_chart(fig, use_container_width=True)
    



