import streamlit as st
from data import *

def judul():
    st.title("😷 Dashboard Covid-19 Indonesia") 
    st.markdown("Selamat datang di dashboard interaktif untuk menganalisis data **Covid-19** di Indonesia.")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])


locations = st.sidebar.multiselect(
    "Pilih Provinsi 📍", 
    ["Aceh", "Bali", "Banten", "Bengkulu", "DKI Jakarta", 
     "Daerah Istimewa Yogyakarta", "Gorontalo", "Jambi", "Jawa Barat", 
     "Jawa Tengah", "Jawa Timur", "Kalimantan Barat", "Kalimantan Selatan", 
     "Kalimantan Tengah", "Kalimantan Timur", "Kalimantan Utara", 
     "Kepulauan Bangka Belitung", "Kepulauan Riau", "Lampung", "Maluku", 
     "Maluku Utara", "Nusa Tenggara Barat", "Nusa Tenggara Timur", 
     "Papua", "Papua Barat", "Riau", "Sulawesi Barat", "Sulawesi Selatan", 
     "Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Utara", "Sumatera Barat", 
     "Sumatera Selatan", "Sumatera Utara"]
)

if menu == "Home":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year, locations) 
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)  
    bar_chart2(df_filtered)  
    map_chart(df_filtered, year) 

elif menu == "Halaman Data":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year, locations)  

def filter_data(df, year, locations=None):
    df = df[df['Year'] == year]  
    if locations:  
        if isinstance(locations, list):  
            df = df[df['Location'].isin(locations)] 
        else:
            raise ValueError("Locations must be a list.")  