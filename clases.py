
import polars as pl
from datetime import datetime,date
from scipy.stats import poisson
import random



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
    
    def menosde45goles(self,liga, local, visita):
        menosde45 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 5:
                    menosde45 += prob_local_x * prob_visita_y
                    
        return menosde45
    
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
    
    def detallepronosticos(self, ligas, local, visita):
        resultados = {
            "Victoria Local": self.VictoriaLocal(ligas, local, visita),
            "Empate": self.EmpateResultado(ligas, local, visita),
            "Victoria Visita": self.VictoriaVisita(ligas, local, visita),
            "1X Local o Empate": self.VictoriaLocal(ligas, local, visita) + self.EmpateResultado(ligas, local, visita),
            "2X Visita o Empate": self.VictoriaVisita(ligas, local, visita) + self.EmpateResultado(ligas, local, visita),
            "12 Local o Visita": self.VictoriaLocal(ligas, local, visita) + self.VictoriaVisita(ligas, local, visita),
            "Más de 0.5 Goles": self.masde05goles(ligas, local, visita),
            "Más de 1.5 Goles": self.masde15goles(ligas, local, visita),
            "Más de 2.5 Goles": self.masde25goles(ligas, local, visita),
            "Más de 3.5 Goles": self.masde35goles(ligas, local, visita),
            "Más de 4.5 Goles": self.masde45goles(ligas, local, visita),
            "Menos de 0.5 Goles": self.menosde05goles(ligas, local, visita),
            "Menos de 1.5 Goles": self.menosde15goles(ligas, local, visita),
            "Menos de 2.5 Goles": self.menosde25goles(ligas, local, visita),
            "Menos de 3.5 Goles": self.menosde35goles(ligas, local, visita),
            "Menos de 4.5 Goles": self.menosde45goles(ligas, local, visita),
            "Cero Goles": self.cerogoles(ligas, local, visita),
            "Con Goles": self.congoles(ligas, local, visita),
            "Ambos Marcan": self.ambosmarcan(ligas, local, visita),
            "Solo Uno Marca": self.solounomarca(ligas, local, visita)
        }
        
        df_resultados = pl.DataFrame({
            "Tipo de Apuesta": list(resultados.keys()),
            "Probabilidad": [f"{value:.2%}" for value in resultados.values()],
            "Cuota Sugerida (Decimal)": [f"{(1/value):.2f}" if value > 0 else "N/A" for value in resultados.values()]
        })
        
        return df_resultados
    
    def predict(self, ligas, local, visita):
        df_resultados = self.detallepronosticos(ligas, local, visita)
        
        # Filtrar las filas con probabilidad mayor o igual al 50%
        df_filtrado = df_resultados.filter(pl.col("Probabilidad").str.replace("%", "").cast(pl.Float64) >= 75.0)
        
        if df_filtrado.height == 0:
            return pl.DataFrame({
                "Tipo de Apuesta": ["No se encontraron pronósticos con probabilidad >= 50%"],
                "Probabilidad": ["N/A"],
                "Cuota Sugerida (Decimal)": ["N/A"]
            })
        
        return df_filtrado.sort("Probabilidad")
    
    
    
      
    
