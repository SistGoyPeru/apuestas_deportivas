import polars as pl

class liga():
    def __init__(self, archivo):
        self.archivo = archivo
        self.df = pl.read_csv(archivo)

    def data(self):
        return self.df
    
