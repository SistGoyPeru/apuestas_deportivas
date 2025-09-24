import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime, date
#------------------------------------

def main():
   

    df_total = liga("data_ligas.csv")
    df = df_total.data()
    
    #--------------------

    st.set_page_config(
        page_title="Pronósticos de Ligas del Mundo - SistGoy", layout="wide", page_icon="🏠",)
    st.title("Pronósticos Deportivos ⚽")
    st.markdown("---")

    fecha = st.date_input("Selecciona la Fecha para Pronosticar",
                          date.today(), format="DD.MM.YYYY", width=250)

    data_filtro_fecha = df.filter(
        pl.col("Fecha") == fecha.strftime("%d.%m.%Y")).sort("Liga")

    Ligas_Fecha = data_filtro_fecha['Liga'].unique().sort().to_list()

    with st.expander("Ligas por Fechas de Futbol ⚽:", expanded=True):
        data = pl.DataFrame({
            "Liga": Ligas_Fecha,
            "% Progreso Disputado": [format(df_total.totaldisputados(liga)/df_total.TotalEncuentrosLiga(liga), '.2%') for liga in Ligas_Fecha],
            "Media de Goles": [format(df_total.medialiga(liga), '.2f') for liga in Ligas_Fecha],
            "% AEM": [format(df_total.AEM(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in Ligas_Fecha],
            "% +0.5": [format(df_total.liga05(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in Ligas_Fecha],
            "% +1.5": [format(df_total.liga15(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in Ligas_Fecha],
            "% +2.5": [format(df_total.liga25(liga)/df_total.totaldisputados(liga)*100, '.2f')+"%" for liga in Ligas_Fecha],
        })

        event = st.dataframe(
            data,
            on_select='rerun',
            selection_mode='single-row',
        )

    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        ligas = data[selected_row, 'Liga']

        

        precision_modelo = df_total.precision_modelo(ligas)
        

        with st.expander("Encuentros de la "+ligas, expanded=True):
            df_final = data_filtro_fecha.filter(pl.col("Liga") == ligas)
# ´´´´
            event = st.dataframe(
                df_final,
                on_select='rerun',
                selection_mode='single-row'

            )
            if event.selection['rows']:
                selected_row = event.selection['rows'][0]
                local = df_final[selected_row, 'Local']
                visita = df_final[selected_row, 'Visita']
                liga_E = df_final[selected_row, 'Liga']
                
                

            if len(event.selection['rows']):

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(local)

                    Elocal = pl.DataFrame({
                        "Local": [
                            "PPP General",
                            "PPP Local",
                            "% Victoria Local",
                            "% Empate Local",
                            "% Perdida Local",
                            "% AEM Local",
                            "% +0.5 Local",
                            "% +1.5 Local",
                            "% +2.5 Local",



                        ],

                        "Valor": [[format(df_total.PPP(liga_E,local), '.2f')],
                                  [format(df_total.PPP_local(liga_E, local), '.2f')],
                                  [format(df_total.TotalVictoriasEquipoLocal(liga_E, local)/df_total.TotalDisputadosEquipoLocal(liga_E, local)*100, '.2f')+"%"if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],
                                  [format(df_total.TotalEmpatesEquipoLocal(liga_E, local)/df_total.TotalDisputadosEquipoLocal(
                                      liga_E, local)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],
                                  [format(df_total.TotalPerdidasEquipoLocal(liga_E, local)/df_total.TotalDisputadosEquipoLocal(
                                      liga_E, local)*100, '.2f')+"%"if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],

                                  [format(df_total.AEMLocal(liga_E, local)/df_total.TotalDisputadosEquipoLocal(liga_E, local)
                                          * 100, '.2f')+"%" if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],
                                  [format(df_total.liga05Local(liga_E, local)/df_total.TotalDisputadosEquipoLocal(
                                      liga_E, local)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],
                                  [format(df_total.liga15Local(liga_E, local)/df_total.TotalDisputadosEquipoLocal(
                                      liga_E, local)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],
                                  [format(df_total.liga25Local(liga_E, local)/df_total.TotalDisputadosEquipoLocal(
                                      liga_E, local)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoLocal(liga_E, local) > 0 else "0.00%"],


                                  ]


                    })
                    st.dataframe(Elocal)

                with col2:
                    st.subheader(visita)

                    EVisita = pl.DataFrame({
                        "Visita": [
                            "PPP General",
                            "PPP Visita",
                            "% Victoria Visita",
                            "% Empate Visita",
                            "% Perdida Visita",
                            "% AEM Visita",
                            "% +0.5 Visita",
                            "% +1.5 Visita",
                            "% +2.5 Visita"

                        ],

                        "Valor": [[format(df_total.PPP(ligas, visita), '.2f')],
                                  [format(df_total.PPP_visita(ligas, visita), '.2f')],
                                  [format(df_total.TotalVictoriasEquipoVisita(ligas, visita)/df_total.TotalDisputadosEquipoVisita(ligas, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(ligas, visita) > 0 else "0.00%"],
                                  [format(df_total.TotalEmpatesEquipoVisita(ligas, visita)/df_total.TotalDisputadosEquipoVisita(
                                      ligas, visita)*100, '.2f')+"%" if df_total.TotalEmpatesEquipoLocal(ligas, local) > 0 else "0.00%"],
                                  [format(df_total.TotalPerdidasEquipoVisita(ligas, visita)/df_total.TotalDisputadosEquipoVisita(
                                      ligas, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(ligas, visita) > 0 else "0.00%"],
                                  [format(df_total.AEMVisita(ligas, visita)/df_total.TotalDisputadosEquipoVisita(
                                      ligas, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(ligas, visita) > 0 else "0.00%"],
                                  [format(df_total.liga05Visita(liga_E, visita)/df_total.TotalDisputadosEquipoVisita(
                                      liga_E, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(liga_E, visita) > 0 else "0.00%"],
                                  [format(df_total.liga15Visita(liga_E, visita)/df_total.TotalDisputadosEquipoVisita(
                                      liga_E, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(liga_E, visita) > 0 else "0.00%"],
                                  [format(df_total.liga25Visita(liga_E, visita)/df_total.TotalDisputadosEquipoVisita(
                                      liga_E, visita)*100, '.2f')+"%" if df_total.TotalDisputadosEquipoVisita(liga_E, visita) > 0 else "0.00%"],



                                  ]

                    })
                    st.dataframe(EVisita)
                    
                    
                st.subheader("Pronosticos Encuentro")    
                col1, col2 = st.columns(2)
                with col1:

                    
                    pronostico = pl.DataFrame({
                        "Resultado ( 1-X-2 )": [
                            local+" ( 1 )",
                            "Empate ( X )",
                            visita+" ( 2 )",

                        ],

                        "Valor": [format(df_total.VictoriaLocal(ligas, local, visita)*100, '.2f')+"%",
                                format(df_total.EmpateResultado(
                                    ligas, local, visita)*100, '.2f')+"%",
                                format(df_total.VictoriaVisita(
                                    ligas, local, visita)*100, '.2f')+"%"

                                ],

                        "Cuota": [format(1/df_total.VictoriaLocal(ligas, local, visita), '.2f'),
                                format(
                            1/df_total.EmpateResultado(ligas, local, visita), '.2f'),
                            format(1/df_total.VictoriaVisita(ligas,
                                                            local, visita), '.2f')
                        ],
                        "% Aciertos":[precision_modelo[1,"Valor"],
                                      precision_modelo[2,"Valor"],
                                      precision_modelo[3,"Valor"]
                                      ]

                    })
                    st.dataframe(pronostico)
                with col2:

                    pronostico = pl.DataFrame({
                        "Doble Oportunidad": [
                            local+" ( 1 ) -  Empate ( X )",
                            local+" ( 1 ) - "+visita+" ( 2 )",
                            visita+" ( 2 ) - Empate ( X )",

                        ],

                        "Valor": [format((df_total.VictoriaLocal(ligas, local, visita)+df_total.EmpateResultado(ligas, local, visita))*100, '.2f')+"%",
                                format((df_total.VictoriaLocal(
                                    ligas, local, visita)+df_total.VictoriaVisita(ligas, local, visita))*100, '.2f')+"%",
                                format((df_total.VictoriaVisita(
                                    ligas, local, visita)+df_total.EmpateResultado(ligas, local, visita))*100, '.2f')+"%"

                                ],

                        "Cuota": [format(1/(df_total.VictoriaLocal(ligas, local, visita)+df_total.EmpateResultado(ligas, local, visita)), '.2f'),
                                format(1/(df_total.VictoriaLocal(ligas, local, visita) +
                                            df_total.VictoriaVisita(ligas, local, visita)), '.2f'),
                                format(1/(df_total.VictoriaVisita(ligas, local, visita) +
                                            df_total.EmpateResultado(ligas, local, visita)), '.2f')
                                ],

                    })
                    st.dataframe(pronostico)

            
                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(df_total.predict(ligas, local, visita))
                with col2:
                    st.dataframe(df_total.predictcombinados(
                        ligas, local, visita))


if __name__ == "__main__":
    main()
