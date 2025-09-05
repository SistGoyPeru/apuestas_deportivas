import streamlit as st
from clases import liga
import polars as pl
from datetime import datetime,date

def main():
  
  colores = {
    "Local": "#28a745",     # Verde para victoria local
    "Empate": "#ffc107",    # Amarillo para empate
    "Visitante": "#dc3545"  # Rojo para victoria visitante
    }

    






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


        st.markdown(f"### Pronóstico para: {local} vs {visita} ({LigasDisponibles})")
        tab1, tab2, tab3 = st.tabs(["📊 Resumen", "📋 Detalle de Pronósticos", "🎯 Precisión del Modelo"])
        with tab1:
            with st.expander("Probabilidades de Resultado ( 1-X-2 ) ⚽:",expanded=True):
                prob_local = df_total.VictoriaLocal(LigasDisponibles,local, visita)*100
                prob_empate = df_total.EmpateResultado(LigasDisponibles,local, visita)*100
                prob_visitante = df_total.VictoriaVisita(LigasDisponibles,local, visita)*100

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
            

        
        
        
  
  
  
  

if __name__ == "__main__":
  main()
