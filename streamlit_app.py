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
    
    fecha = st.date_input("Selecciona la Fecha para Pronosticar",
                          date.today(), format="DD.MM.YYYY", width=250)
           
    dfecha = df.filter(pl.col("Fecha") ==
                       fecha.strftime("%d.%m.%Y")).sort("Liga")
    
    ld = dfecha['Liga'].unique().sort().to_list()
    
    data=pl.DataFrame({
        "Liga":ld, 
        "Estado":[df_total.completado(liga) for liga in ld],
        "% Progreso": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga)*100,'.2f')+"%" for liga in ld],
        "% Victoria Local": [format(df_total.totalvictorias(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in ld],
        "% Empate": [format(df_total.totalempates(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in ld],
        "% Victoria Visita": [format(df_total.totalperdidas(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in ld],
        "Media de Goles":[format(df_total.medialiga(liga),'.2f') for liga in ld],
        "% AEM":[format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in ld],
        "% +2.5 GLS":[format(df_total.liga25(liga)/df_total.totaldisputados(liga)*100,'.2f')+"%" for liga in ld]
    
    })
    
    
    
    with st.expander("Ligas de Futbol ⚽:",expanded=True):  
        
        event = st.dataframe(
            data,
            on_select='rerun',
            selection_mode='single-row',
            
        
        )

        #=====================================
        
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
            
        with st.expander("Encuentros de la "+ligas+" ⚽:",expanded=True): 
            

            df_final = dfecha.filter(pl.col("Liga") == ligas)
            
            event = st.dataframe(
                df_final,
                on_select='rerun',
                selection_mode='single-row'

            )


        
                 
                    

            
        
if __name__ == "__main__":  
  main()
