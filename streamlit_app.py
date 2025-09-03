import streamlit as st
import polars as pl

class liga():
    def __init__(self, archivo):
        self.archivo = archivo
        self.df=pl.read_csv(archivo)

    def data(self):
        return self.df




def main():
  ligas=liga("data_liga.csv")
  st.write(ligas.data())

if __name__ == "__main__":
  main()
