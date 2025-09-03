import streamlit as st
from scraper import FootballDataScraper


def main():
  st.write(FootballDataScraper("https://www.livefutbol.com/todos_partidos/per-primera-division-2025-clausura/"))


if __name__ == "__main__":
  main()
