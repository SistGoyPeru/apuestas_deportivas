import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime, date
import polars as pl
import pandas as pd



def main():

    

    df_total = liga("data_ligas.csv")
    df = df_total.data()
    st.set_page_config(page_title="Pronósticos de Ligas del Mundo - SistGoy",layout="wide",page_icon="🏠",)
    
    

    st.title("Pronósticos Deportivos ⚽")
    st.markdown("---")
    
   
    #=================================================================
    
    data=pl.DataFrame({
        "Liga":df_total.ligas(), 
        "Estado":[df_total.completado(liga) for liga in df_total.ligas()],
        "% Progreso": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Local": [format(df_total.totalvictorias(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Empate": [format(df_total.totalempates(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% Victoria Visita": [format(df_total.totalperdidas(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "Media de Goles":[format(df_total.medialiga(liga),'.2f') for liga in df_total.ligas()],
        "% AEM":[format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()],
        "% +2.5 GLS":[format(df_total.liga25(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in df_total.ligas()]
    
    })
    
    with st.expander("Ligas de Futbol ⚽:",expanded=True):  
        
        event = st.dataframe(
            data,
            on_select='rerun',
            selection_mode='single-row',
            
        
        )
        
        if len(event.selection['rows']):
            selected_row = event.selection['rows'][0]
            ligas = data[selected_row, 'Liga']

    if len(event.selection['rows']):
        with st.expander("Equipos de "+ligas+" ⚽:",expanded=True): 
            data_equipos=pl.DataFrame({
                    "Equipos":df_total.equipos_ligas(ligas),
                    "% Victoria Local":[format(df_total.TotalVictoriasEquipoLocal(ligas,local)/df_total.TotalDisputadosEquipoLocal(ligas,local)*100,'.2f')+"%" for local in df_total.equipos_ligas(ligas)],
                    "% Empate Local":[format(df_total.TotalEmpatesEquipoLocal(ligas,local)/df_total.TotalDisputadosEquipoLocal(ligas,local)*100,'.2f')+"%" for local in df_total.equipos_ligas(ligas)],
                    "% Perdida Local":[format(df_total.TotalPerdidasEquipoLocal(ligas,local)/df_total.TotalDisputadosEquipoLocal(ligas,local)*100,'.2f')+"%" for local in df_total.equipos_ligas(ligas)],
                    "% Victoria Visita":[format(df_total.TotalVictoriasEquipoVisita(ligas,visita)/df_total.TotalDisputadosEquipoVisita(ligas,visita)*100,'.2f')+"%" for visita in df_total.equipos_ligas(ligas)],
                    "% Empate Visita":[format(df_total.TotalEmpatesEquipoVisita(ligas,visita)/df_total.TotalDisputadosEquipoVisita(ligas,visita)*100,'.2f')+"%" for visita in df_total.equipos_ligas(ligas)],
                    "% Perdida Visita":[format(df_total.TotalPerdidasEquipoVisita(ligas,visita)/df_total.TotalDisputadosEquipoVisita(ligas,visita)*100,'.2f')+"%" for visita in df_total.equipos_ligas(ligas)],
                    
                    
            
            
            })
            st.dataframe(data_equipos)
           
            
        
                 
                    

            
        
if __name__ == "__main__":  
  main()
