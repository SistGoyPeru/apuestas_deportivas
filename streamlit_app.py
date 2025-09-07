import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime, date


def main():

    colores = {
        "Local": "#28a745",     # Verde para victoria local
        "Empate": "#ffc107",    # Amarillo para empate
        "Visitante": "#dc3545"  # Rojo para victoria visitante
    }

    df_total = liga("data_ligas.csv")
    df = df_total.data()
    st.set_page_config(page_title="Pronósticos de Ligas del Mundo - SistGoy")
    
    #=================================================================
    
    data={
        "Liga":df_total.ligas(), 
        "Estado":[df_total.completado(liga) for liga in df_total.ligas()],
        "% Progreso": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Local": [format(df_total.totalvictorias(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Empate": [format(df_total.totalempates(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Visita": [format(df_total.totalperdidas(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "Media de Goles":[format(df_total.medialiga(liga),'.2f') for liga in df_total.ligas()],
        "% AEM":[format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()]
        
        
        
        
    
    }
    
    data=pl.DataFrame(data)
    
    st.dataframe(data)
    
   
    
    
    
   




if __name__ == "__main__":
    main()
