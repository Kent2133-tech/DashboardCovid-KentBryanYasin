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
    return df['Total Cases'].sum()  

# Total kematian
def total_death(df):
    return df['Total Deaths'].sum()

# Total sembuh
def total_recovery(df):
    return df['Total Recovered'].sum()

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