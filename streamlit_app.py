import streamlit as st
import polars as pl
from datetime import datetime,date
from scipy.stats import poisson



class liga():
    def __init__(self, archivo):
        self.archivo = archivo
        self.df=pl.read_csv(archivo)

    def data(self):
        return self.df
    
    def ligas(self):
       return self.df['Liga'].unique().sort().to_list()  
    
    def PGFliga(self,liga):
        df=self.df.filter(pl.col('Liga') == liga)
        
        return df["GA"].mean()
    
    def PGCliga(self,liga):
        df=self.df.filter(pl.col('Liga') == liga)
        
        return df["GC"].mean()  
    
    def medialiga(self,liga):
        return self.PGFliga(liga)+self.PGCliga(liga)
    
    def PromGEFL(self,liga,local):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Local')==local)
        return pfl["GA"].mean()

    def PromGECL(self,liga,local):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Local')==local)
        return pfl["GC"].mean()
         
    def PromGEFV(self,liga,visita):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Visita')==visita)
        return pfl["GC"].mean()

    def PromGECV(self,liga,visita):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Visita')==visita)
        return pfl["GA"].mean()
    
    def fuerzaOfensivaLocal(self,liga,local):       
        return self.PromGEFL(liga,local) / self.PGFliga(liga)
    
    def fuerzaDefensivaLocal(self,liga,local):       
        return self.PromGECL(liga,local) / self.PGCliga(liga)
    
    def fuerzaOfensivaVisita(self,liga,visita):       
        return self.PromGEFV(liga,visita) / self.PGCliga(liga)
    
    def fuerzaDefensivaVisita(self,liga,visita):       
        return self.PromGECV(liga,visita) / self.PGFliga(liga)
    
    def fuerzaPromedioLocal(self, liga,local, visita):
        return ((self.PromGEFL(liga,local) * self.PromGECV(liga,visita))/self.medialiga(liga)) 
    
    def fuerzaPromedioVisita(self, liga,local, visita):
        return ((self.PromGEFV(liga,visita) * self.PromGECL(liga,local))/self.medialiga(liga)) 
    

    def VictoriaLocal(self, liga,local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo visitante (hasta un límite razonable)
        for y in range(21):
            prob_visita_y = poisson.pmf(y, fuerza_visita)
            
            # Probabilidad de que el local marque más de y goles
            prob_local_mas_y = 1 - poisson.cdf(y, fuerza_local)
            
            victoria += prob_visita_y * prob_local_mas_y
            
        return victoria
    
    def EmpateResultado(self,liga, local, visita):
        empate = 0.0
    
        fuerza_promedio_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_promedio_visita = self.fuerzaPromedioVisita(liga,local, visita)
    
        umbral = 1e-10
    
        for x in range(11):
        
            prob_local = poisson.pmf(x, fuerza_promedio_local)
            prob_visita = poisson.pmf(x, fuerza_promedio_visita)
            
           
            prob_empate_actual = prob_local * prob_visita
            empate += prob_empate_actual
         
            if prob_local < umbral or prob_visita < umbral:
                break
            
        return empate
    
    
    def VictoriaVisita(self, liga,local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Probabilidad de que el visitante marque más de x goles
            prob_visita_mas_x = 1 - poisson.cdf(x, fuerza_visita)
            
            victoria += prob_local_x * prob_visita_mas_x
            
        return victoria
    
    def masde05goles(self, liga,local, visita):
        masde05 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 0:
                    masde05 += prob_local_x * prob_visita_y
                    
        return masde05
    
    def masde15goles(self,liga, local, visita):
        masde15 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 1:
                    masde15 += prob_local_x * prob_visita_y
                    
        return masde15
    
    def masde25goles(self, liga,local, visita):
        masde25 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 2:
                    masde25 += prob_local_x * prob_visita_y
                    
        return masde25
    
    def masde35goles(self, liga,local, visita):
        masde35 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 3:
                    masde35 += prob_local_x * prob_visita_y
                    
        return masde35
    
    def masde45goles(self, liga,local, visita):
        masde45 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 4:
                    masde45 += prob_local_x * prob_visita_y
                    
        return masde45
    
    def menosde05goles(self,liga, local, visita):
        menosde05 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 1:
                    menosde05 += prob_local_x * prob_visita_y
                    
        return menosde05
    
    def menosde15goles(self,liga, local, visita):
        menosde15 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 2:
                    menosde15 += prob_local_x * prob_visita_y
                    
        return menosde15
    
    def menosde25goles(self,liga, local, visita):
        menosde25 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 3:
                    menosde25 += prob_local_x * prob_visita_y
                    
        return menosde25
    
    def menosde35goles(self,liga, local, visita):
        menosde35 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 4:
                    menosde35 += prob_local_x * prob_visita_y
                    
        return menosde35
    
    def cerogoles(self, liga,local, visita):
        cerogoles = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        prob_local_0 = poisson.pmf(0, fuerza_local)
        prob_visita_0 = poisson.pmf(0, fuerza_visita)
        
        cerogoles = prob_local_0 * prob_visita_0
        
        return cerogoles
    
    def congoles(self, liga,local, visita):
        return 1 - self.cerogoles(liga,local, visita)  
    

    def solounomarca(self, liga,local, visita):
        unomarca = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        prob_local_0 = poisson.pmf(0, fuerza_local)
        prob_visita_0 = poisson.pmf(0, fuerza_visita)
        
        prob_local_mas_0 = 1 - prob_local_0
        prob_visita_mas_0 = 1 - prob_visita_0
        
        unomarca = (prob_local_mas_0 * prob_visita_0) + (prob_local_0 * prob_visita_mas_0)
        
        return unomarca
    
    def ambosmarcan(self,liga, local, visita):
        return 1 - self.solounomarca(liga,local, visita) - self.cerogoles(liga,local, visita) 
    
    
       
    




#================================================================================================

def main():
  df_total=liga("data_ligas.csv")
  
  fecha=st.sidebar.date_input("Selecciona la Fecha para Pronosticar",date.today())
  df=df_total.data()
  
  dfecha=df.filter(pl.col("Fecha")==fecha.strftime("%d.%m.%Y")).sort("Liga")
  
  st.sidebar.title("**Ligas Disponibles**")
  ld=dfecha['Liga'].unique().sort() 
  LigasDisponibles=st.sidebar.selectbox("Liga Para Pronosticar",ld) 
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

        tab1, tab2, tab3 = st.tabs(["Principal", "Goles", "Combinaciones"])
        with tab1:
            with st.expander("Probabilidades de Resultado ( 1-X-2 ) ⚽:",expanded=True):
                
                st.set_page_config(layout="wide") # Utiliza el ancho completo de la página

                

                # Valores de ejemplo para el pronóstico (podrían ser porcentajes o votos)
                # Aquí usamos valores aleatorios para simular un pronóstico dinámico
                prob_local = df_total.VictoriaLocal(LigasDisponibles,local, visita)*100
                prob_empate = df_total.EmpateResultado(LigasDisponibles,local, visita)*100
                prob_visitante = df_total.VictoriaVisita(LigasDisponibles,local, visita)*100

                # Colores y títulos personalizados para cada pronóstico
                colores = {
                    "Local": "#28a745",     # Verde para victoria local
                    "Empate": "#ffc107",    # Amarillo para empate
                    "Visitante": "#dc3545"  # Rojo para victoria visitante
                }

                # Crear las tres columnas para el pronóstico
                col1, col2, col3 = st.columns(3)

            # --- Columna de Pronóstico Local ---
            with col1:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Local']};">
                    <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Victoria Local</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Local']}; margin: 5px 0 0 0;">
                        {prob_local:.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # --- Columna de Pronóstico de Empate ---
            with col2:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Empate']};">
                    <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Empate</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Empate']}; margin: 5px 0 0 0;">
                        {prob_empate:.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # --- Columna de Pronóstico Visitante ---
            with col3:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center; border-left: 5px solid {colores['Visitante']};">
                    <h3 style="margin: 0; font-size: 1.2rem; color: #555;">Victoria Visitante</h3>
                    <p style="font-size: 2.5rem; font-weight: bold; color: {colores['Visitante']}; margin: 5px 0 0 0;">
                        {prob_visitante:.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)

            
                
            
            with st.expander("Ambos Equipos Marcan:",expanded=True):
                a,b=st.columns(2)
    
                a.metric("SI",format(1/df_total.ambosmarcan(LigasDisponibles,local,visita),'.2f'),border=True)       
                
                b.metric("NO",format(1/df_total.solounomarca(LigasDisponibles,local,visita),'.2f'),border=True) 

                
            with st.expander("Doble Opòrtunidad:",expanded=True):

                a,b,c=st.columns(3)
              
                a.metric(local+" O Empate",format(1/(df_total.VictoriaLocal(LigasDisponibles,local,visita)+df_total.EmpateResultado(LigasDisponibles,local,visita)),'.2f'),border=True)
                
                b.metric(local+" O "+visita,format(1/(df_total.VictoriaVisita(LigasDisponibles,local,visita)+df_total.VictoriaLocal(LigasDisponibles,local,visita)),'.2f') ,border=True)
                
                c.metric("Empate O "+visita,format(1/(df_total.EmpateResultado(LigasDisponibles,local,visita)+df_total.VictoriaVisita(LigasDisponibles,local,visita)),'.2f'),border=True) 


        with tab2:
            with st.expander("Va Haber Goles:",expanded=True):
                a,b=st.columns(2)
    
                a.metric("NO",format(1/df_total.cerogoles(LigasDisponibles,local,visita),'.2f'),border=True)       
                
                b.metric("SI",format(1/df_total.congoles(LigasDisponibles,local,visita),'.2f'),border=True) 
            
            with st.expander("Goles Totales - Más/Menos:",expanded=True):
                a,b,c,d=st.columns(4)
              
                a.metric("Más de 0.5",format(1/df_total.masde05goles(LigasDisponibles,local,visita),'.2f'),border=True)
                
                b.metric("Más de 1.5",format(1/df_total.masde15goles(LigasDisponibles,local,visita),'.2f') ,border=True)
                
                c.metric("Más de 2.5",format(1/df_total.masde25goles(LigasDisponibles,local,visita),'.2f'),border=True) 

                d.metric("Más de 3.5",format(1/df_total.masde35goles(LigasDisponibles,local,visita),'.2f'),border=True)
                
                
                d,e,f,g=st.columns(4)
              
                d.metric("Menos de 0.5",format(1/df_total.menosde05goles(LigasDisponibles,local,visita),'.2f'),border=True)
                
                e.metric("Menos de 1.5",format(1/df_total.menosde15goles(LigasDisponibles,local,visita),'.2f') ,border=True)
                
                f.metric("Menos de 2.5",format(1/df_total.menosde25goles(LigasDisponibles,local,visita),'.2f'),border=True)
                
                g.metric("Menos de 3.5",format(1/df_total.menosde35goles(LigasDisponibles,local,visita),'.2f'),border=True)
            
            

        
    
 

if __name__ == "__main__":
  main()
