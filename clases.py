
import polars as pl
from datetime import datetime, date

from scipy.stats import poisson
import random

#-------------------------------------------------------
class liga():
    def __init__(self,archivo):
        self.archivo = archivo
        self.df = pl.read_excel(archivo)

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

    def PGFliga(self, liga):
        df = self.df.filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0
        else:
            return df["GA"].mean()

    def PGCliga(self, liga):
        df = self.df.filter(pl.col('Liga') == liga)
        if df.height == 0:
            return 0.0
        else:
            return df["GC"].mean()

    def medialiga(self, liga):
        return self.PGFliga(liga)+self.PGCliga(liga)

    def AEM(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('GA') != 0).filter(pl.col('GC') != 0)

        return df_liga.height
    
    def AEMLocal(self,liga,local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)
        
        df_liga = df_liga.filter(pl.col('GA') != 0).filter(pl.col('GC') != 0)
        
        
        return df_liga.height
        
    def AEMVisita(self,liga,visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)
        df_liga = df_liga.filter(pl.col('GA') != 0).filter(pl.col('GC') != 0)

        return df_liga.height

    def PromGEFL(self, liga, local):
        df = self.df.filter(pl.col('Liga') == liga)
        pfl = df.filter(pl.col('Local') == local)
        if pfl.height == 0:
            return 0.0
        else:
            return pfl["GA"].mean()

    def PromGECL(self, liga, local):
        df = self.df.filter(pl.col('Liga') == liga)
        pfl = df.filter(pl.col('Local') == local)
        if pfl.height == 0:
            return 0.0
        else:
            return pfl["GC"].mean()

    def PromGEFV(self, liga, visita):
        df = self.df.filter(pl.col('Liga') == liga)
        pfl = df.filter(pl.col('Visita') == visita)
        if pfl.height == 0:
            return 0.0
        else:
            return pfl["GC"].mean()

    def PromGECV(self, liga, visita):
        df = self.df.filter(pl.col('Liga') == liga)
        pfl = df.filter(pl.col('Visita') == visita)
        if pfl.height == 0:
            return 0.0
        else:
            return pfl["GA"].mean()

    def fuerzaOfensivaLocal(self, liga, local):
        if self.PGFliga(liga) == 0:
            return 0.0
        else:
            return self.PromGEFL(liga, local) / self.PGFliga(liga)

    def fuerzaDefensivaLocal(self, liga, local):
        if self.PGCliga(liga) == 0:
            return 0.0
        else:
            return self.PromGECL(liga, local) / self.PGCliga(liga)

    def fuerzaOfensivaVisita(self, liga, visita):
        if self.PGCliga(liga) == 0:
            return 0.0
        else:
            return self.PromGEFV(liga, visita) / self.PGCliga(liga)

    def fuerzaDefensivaVisita(self, liga, visita):
        if self.PGFliga(liga) == 0:
            return 0.0
        else:
            return self.PromGECV(liga, visita) / self.PGFliga(liga)

    def fuerzaPromedioLocal(self, liga, local, visita):
        return self.PromGEFL(liga, local) * self.fuerzaDefensivaVisita(liga, visita)

    def fuerzaPromedioVisita(self, liga, local, visita):
        return self.PromGEFV(liga, visita) * self.fuerzaDefensivaLocal(liga, local)

    def VictoriaLocal(self, liga, local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga, local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga, local, visita)

        # Buclea solo los goles del equipo visitante (hasta un límite razonable)
        for y in range(21):
            prob_visita_y = poisson.pmf(y, fuerza_visita)

            # Probabilidad de que el local marque más de y goles
            prob_local_mas_y = 1 - poisson.cdf(y, fuerza_local)

            victoria += prob_visita_y * prob_local_mas_y

        return victoria

    def EmpateResultado(self, liga, local, visita):
        empate = 0.0

        fuerza_promedio_local = self.fuerzaPromedioLocal(liga, local, visita)
        fuerza_promedio_visita = self.fuerzaPromedioVisita(liga, local, visita)

        umbral = 1e-10

        for x in range(11):

            prob_local = poisson.pmf(x, fuerza_promedio_local)
            prob_visita = poisson.pmf(x, fuerza_promedio_visita)

            prob_empate_actual = prob_local * prob_visita
            empate += prob_empate_actual

            if prob_local < umbral or prob_visita < umbral:
                break

        return empate

    def VictoriaVisita(self, liga, local, visita):
        victoria = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga, local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga, local, visita)

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

            if resultado_real == '1':
                ganador_real += 1
            elif resultado_real == 'X':
                empate_real += 1
            elif resultado_real == '2':
                perdedor_real += 1

            if prediccion == prob_local and resultado_real == '1':
                aciertos_local += 1

            elif prediccion == prob_empate and resultado_real == 'X':
                aciertos_empate += 1

            elif prediccion == prob_visita and resultado_real == '2':
                aciertos_visita += 1

        precision_total = ((aciertos_local + aciertos_empate + aciertos_visita) /
                           total_partidos) * 100 if total_partidos > 0 else 0

        df_precision = pl.DataFrame({
            "Analisis": [
                "Total de Partidos Analizados",
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
            pl.when((pl.col("GA") + pl.col("GC")) > 0).then(pl.lit("05"))
            .alias("mas05")
        )

        df_liga = df_liga.filter(pl.col('mas05') == "05")

        return df_liga['mas05'].count()
    
    def liga05Local(self, liga,local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        
        df_liga = df_liga.filter(pl.col('Local') == local)
      

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 0).then(pl.lit("05"))
            .alias("mas05")
        )

        df_liga = df_liga.filter(pl.col('mas05') == "05")
        
        return df_liga['mas05'].count()
    
    def liga15Local(self, liga,local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 1).then(pl.lit("15"))
            .alias("mas15")
        )

        df_liga = df_liga.filter(pl.col('mas15') == "15")

        return df_liga['mas15'].count()
    
    def liga25Local(self, liga,local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 2).then(pl.lit("25"))
            .alias("mas25")
        )

        df_liga = df_liga.filter(pl.col('mas25') == "25")

        return df_liga['mas25'].count()
    
    def liga05Visita(self, liga,visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        
        df_liga = df_liga.filter(pl.col('Visita') == visita)
      

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 0).then(pl.lit("05"))
            .alias("mas05")
        )

        df_liga = df_liga.filter(pl.col('mas05') == "05")
        
        return df_liga['mas05'].count()
    
    def liga15Visita(self, liga,visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 1).then(pl.lit("15"))
            .alias("mas15")
        )

        df_liga = df_liga.filter(pl.col('mas15') == "15")

        return df_liga['mas15'].count()
    
    def liga25Visita(self, liga,visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 2).then(pl.lit("25"))
            .alias("mas25")
        )

        df_liga = df_liga.filter(pl.col('mas25') == "25")

        return df_liga['mas25'].count()

    def liga15(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 1).then(pl.lit("15"))
            .alias("mas15")
        )

        df_liga = df_liga.filter(pl.col('mas15') == "15")

        return df_liga['mas15'].count()

    def liga25(self, liga):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()

        df_liga = df_liga.with_columns(
            pl.when((pl.col("GA") + pl.col("GC")) > 2).then(pl.lit("25"))
            .alias("mas25")
        )

        df_liga = df_liga.filter(pl.col('mas25') == "25")

        return df_liga['mas25'].count()

    def equipos_ligas(self, liga):

        return self.df.filter(pl.col('Liga') == liga)['Local'].unique().sort()

    def TotalDisputadosEquipoLocal(self, liga, local):
        df = self.df.filter(pl.col('Liga') == liga)
        df = df.filter(pl.col('Local') == local)
        if df.height == 0:
            return 0.0
        else:
            return df["GA"].count()

    def TotalDisputadosEquipoVisita(self, liga, visita):
        df = self.df.filter(pl.col('Liga') == liga)
        df = df.filter(pl.col('Visita') == visita)
        if df.height == 0:
            return 0.0
        else:
            return df["GC"].count()

    def TotalVictoriasEquipoLocal(self, liga, local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)

        df_liga = df_liga.filter(pl.col('Resultado') == "1")

        if df_liga.height == 0:
            return 0.0
        else:
            return df_liga['Resultado'].count()

    def TotalVictoriasEquipoVisita(self, liga, visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)

        df_liga = df_liga.filter(pl.col('Resultado') == "2")
        if df_liga.height == 0:
            return 0.0
        else:
            return df_liga['Resultado'].count()

    def TotalEmpatesEquipoLocal(self, liga, local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)

        df_liga = df_liga.filter(pl.col('Resultado') == "X")

        return df_liga['Resultado'].count()

    def TotalEmpatesEquipoVisita(self, liga, visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)

        df_liga = df_liga.filter(pl.col('Resultado') == "X")

        return df_liga['Resultado'].count()

    def TotalPerdidasEquipoLocal(self, liga, local):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Local') == local)

        df_liga = df_liga.filter(pl.col('Resultado') == "2")

        return df_liga['Resultado'].count()

    def TotalPerdidasEquipoVisita(self, liga, visita):
        df_liga = self.df.filter(pl.col('Liga') == liga).drop_nulls()
        df_liga = df_liga.filter(pl.col('Visita') == visita)

        df_liga = df_liga.filter(pl.col('Resultado') == "1")

        return df_liga['Resultado'].count()
    
    
    def PPP(self, liga,equipo):
        ppp = 0.0
        totalVictorias= self.TotalVictoriasEquipoVisita(liga, equipo)+self.TotalVictoriasEquipoLocal(liga, equipo)
        puntosvictoria=totalVictorias*3
        totalEmpates=self.TotalEmpatesEquipoLocal(liga, equipo)+self.TotalEmpatesEquipoVisita(liga, equipo)
        puntosEmpate=totalEmpates*1
        ppp = (puntosvictoria+puntosEmpate) /(self.TotalDisputadosEquipoLocal(liga, equipo)+self.TotalDisputadosEquipoVisita(liga, equipo))
        return ppp
        
    def PPP_local(self, liga,local):
        ppp = 0.0
        totalVictorias=self.TotalVictoriasEquipoLocal(liga, local)
        puntosvictoria=totalVictorias*3
        totalEmpates=self.TotalEmpatesEquipoLocal(liga, local)
        puntosEmpate=totalEmpates*1 
        ppp=(puntosvictoria+puntosEmpate)/self.TotalDisputadosEquipoLocal(liga, local)
        return ppp
    
    def PPP_visita(self, liga,visita):
        ppp = 0.0
        totalVictorias=self.TotalVictoriasEquipoVisita(liga, visita)    
        puntosvictoria=totalVictorias*3
        totalEmpates=self.TotalEmpatesEquipoVisita(liga, visita)
        puntosEmpate=totalEmpates*1 
        ppp=(puntosvictoria+puntosEmpate)/self.TotalDisputadosEquipoVisita(liga, visita)
        return ppp
    
          

         
        

       

    
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
    
    def masde55goles(self, liga,local, visita):
        masde55 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) > 5:
                    masde55 += prob_local_x * prob_visita_y
                    
        return masde55
    
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
    
    def menosde55goles(self,liga, local, visita):
        menosde55 = 0.0
        fuerza_local = self.fuerzaPromedioLocal(liga,local, visita)
        fuerza_visita = self.fuerzaPromedioVisita(liga,local, visita)
        
        # Buclea solo los goles del equipo local (hasta un límite razonable)
        for x in range(21):
            prob_local_x = poisson.pmf(x, fuerza_local)
            
            # Buclea solo los goles del equipo visitante (hasta un límite razonable)
            for y in range(21):
                prob_visita_y = poisson.pmf(y, fuerza_visita)
                
                if (x + y) < 6:
                    menosde55 += prob_local_x * prob_visita_y
                    
        return menosde55
    

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
        
        # Filtrar las filas con probabilidad mayor o igual al 75%
        df_filtrado = df_resultados.filter(pl.col("Probabilidad").str.replace("%", "").cast(pl.Float64) >= 75.0)
        
        if df_filtrado.height == 0:
            return pl.DataFrame({
                "Tipo de Apuesta": ["No se encontraron pronósticos con probabilidad >= 75%"],
                "Probabilidad": ["N/A"],
                "Cuota Sugerida (Decimal)": ["N/A"]
            })
        
        return df_filtrado.sort("Probabilidad")
    
    def predictcombinados(self, ligas, local, visita):
        df_resultados = self.detallepronosticoscombinados(ligas, local, visita)
        
        # Filtrar las filas con probabilidad mayor o igual al 75%
        df_filtrado = df_resultados.filter(pl.col("Probabilidad").str.replace("%", "").cast(pl.Float64) >= 75.0)
        
        if df_filtrado.height == 0:
            return pl.DataFrame({
                "Tipo de Apuesta Combinada": ["No se encontraron pronósticos combinados con probabilidad >= 75%"],
                "Probabilidad": ["N/A"],
                "Cuota Sugerida (Decimal)": ["N/A"]
            })
        
        return df_filtrado.sort("Probabilidad") 
    #-----_aa
    def localmas05(self, liga, local, visita):
        return self.VictoriaLocal(liga, local, visita) * self.masde05goles(liga, local, visita) 
    
    def localmas15(self, liga, local, visita):
        return self.VictoriaLocal(liga, local, visita) * self.masde15goles(liga, local, visita) 
    
    def localmas25(self, liga, local, visita):
        return self.VictoriaLocal(liga, local, visita) * self.masde25goles(liga, local, visita)
    
    def visitamas05(self, liga, local, visita):
        return self.VictoriaVisita(liga, local, visita) * self.masde05goles(liga, local, visita)
    
    def visitamas15(self, liga, local, visita):
        return self.VictoriaVisita(liga, local, visita) * self.masde15goles(liga, local, visita) 
       
    def visitamas25(self, liga, local, visita):
        return self.VictoriaVisita(liga, local, visita) * self.masde25goles(liga, local, visita)
    
    def empatemas05(self, liga, local, visita):
        return self.EmpateResultado(liga, local, visita) * self.congoles(liga, local, visita)
    def empatemas15(self, liga, local, visita):
        return self.EmpateResultado(liga, local, visita) * self.masde15goles(liga, local, visita)
    def empatemas25(self, liga, local, visita):
        return self.EmpateResultado(liga, local, visita) * self.masde25goles(liga, local, visita)
    
    def detallepronosticoscombinados(self, ligas, local, visita):
        resultados = {
            "Victoria Local y Más de 0.5 Goles": self.localmas05(ligas, local, visita),
            "Victoria Local y Más de 1.5 Goles": self.localmas15(ligas, local, visita),
            "Victoria Local y Más de 2.5 Goles": self.localmas25(ligas, local, visita),
            "Victoria Visita y Más de 0.5 Goles": self.visitamas05(ligas, local, visita),
            "Victoria Visita y Más de 1.5 Goles": self.visitamas15(ligas, local, visita),
            "Victoria Visita y Más de 2.5 Goles": self.visitamas25(ligas, local, visita),
            "Empate y Más de 0.5 Goles": self.empatemas05(ligas, local, visita),
            "Empate y Más de 1.5 Goles": self.empatemas15(ligas, local, visita),
            "Empate y Más de 2.5 Goles": self.empatemas25(ligas, local, visita)
        }
        df_resultados = pl.DataFrame({
            "Tipo de Apuesta Combinada": list(resultados.keys()),
            "Probabilidad": [f"{value:.2%}" for value in resultados.values()],
            "Cuota Sugerida (Decimal)": [f"{(1/value):.2f}" if value > 0 else "N/A" for value in resultados.values()]
        })      
        return df_resultados

