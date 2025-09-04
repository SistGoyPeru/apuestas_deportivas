import streamlit as st
from clases import liga
from datetime import datetime,date

def main():
  df_total=liga("data_ligas.csv")
  st.set_page_config(page_title="Pronósticos de Ligas del Mundo - SistGoy")

  st.title("Pronósticos Deportivos ⚽")
  st.markdown("---")
  fecha=st.date_input("Selecciona la Fecha para Pronosticar",date.today(),format="DD.MM.YYYY",width=250 )
  
  
  

if __name__ == "__main__":
  main()
