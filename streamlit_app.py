import streamlit as st
from clases import liga

def main():
  df_total=liga("data_ligas.csv")
  st.write(df_total.data())
  
  

if __name__ == "__main__":
  main()
