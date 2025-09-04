import streamlit as st
from clases import liga

def main():
  df_total=liga("data_ligas.csv")
  st.set_page_config(layout="wide", page_title="Pronósticos de Ligas del Mundo - SistGoy")

  st.title("Dashboard de Pronósticos Deportivos ⚽")
  
  
  

if __name__ == "__main__":
  main()
