  # the data is local but it might better to cache it
@st.cache_data
def get_data():
    df_w = query_data(conn, query)

    # In danh sách các tên cột để kiểm tra xem "Unnamed: 0" có trong đó hay không
    print("Column names:", df_w.columns.tolist())

    # Kiểm tra xem cột "Unnamed: 0" có tồn tại trong DataFrame hay không
    if 'Unnamed: 0' in df_w.columns:
        df_w = df_w.drop(columns=['Unnamed: 0'])

    return df_w

# Gọi hàm để xem thông tin cột
get_data()

# set dataframes, and countries list
df_w = get_data()

# initialise the year if not already set
if 'year' not in st.session_state:
    st.session_state['year'] = 2021



#
# Define layout
#
# header bar 
# - contains header text in the first and the global emissions for the selected year
colh1, colh2 = st.columns((4,2))
colh1.markdown("## Global CO2 Emissions")
colh2.markdown("")  # this will be overwritten in the app

# body columns
# - the first column contains the map of global emissions
# - the second column contains graphs for emissions from selected countries 
col1, col2 = st.columns ((8,4))

#
# App logic
#

# define parameters for map graphic
col = 'indicator_value'    # the column that contains the emissions data
max = df_w[col].max()       # maximum emissions value for color range
min = df_w[col].min()       # minimum emissions value for color range

# define the year range for the slider
# to get the whole range replace 1950 with the comment that follows it
first_year = 2018 #df_total['Year'].min()
last_year = df_w['year'].max()

# The first body column contains the map
with col1:
    # get the year with a slider
    st.session_state['year'] = st.slider('Select year',first_year,last_year, key=col)

    # set projection
    p = 'equirectangular'   # default projection

    # create the maps
    fig1 = px.scatter_geo(df_w[df_w['year']==st.session_state['year']], 
                        locations="districtid",       # The ISO code for the Entity (country)
                        color=col,              # color is set by this column
                        size=col,               # size of the scatter dot mirrors the color
                        hover_name="district",    # hover name is the name of the Entity (country)
                        range_color=(min,max),  # the range of values as set above
                        scope= 'world',         # a world map - the default
                        projection=p,           # the project as set above
                        title='indicator_value',
                        template = 'plotly_dark',
                        color_continuous_scale=px.colors.sequential.Reds
                        )
    fig1.update_layout(margin={'r':0, 't':0, 'b':0, 'l':0})  # maximise the figure size
    fig2 = px.choropleth(df_w[df_w['year']==st.session_state['year']], 
                        locations="indicator",       # The ISO code for the Entity (country)
                        color=col,              # color is set by this column
                        hover_name="districtid",    # hover name is the name of the Entity (country)
                        range_color=(min,max),  # the range of values as set above
                        scope= 'world',         # a world map - the default
                        projection=p,           # the project as set above
                        title='indicator_value',
                        template = 'plotly_dark',
                        color_continuous_scale=px.colors.sequential.Reds
                        )
    fig2.update_layout(margin={'r':0, 't':0, 'b':0, 'l':0})  # maximise the figure size
    
    map = st.radio(
    "Choose the map style",
    ["Scatter", "Choropleth"], horizontal = True)
    fig = fig1 if map == 'Scatter' else fig2

    # plot the map
    st.plotly_chart(fig, use_container_width=True)

# set the header with the new year data
emissions = df_w[df_w['year']==st.session_state['year']]['indicator_value']