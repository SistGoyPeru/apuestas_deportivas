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
    
    
       
    




#================================================================================================

def main():
  df_final=liga("data_ligas.csv")
  
  fecha=st.sidebar.date_input("Selecciona la Fecha para Pronosticar",date.today())
  df=df_final.data()
  
  dfecha=df.filter(pl.col("Fecha")==fecha.strftime("%d.%m.%Y")).sort("Liga")
  
  st.sidebar.title("**Ligas Disponibles**")
  ld=dfecha['Liga'].unique().sort() 
  LigasDisponibles=st.sidebar.selectbox("Liga Para Pronosticar",ld) 
  df_final=dfecha.filter(pl.col("Liga")==LigasDisponibles)
  st.dataframe(df_final)

 
    
 

if __name__ == "__main__":
  main()
