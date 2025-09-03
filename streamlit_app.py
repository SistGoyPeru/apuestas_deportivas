import streamlit as st
import polars as pl
from datetime import datetime,date

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

        st.write(df_total.PGFliga(LigasDisponibles))
        st.write(df_total.PGCliga(LigasDisponibles))
        st.write(df_total.PromGEFL(LigasDisponibles,local))

       

 
    
 

if __name__ == "__main__":
  main()
