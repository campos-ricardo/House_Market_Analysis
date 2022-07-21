#############################
# Dashborad for data visualization using streamlit
# Author: Ricardo Barbosa de Almeida Campos
#############################

## Required Libraries
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px

## Page Configuration

st.set_page_config(layout='wide')


def dashboard_initialization():
    st.title("Dashboard House Rocket")
    st.markdown("Dashboard para visualizacao de Dados referentes ao mercado imobiliario")

    st.header("Data Overview")
    st.markdown("Visualizacao Geral dos dados")

    return None


## Function description
def load_data(url):
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    st.dataframe(df, height=200)

    return df


def statistical_filter_creation(df):
    st.sidebar.title("Filtering Options")
    # Zipcode Filter
    zipcode_filter = st.sidebar.multiselect("Zipcode Selection", df['zipcode'].unique(),
                                            default=None)

    variable_filter = st.sidebar.multiselect("Variable Selection", df.columns,
                                             default=None)

    return zipcode_filter, variable_filter


def comercial_filter_creation(df):
    st.sidebar.title("Commercial Options")

    st.sidebar.subheader("Select Minimal Year")
    year_filter = st.sidebar.slider('Year Built', int(df['yr_built'].min()), int(df['yr_built'].max()),
                                    value=int(df['yr_built'].median()))

    st.sidebar.subheader("Select Date")

    med_date = df['date'][int(df.shape[0] / 2)]

    day_filter = st.sidebar.select_slider('Date', df['date'].sort_values(ascending=True), value=med_date)

    min_price = int(df['price'].min())
    max_price = int(df['price'].max())
    avg_price = int(df['price'].mean())

    st.sidebar.subheader("Select Price")
    price_filter = st.sidebar.slider('Maximun Price', min_price, max_price, value=avg_price, step=500)

    return year_filter, day_filter, price_filter


def feature_filter_creation(df):
    st.sidebar.title("Feature Options")

    bedroom_filter = st.sidebar.selectbox('Maximum Number of Bedrooms', sorted(data_frame['bedrooms'].unique()))

    bathroom_filter = st.sidebar.selectbox('Maximum Number of Bathrooms', sorted(data_frame['bathrooms'].unique()))

    floors_filter = st.sidebar.selectbox('Maximum Number of floors', sorted(data_frame['floors'].unique()))

    waterfront_filter = st.sidebar.checkbox('Show only houses with waterfron view')

    return bedroom_filter, bathroom_filter, floors_filter, waterfront_filter


@st.cache(allow_output_mutation=True)
def data_filtering(data, zipcode_filter, variable_filter):
    if (zipcode_filter != []) & (variable_filter != []):
        filtered_df = data.loc[data['zipcode'].isin(zipcode_filter), variable_filter]
    elif (zipcode_filter != []) & (variable_filter == []):
        filtered_df = data.loc[data['zipcode'].isin(zipcode_filter), :]
    elif (zipcode_filter == []) & (variable_filter != []):
        filtered_df = data.loc[:, variable_filter]
    else:
        filtered_df = data.copy()

    return filtered_df


def zipcode_filtering(data, zipcode_filter):
    if (zipcode_filter != []):
        f_df_zipcode = data[data['zipcode'].isin(zipcode_filter)]
    else:
        f_df_zipcode = data.copy()

    return f_df_zipcode


def data_feature(df):
    df['price_sqft_square'] = df['price'] / df['sqft_lot']

    return None


