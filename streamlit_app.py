import streamlit as st
import polars as pl

class liga():
    def __init__(self, archivo):
        self.archivo = archivo
        self.df=pl.read_csv(archivo)

    def data(self):
        return self.df
    




#================================================================================================

def main():
  df_final=liga("data_ligas.csv")
  
  st.sidebar.title("**Ligas Disponibles**")
  ligas=df_final['Liga'].unique().sort()   
  LigasDisponibles=st.sidebar.selectbox("Liga Para Pronosticar",ligas)
  df_final=df_final.filter(pl.col("Liga")==LigasDisponibles)

if __name__ == "__main__":
  main()
