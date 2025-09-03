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
        return (self.fuerzaOfensivaLocal(liga,local) * self.fuerzaDefensivaVisita(liga,visita)) 
    
    def fuerzaPromedioVisita(self, liga,local, visita):
        return (self.fuerzaOfensivaVisita(liga,visita) * self.fuerzaDefensivaLocal(liga,local)) 
    

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
        
        a, b = st.columns(2)
        a.write("**"+local+" vs "+visita+"**") 
        b.write("**Fecha:** "+df_final[selected_row, 'Fecha'])

        st.markdown("**Probabilidades de Resultado ( 1-X-2 ):**")
        c1,c2,c3=st.columns(3,gap='large')
        with c1:
              st.metric("Kpi Victoria Local",format(df_total.VictoriaLocal(liga,local,visita)*100,'.2f')+"%",format(1/df_total.VictoriaLocal(liga,local,visita),'.2f'),border=True)
        

        

       

 
    
 

if __name__ == "__main__":
  main()
