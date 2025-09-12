
import polars as pl
from datetime import datetime, date
from scipy.stats import poisson
import random


class liga():
    def __init__(self, archivo):
        self.archivo = archivo
        self.df = pl.read_csv(archivo)

    def data(self):

        return self.df

    def data_Disputados(self):
        return self.df.drop_nulls()

    def data_Faltantes(self):
        return self.df.filter(pl.col('GA').is_null())

    def totaldisputados(self, liga):
        df = self.data_Disputados().filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0
        else:
            return df.height

    def TotalEncuentrosLiga(self, liga):
        df = self.df.filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0
        else:
            return df.height

    def totalvictorias(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()

        df_liga = df_liga.filter(pl.col('Resultado') == "1")

        return df_liga['Resultado'].count()
    
    def totalempates(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()

        df_liga = df_liga.filter(pl.col('Resultado') == "X")

        return df_liga['Resultado'].count()
    
    def totalperdidas(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()

        df_liga = df_liga.filter(pl.col('Resultado') == "2")

        return df_liga['Resultado'].count()
    
    
    def PGFliga(self,liga):
        df=self.df.filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0 
        else: 
            return df["GA"].mean()
        
        
    
    def PGCliga(self,liga):
        df=self.df.filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0 
        else: 
            return df["GC"].mean()
    
    def medialiga(self,liga):
        return self.PGFliga(liga)+self.PGCliga(liga)
    
    def AEM(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga= df_liga.filter(pl.col('GA') !=0).filter(pl.col('GC') !=0)
        

        return  df_liga.height
    
    def PromGEFL(self,liga,local):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Local')==local)
        if pfl.height == 0:
            return 0.0 
        else: 
            return pfl["GA"].mean()

    def PromGECL(self,liga,local):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Local')==local)
        if pfl.height == 0:
            return 0.0 
        else: 
            return pfl["GC"].mean()
         
    def PromGEFV(self,liga,visita):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Visita')==visita)
        if pfl.height == 0:
            return 0.0 
        else: 
            return pfl["GC"].mean()

    def PromGECV(self,liga,visita):
        df=self.df.filter(pl.col('Liga') == liga)
        pfl=df.filter(pl.col('Visita')==visita)
        if pfl.height == 0:
            return 0.0 
        else: 
            return pfl["GA"].mean()
    
    def fuerzaOfensivaLocal(self,liga,local):
        if self.PGFliga(liga)==0:
            return 0.0
        else:   
            return self.PromGEFL(liga,local) / self.PGFliga(liga)
    
    def fuerzaDefensivaLocal(self,liga,local):
        if self.PGCliga(liga)==0:
            return 0.0
        else:       
            return self.PromGECL(liga,local) / self.PGCliga(liga)
    
    def fuerzaOfensivaVisita(self,liga,visita):
        if self.PGCliga(liga)==0:
            return 0.0
        else:       
            return self.PromGEFV(liga,visita) / self.PGCliga(liga)
    
    def fuerzaDefensivaVisita(self,liga,visita):
        if self.PGFliga(liga)==0:
            return 0.0
        else:       
            return self.PromGECV(liga,visita) / self.PGFliga(liga)
    
    def fuerzaPromedioLocal(self, liga,local, visita):
        return self.PromGEFL(liga,local) * self.fuerzaDefensivaVisita(liga,visita)
    
    def fuerzaPromedioVisita(self, liga,local, visita):
        return self.PromGEFV(liga,visita) * self.fuerzaDefensivaLocal(liga,local)
    
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
        
    
    
    
    
    
    def precision_modelo(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
       
        
        if df_liga.height == 0:
            return pl.DataFrame({
                "Métrica": ["No hay datos disponibles para la liga seleccionada."],
                "Valor": ["N/A"]
            })
        
        
        total_partidos = df_liga.height 
        aciertos_local = 0
        aciertos_empate = 0
        aciertos_visita = 0
        ganador_real = 0
        empate_real = 0
        perdedor_real = 0    

        
        for row in df_liga.iter_rows(named=True):
            local = row['Local']
            visita = row['Visita']
            resultado_real = row['Resultado']  
            
            prob_local = self.VictoriaLocal(liga, local, visita)
            prob_empate = self.EmpateResultado(liga, local, visita)
            prob_visita = self.VictoriaVisita(liga, local, visita)
            
            prediccion = max(prob_local, prob_empate, prob_visita)
            
            if resultado_real=='1':
                ganador_real += 1
            elif resultado_real=='X':
                empate_real += 1
            elif resultado_real=='2':
                perdedor_real += 1
                

            if prediccion == prob_local and resultado_real == '1':
                aciertos_local += 1
               
                
            elif prediccion == prob_empate and resultado_real == 'X':
                aciertos_empate += 1
                
                
            elif prediccion == prob_visita and resultado_real == '2':
                aciertos_visita += 1
               
        precision_total = ((aciertos_local + aciertos_empate + aciertos_visita) / total_partidos) * 100 if total_partidos > 0 else 0
        
        df_precision = pl.DataFrame({
            "Métrica": [
                "Total de Partidos Analizados de la "+liga,
                "Aciertos Victoria Local (%)",
                "Aciertos Empate (%)",
                "Aciertos Victoria Visita (%)",
                "Precisión Total (%)",
            ],
            "Valor": [
                str(total_partidos),
                format(aciertos_local/ganador_real*100, '.2f')+"%",
                format(aciertos_empate/empate_real*100, '.2f')+"%",
                format(aciertos_visita/perdedor_real*100, '.2f')+"%",   
                f"{precision_total:.2f}%"   
                
            ]
        })
        
        return df_precision

    def liga05(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        
        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC"))>0).then(pl.lit("05"))
            .alias("mas05")
        )   
        
        df_liga =df_liga.filter(pl.col('mas05') == "05")
                
        return df_liga['mas05'].count()
    
    
    def liga15(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        
        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC"))>1).then(pl.lit("15"))
            .alias("mas15")
        )   
        
        df_liga =df_liga.filter(pl.col('mas15') == "15")
                
        return df_liga['mas15'].count()
    
    
    def liga25(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        
        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC"))>2).then(pl.lit("25"))
            .alias("mas25")
        )   
        
        df_liga =df_liga.filter(pl.col('mas25') == "25")
                
        return df_liga['mas25'].count()
        