#Este proyecto es sencillo, dentro de la etapa de transformación se podrían agregar operaciones de ML
# Se agrega el webscraping realizado anteriormente a el extractor de información 
import requests
import pandas as pd

class ExtractorPeliculas:
    def __init__(self, passApi):  
        self.llaveApi=passApi
    
    def busqueda_nombres(self,queries,max_pages=5):
        resultados=[]
        for q in queries:
            for page in range(1,max_pages+1):
                url=f"http://www.omdbapi.com/?s={q}&type=movie&apikey={self.llaveApi}&page={page}"  # "?s=" para encontrar sólo el titulo de la pelicula
                r=requests.get(url,timeout=30)
                data=r.json()
                print(f"Consulta {url}" )
                print(data)
                if data.get("Response")=="True":
                    resultados.extend([p["Title"] for p in data["Search"]])  #<-Recorre cada elemento "p"  dentro de "Search" del cual extrae sólo "Title"
                else:
                    print(f"No hay resultados para {q} en pagina{page} : {data.get('Error')}")
                    break
        return resultados
    def fetch_movie(self,titulo): # Esta función se construye para recabar los detalles de una sóla pelicula, la cual a través del bucle dentro de "extrae_pelicula" recolecta el conjunto dentro de la lista "resultados"        
        url=f"http://www.omdbapi.com/?t={titulo}&apikey={self.llaveApi}" #<- "?t=" recolecta información más detallada
        r=requests.get(url,timeout=30)
        return r.json()

    def extrae_pelicula(self,resultados):
        data=[]
        for titulo in resultados:
            peli=self.fetch_movie(titulo)
            if peli.get('Response')=='True':
                data.append(peli)
            else:
                print(f"No se encontró: {titulo}")
        return pd.DataFrame(data)

#Lo siguiente es empezar a construir la instanciacion para la etapa de extracción

# API_KEY="Aqui va tu clave"
# clave=ExtractorPeliculas(API_KEY)#Esta es mi instancia principal
# palabrasClave = ["star", "love", "man", "dark"]
# nombrespeliculas=clave.busqueda_nombres(palabrasClave) 
# datosPeliculas=clave.extrae_pelicula(nombrespeliculas)
# print(datosPeliculas)
