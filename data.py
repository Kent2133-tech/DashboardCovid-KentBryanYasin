import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

# Filter data berdasarkan tahun dan lokasi
def filter_data(df, year=None, locations=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if locations:
        df = df[df['Location'].isin(locations)]
    return df

def select_location():
    df = load_data()
    location = ['Semua Provinsi'] + sorted(df['Location'].unique())
    return st.sidebar.selectbox(
        "Pilih Provinsi 🏙️",
        options=location
    )

# Select tahun dengan key unik
def select_year(unique_suffix=""):
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else x,
        key=f"select_year_{unique_suffix}"
    )

# Fungsi filter lokasi (multi-select)
def select_locations(df, unique_suffix=""):
    all_locations = df['Location'].dropna().unique().tolist()
    selected_locations = st.sidebar.multiselect(
        "Pilih Provinsi 📍",
        options=sorted(all_locations),
        default=[],
        key=f"select_location_{unique_suffix}"
    )
    return selected_locations

# Tampilkan data
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia 🦠🔴⚪")
    st.dataframe(df_selected.head(10))

# Total kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

def total_death(df):
    total_mati = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_mati['Total Deaths'].sum()

def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

# Tampilkan metrik dalam 3 kolom
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🧪 Total Kasus", value=f"{kasus/1000:.1f}K", delta=None)
    col2.metric(label="⚰️ Total Kematian", value=f"{kematian/1000:.1f}K", delta=None)
    col3.metric(label="💊 Total Sembuh", value=f"{sembuh/1000:.1f}K", delta=None)

# Pie chart kematian vs sembuh
def pie_chart1(df):
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_death(df), total_recovery(df)]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']
    )

    st.plotly_chart(fig, use_container_width=True)

def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title='5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    df['Date'] = pd.to_datetime(df['Date'])

    if year:
        df = df[df['Date'].dt.year == year]

    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return

    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118}, 
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    fig.update_layout(
        mapbox_style="carto-positron",  
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

# Fungsi utama
def main():
    st.title("Dashboard Covid-19 Indonesia 💉🦠")

    df = load_data()
    year = select_year("main")
    selected_locations = select_locations(df, "main")

    filtered_df = filter_data(df, year, selected_locations)

    show_data(filtered_df)
    kolom(filtered_df)
    pie_chart1(filtered_df)

if __name__ == "__main__":
    main()