def data_aggregaton(df):
    df1 = df[['zipcode', 'id']].groupby('zipcode').count().reset_index()
    df2 = df[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
    df3 = df[['zipcode', 'sqft_living']].groupby('zipcode').mean().reset_index()
    df4 = df[['zipcode', 'price_sqft_square']].groupby('zipcode').mean().reset_index()

    df_ag1 = df1.merge(df2, how='inner', on='zipcode')
    df_ag2 = df_ag1.merge(df3, how='inner', on='zipcode')
    df_ag3 = df_ag2.merge(df4, how='inner', on='zipcode')

    df_ag3.drop(['id'], axis=1, inplace=True)
    df_ag3.rename(columns={'zipcode': 'ZIPCODE',
                           'price': 'AVERAGE_PRICE', 'sqft_living': 'SQFT_LIVING_AVG',
                           'price_sqft_square': 'PRICE_SQFT_SQUARE'}, inplace=True)

    return df_ag3


def statiscal_analysis_tables(f_df, agg_df):
    c1, c2 = st.columns((1, 1))

    c1.title('Average Values')
    c1.dataframe(f_df, width=800, height=600)

    c2.title('Aggregated Values')
    c2.dataframe(agg_df, width=1200, height=600)

    st.title('Filtered Data Description')
    st.dataframe(f_df.describe(), width=1200)

    return None


def portifolio_density_map(df):
    # df = df.sample(n = 1000)
    m1 = folium.Map(location=[df['lat'].mean(), df['long'].mean()], width="%100", height="%100")
    mCluster = MarkerCluster(name="house density").add_to(m1)

    for index, row in df.iterrows():
        folium.Marker(location=[row['lat'], row['long']],
                      popup="Data:{0} por U${1}. Features: {2}sqft, {3} bedrooms, {4} bathrooms, year built: {5}.".format(
                          row['date'],
                          row['price'], row['sqft_living'], row['bedrooms'], row['bathrooms'], row['yr_built'])).add_to(
            mCluster)

    folium.LayerControl().add_to(m1)

    st.data = st_folium(m1, key='fig1', width=725)


def price_density_map(df, df_price_zip, geofile, column):
    m2 = folium.Map(location=[df['lat'].mean(), df['long'].mean()], width="%100", height="%100")
    geofile = geofile[geofile['ZIP'].isin(df_price_zip['ZIP'].tolist())]

    folium.Choropleth(
        geo_data=geofile,
        data=df_price_zip,
        columns=['ZIP', 'PRICE'],
        key_on='feature.properties.id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='AVG PRICES'
    ).add_to(m2)

    with column:
        st.data = st_folium(m2, key='fig2', width=725)


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile


def print_density_maps(df, geofile):
    # Price Maps
    # c1, c2 = st.columns((1, 1))

    df = df.sample(n=100, random_state=1)

    st.title('Portifolio Density')
    portifolio_density_map(df)

    # c2.title('Price Density')
    # df_price_zip = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    # df_price_zip.columns = ['ZIP', 'PRICE']
    # price_density_map(filtered_df,df_price_zip,geofile,c2)

    return None


def price_varation_lines(df, year_filter, day_filter, price_filter):
    st.title("Commercial Attributes")

    f_year_df = df.loc[df['yr_built'] < year_filter]
    year_df = f_year_df[['price', 'yr_built']].groupby('yr_built').mean().reset_index()
    st.header('Price variation per year')
    fig_3 = px.line(year_df, x='yr_built', y='price')
    st.plotly_chart(fig_3, use_container_width=True)

    st.header('Price Variation per Date')
    f_date_df = df.loc[df['date'] < day_filter]
    date_df = f_date_df[['price', 'date']].groupby('date').mean().reset_index()
    fig_4 = px.line(date_df, x='date', y='price')
    st.plotly_chart(fig_4, use_container_width=True)

    st.header('House Price Distribution')
    f_price_df = df.loc[df['price'] < price_filter]
    fig_5 = px.histogram(f_price_df, x='price', nbins=50)
    st.plotly_chart(fig_5, use_container_width=True)

    return None


def price_feature_distribution(df, bedroom_filter, bathroom_filter, floors_filter, waterfront_filter):
    st.title("Feature Attributes")

    c1, c2 = st.columns(2)
    c1.header('Bedroom Distribution')
    fig_6 = px.histogram(df[df['bedrooms'] < bedroom_filter], x='bedrooms', nbins=15)
    with c1:
        st.plotly_chart(fig_6, use_container_width=True)

    c2.header('Bathroom Distribution')
    fig_7 = px.histogram(df[df['bathrooms'] < bathroom_filter], x='bathrooms', nbins=15)
    with c2:
        st.plotly_chart(fig_7, use_container_width=True)

    c1, c2 = st.columns(2)
    c1.header('Floors Distribution')
    fig_7 = px.histogram(df[df['floors'] < floors_filter], x='floors', nbins=15)
    with c1:
        st.plotly_chart(fig_7, use_container_width=True)

    c2.header('Waterfront Distribution')

    if waterfront_filter:

        df_waterfront = df[df['waterfront'] == 1]

    else:

        df_waterfront = df.copy()

    fig_8 = px.histogram(df_waterfront, x='waterfront', nbins=15)
    with c2:
        st.plotly_chart(fig_8, use_container_width=True)

    return None


def operating_strategy_tables(df):
    c1, c2 = st.columns(2)

    zipcode_price_median = df[['price', 'zipcode']].groupby('price').median().reset_index()
    zipcode_price_median.rename(columns={'price': 'median'}, inplace=True)

    buy_table_analysis = df[['id', 'zipcode', 'price', 'condition', 'waterfront', 'date']]

    buy_median_analysis = buy_table_analysis.join(zipcode_price_median.set_index('zipcode'),
                                                  on='zipcode').drop_duplicates(subset=['id']).sort_values(by=['zipcode'])
    buy_median_analysis['status'] = buy_median_analysis.apply(
        lambda x: 1 if (x['condition'] > 3) & (x['price'] < x['median']) else 0, axis=1)

    buy_median_analysis = buy_median_analysis.loc[buy_median_analysis['status'] == 1, :].copy()

    c1.title("Buying Table")
    c1.dataframe(buy_median_analysis, width=800, height=600)

    sell_table_analysis = buy_median_analysis.copy()
    sell_table_analysis['offset'] = (pd.to_datetime(buy_median_analysis['date']).dt.month * 100 + pd.to_datetime(
        buy_median_analysis['date']).dt.day - 320) % 1300
    sell_table_analysis['season'] = pd.cut(sell_table_analysis['offset'], [0, 300, 602, 900, 1300],
                                           labels=['spring', 'summer', 'autumn', 'winter'], include_lowest=True)

    sell_table_analysis.drop(['offset', 'date'], axis=1, inplace=True)

    sell_table_analysis['sell_price'] = sell_table_analysis.apply(
        lambda x: x['price'] * 1.3 if (x['season'] == 'autum' or x['season'] == 'winter')
                                      & (x['price'] < x['median']) else x['price'] * 1.1, axis=1)

    c2.title("Selling Price Table")
    c2.dataframe(sell_table_analysis, width=800, height=600)

    expected_profit = sum(sell_table_analysis['sell_price'] - sell_table_analysis['price'])

    st.write("The expected profit is: U${}".format(expected_profit))

    return None


## Main Code
if __name__ == "__main__":
    dashboard_initialization()

    data_frame = load_data(r"kc_house_data.csv")
    data_feature(data_frame)

    # url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    # geofile = get_geofile( url )

    zipcode_filter, variable_filter = statistical_filter_creation(data_frame)
    year_filter, day_filter, price_filter = comercial_filter_creation(data_frame)
    bedroom_filter, bathroom_filter, floors_filter, waterfront_filter = feature_filter_creation(data_frame)

    filtered_df = data_filtering(data_frame, zipcode_filter, variable_filter)
    f_df_zipcode = zipcode_filtering(data_frame, zipcode_filter)
    agg_df = data_aggregaton(f_df_zipcode)

    statiscal_analysis_tables(filtered_df, agg_df)
    print_density_maps(filtered_df, 1)
    price_varation_lines(data_frame, year_filter, day_filter, price_filter)
    price_feature_distribution(data_frame, bedroom_filter, bathroom_filter, floors_filter, waterfront_filter)
    operating_strategy_tables(data_frame)
