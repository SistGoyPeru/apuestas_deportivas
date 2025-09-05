import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime,date

def main():
  df_total=liga("data_ligas.csv")
  df=df_total.data()
  st.set_page_config(page_title="Pronósticos de Ligas del Mundo - SistGoy")

  st.title("Pronósticos Deportivos ⚽")
  st.markdown("---")
  fecha=st.date_input("Selecciona la Fecha para Pronosticar",date.today(),format="DD.MM.YYYY",width=250 )
  dfecha=df.filter(pl.col("Fecha")==fecha.strftime("%d.%m.%Y")).sort("Liga")

  
  ld=dfecha['Liga'].unique().sort() 
  LigasDisponibles=st.selectbox("Liga Para Pronosticar",ld) 
  df_final=dfecha.filter(pl.col("Liga")==LigasDisponibles)

  event=st.dataframe(
        df_final,
        on_select='rerun',
        selection_mode='single-row'

    )
  
  if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        local = df_final[selected_row, 'Local']
        visita = df_final[selected_row, 'Visita']
        
        
        st.badge(local+" vs "+visita,color="gray") 
  
  
  
  

if __name__ == "__main__":
  main()
