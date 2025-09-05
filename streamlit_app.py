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

    st.title("Pronósticos Deportivos ⚽")
    st.markdown("---")
    fecha = st.date_input("Selecciona la Fecha para Pronosticar",
                          date.today(), format="DD.MM.YYYY", width=250)
    dfecha = df.filter(pl.col("Fecha") ==
                       fecha.strftime("%d.%m.%Y")).sort("Liga")

    ld = dfecha['Liga'].unique().sort()
    LigasDisponibles = st.selectbox("Liga Para Pronosticar", ld)
    df_final = dfecha.filter(pl.col("Liga") == LigasDisponibles)

    event = st.dataframe(
        df_final,
        on_select='rerun',
        selection_mode='single-row'

    )

    if len(event.selection['rows']):
        selected_row = event.selection['rows'][0]
        local = df_final[selected_row, 'Local']
        visita = df_final[selected_row, 'Visita']

        st.markdown(
            f"### Pronóstico para: {local} vs {visita} ({LigasDisponibles})")
        tab1, tab2, tab3 = st.tabs(
            ["📊 Resumen", "📋 Detalle de Pronósticos", "🎯 Precisión del Modelo"])
        with tab1:
            with st.expander("Probabilidades de Resultado ( 1-X-2 ) ⚽:", expanded=True):
                prob_local = df_total.VictoriaLocal(
                    LigasDisponibles, local, visita)*100
                prob_empate = df_total.EmpateResultado(
                    LigasDisponibles, local, visita)*100
                prob_visitante = df_total.VictoriaVisita(
                    LigasDisponibles, local, visita)*100

                cuota_local = 100 / prob_local if prob_local > 0 else 0
                cuota_empate = 100 / prob_empate if prob_empate > 0 else 0
                cuota_visitante = 100 / prob_visitante if prob_visitante > 0 else 0

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Local']};">
                        <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Victoria Local</h3>
                        <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Local']}; margin: 5px 0 0 0;">
                            {prob_local:.1f}%
                        </p>
                        <p style="font-size: 1.2rem; margin: 0; color: #777;">
                            Cuota: <span style="font-weight: bold;">{cuota_local:.2f}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Empate']};">
                        <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Empate</h3>
                        <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Empate']}; margin: 5px 0 0 0;">
                            {prob_empate:.1f}%
                        </p>
                        <p style="font-size: 1.2rem; margin: 0; color: #777;">
                            Cuota: <span style="font-weight: bold;">{cuota_empate:.2f}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Visitante']};">
                        <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Victoria Visitante</h3>
                        <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Visitante']}; margin: 5px 0 0 0;">
                            {prob_visitante:.1f}%
                        </p>
                        <p style="font-size: 1.2rem; margin: 0; color: #777;">
                            Cuota: <span style="font-weight: bold;">{cuota_visitante:.2f}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            with st.expander("Ambos Equipos Marcan (BTTS) ⚽:", expanded=True):
                prob_btts_si = df_total.ambosmarcan(
                    LigasDisponibles, local, visita)*100
                prob_btts_no = df_total.solounomarca(
                    LigasDisponibles, local, visita)*100

                cuota_btts_si = 100 / prob_btts_si if prob_btts_si > 0 else 0
                cuota_btts_no = 100 / prob_btts_no if prob_btts_no > 0 else 0

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Local']};">
                        <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Sí</h3>
                        <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Local']}; margin: 5px 0 0 0;">
                            {prob_btts_si:.1f}%
                        </p>
                        <p style="font-size: 1.2rem; margin: 0; color: #777;">
                            Cuota: <span style="font-weight: bold;">{cuota_btts_si:.2f}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Visitante']};">
                        <h3 style="margin: 0; font-size: 1.2rem; color: #555;">No</h3>
                        <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Visitante']}; margin: 5px 0 0 0;">
                            {prob_btts_no:.1f}%
                        </p>
                        <p style="font-size: 1.2rem; margin: 0; color: #777;">
                            Cuota: <span style="font-weight: bold;">{cuota_btts_no:.2f}</span> 
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            with st.expander("Doble oportunidad (1X-X2-12) ⚽:", expanded=True):
                prob_1x = prob_local + prob_empate
                prob_x2 = prob_empate + prob_visitante
                prob_12 = prob_local + prob_visitante

                cuota_1x = 100 / prob_1x if prob_1x > 0 else 0
                cuota_x2 = 100 / prob_x2 if prob_x2 > 0 else 0
                cuota_12 = 100 / prob_12 if prob_12 > 0 else 0

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Local']};">
                            <h3 style="margin: 0; font-size: 1.2rem; color: #555;">1X</h3>
                            <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Local']}; margin: 5px 0 0 0;">
                                {prob_1x:.1f}%
                            </p>
                            <p style="font-size: 1.2rem; margin: 0; color: #777;">
                                Cuota: <span style="font-weight: bold;">{cuota_1x:.2f}</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Empate']};">
                            <h3 style="margin: 0; font-size: 1.2rem; color: #555;">X2</h3>
                            <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Empate']}; margin: 5px 0 0 0;">
                                {prob_x2:.1f}%
                            </p>
                            <p style="font-size: 1.2rem; margin: 0; color: #777;">
                                Cuota: <span style="font-weight: bold;">{cuota_x2:.2f}</span>   
                            </p>

                        </div>
                        """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Visitante']};">
                            <h3 style="margin: 0; font-size: 1.2rem; color: #555;">12</h3>
                            <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Visitante']}; margin: 5px 0 0 0;">
                                {prob_12:.1f}%
                            </p>
                            <p style="font-size: 1.2rem; margin: 0; color: #777;">
                                Cuota: <span style="font-weight: bold;">{cuota_12:.2f}</span> 
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
        with tab2:
            st.markdown("### Detalle de Pronósticos 📋")
            st.markdown(
                "Aquí se muestran las probabilidades detalladas y las cuotas sugeridas para diferentes tipos de apuestas basadas en el análisis histórico de los equipos.")
            detalle = df_total.detallepronosticos(
                LigasDisponibles, local, visita)
            st.dataframe(detalle, use_container_width=True)
        
        with tab3:  
            st.markdown("### Precisión del Modelo 🎯")
            st.markdown(
                "Aquí se muestra la precisión histórica del modelo de pronósticos para la liga seleccionada.")
            precision = df_total.predict(LigasDisponibles, local, visita)
            st.dataframe(precision, use_container_width=True) 

       
              



if __name__ == "__main__":
    main()
