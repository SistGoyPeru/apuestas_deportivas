import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime, date
import polars as pl




def main():



    df_total = liga("data_ligas.csv")
    df = df_total.data()
    st.set_page_config(page_title="Pronósticos de Ligas del Mundo - SistGoy",layout="wide")

    st.title("Pronósticos Deportivos ⚽")
    st.markdown("---")
    
  

    #=================================================================
    
    data={
        "Liga":df_total.ligas(), 
        "Estado":[df_total.completado(liga) for liga in df_total.ligas()],
        "% Progreso": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Local": [format(df_total.totalvictorias(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Empate": [format(df_total.totalempates(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Visita": [format(df_total.totalperdidas(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "Media de Goles":[format(df_total.medialiga(liga),'.2f') for liga in df_total.ligas()],
        "% AEM":[format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% +2.5 GLS":[format(df_total.liga25(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()]
    
    }
    
    data=pl.DataFrame(data)
    
    event = st.dataframe(
        data,
        on_select='rerun',
        selection_mode='single-row',
        height=200
        
         
        
        
       

    )
    
    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]   

    


if __name__ == "__main__":
    main()
