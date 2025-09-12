import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime, date


def main():

    df_total = liga("data_ligas.csv")
    df = df_total.data()

    st.set_page_config(
        page_title="Pronósticos de Ligas del Mundo - SistGoy", layout="wide", page_icon="🏠",)
    st.title("Pronósticos Deportivos ⚽")
    st.markdown("---")

    fecha = st.date_input("Selecciona la Fecha para Pronosticar",
                          date.today(), format="DD.MM.YYYY", width=250)

    dfecha = df.filter(pl.col("Fecha") ==
                       fecha.strftime("%d.%m.%Y")).sort("Liga")

    ld = dfecha['Liga'].unique().sort().to_list()

    with st.expander("Ligas de Futbol ⚽:", expanded=True):

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Estadisticas Resultados", "🎯 Precisión del Modelo :", "📋 Detalle de Pronosticos Combinados", "🎯 Precisión del Modelo"])
        with tab1:
            data = pl.DataFrame({
                "Liga": ld,
                "Estado": [df_total.completado(liga) for liga in ld],
                "% Progreso": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga)*100, '.2f')+"%" for liga in ld],
                "% Victoria Local": [format(df_total.totalvictorias(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in ld],
                "% Empate": [format(df_total.totalempates(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in ld],
                "% Victoria Visita": [format(df_total.totalperdidas(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in ld],
                "Media de Goles": [format(df_total.medialiga(liga), '.2f') for liga in ld],
                "% AEM": [format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in ld],
                "% +2.5 GLS": [format(df_total.liga25(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in ld],
                

            })

            event = st.dataframe(
                data,
                on_select='rerun',
                selection_mode='single-row',
            )

            if len(event.selection['rows']):
                selected_row = event.selection['rows'][0]
                ligas = data[selected_row, 'Liga']

        with tab2:
            if len(event.selection['rows']):
                precision_modelo = df_total.precision_modelo(ligas)
                st.dataframe(precision_modelo, use_container_width=True)

    if len(event.selection['rows']):

        with st.expander("Encuentros de la "+ligas+" ⚽:", expanded=True):

            df_final = dfecha.filter(pl.col("Liga") == ligas)

            event = st.dataframe(
                df_final,
                on_select='rerun',
                selection_mode='single-row'

            )

            if len(event.selection['rows']):
                selected_row = event.selection['rows'][0]
                local = df_final[selected_row, 'Local']
                visita = df_final[selected_row, 'Visita']

            if len(event.selection['rows']):
                st.markdown(
                    f"### Pronóstico para: {local} vs {visita})")
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📊 Resumen", "📋 Detalle de Pronósticos", "📋 Detalle de Pronosticos Combinados", "🎯 Precisión del Modelo"])
                with tab1:
                    with st.expander("Probabilidades de Resultado ( 1-X-2 ) ⚽:", expanded=True):
                        prob_local = df_total.VictoriaLocal(
                            ligas, local, visita)*100
                        prob_empate = df_total.EmpateResultado(
                            ligas, local, visita)*100
                        prob_visitante = df_total.VictoriaVisita(
                            ligas, local, visita)*100

                        cuota_local = 100 / prob_local if prob_local > 0 else 0
                        cuota_empate = 100 / prob_empate if prob_empate > 0 else 0
                        cuota_visitante = 100 / prob_visitante if prob_visitante > 0 else 0

                        col1, col2, col3 = st.columns(3)
                # ``````
                        with col1:
                            pass
                            

if __name__ == "__main__":
    main()
