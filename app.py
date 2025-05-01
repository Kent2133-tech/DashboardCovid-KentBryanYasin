import streamlit as st
from data import *

# Fungsi judul halaman
def judul():
    st.title("😀 Dashboard Covid-19 Indonesia")
    st.markdown("Selamat datang di dashboard interaktif untuk menganalisis data **Covid-19** di Indonesia 🇮🇩.")

# Sidebar navigasi
st.sidebar.title("🧭 Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

# Load data (sekali saja)
df = load_data()

# Halaman HOME
if menu == "Home":
    judul()
    year = select_year("home")
    selected_locations = select_locations(df, "home")
    df_filtered = filter_data(df, year, selected_locations)
    kolom(df_filtered)
    pie_chart1(df_filtered)

# Halaman DATA
elif menu == "Halaman Data":
    judul()
    year = select_year("data")
    selected_locations = select_locations(df, "data")
    df_filtered = filter_data(df, year, selected_locations)
    show_data(df_filtered)
