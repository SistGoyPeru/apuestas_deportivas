import streamlit as st
from clases import liga



def main():
  ligas=liga("data_ligas.csv")
  st.write(ligas.data())

if __name__ == "__main__":
  main()
