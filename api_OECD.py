import pandas as pd
import requests 
import sys



def get_data(identifier, countries, datos, fechaini, fechafin, periodicidad):
    
    """ Importar multiples series de la API de la OCDE
    
    Parametros
    ----------
    identifier: str
        Código identificador de la base de datos ???
    countries: dict
        Códigos y nombres de los países (keys, values)
    datos: str
        Código de las series
    fechaini: str
        Fecha de inicio (yyyy-qq) 
    fechafin: str
        Fecha de fin (yyyy-qq) 
    periodicidad: str
        Frecuencia de los datos: "Q", "Y"    
    
    Retorno
    -------
    df: pd.DataFrame
        Series consultadas
    
    Documentación
    -------
    https://stats.oecd.org/
    
    
    @author: Nobert Andrei Romero Escobedo
             Mauricio Alvarado
    
    """


    # Uno los codigos de los paises con un '+'
    filters = ["+".join(i) for i in countries.keys()]
    
    # Nombres de los países
    nombres = list(countries.values())
    
    # Cuantos paises hay?
    cantidad_paises = len(countries.keys())
    
    url = f"https://stats.oecd.org/SDMX-JSON/data/{identifier}/{filters}.{datos}/all?startTime={fechaini}&endTime={fechafin}"

    # Requests a la base de datos
    r = requests.get(url)
    if r.status_code == 200:
        pass
    else:
        print("Porfavor, revisa los datos ingresados.")
        sys.exit()


    # Consigo la ruta donde están las series, pero contiene más info
    series = r.json()["dataSets"][0]["series"]    
    
    df = pd.DataFrame()
    j = 0 # Para asignar los nombres a las columnas

    
    # Loop para consultar las series de cada país
    for i in range(0, cantidad_paises):
        fechas = list(list(series.values())[i]["observations"].keys())    # Índices con fechas
        valores = list(list(series.values())[i]["observations"].values()) # Valores, en bruto
        
        # Extraer los valores, limpios -> renombrado como 'nv'
        nv = []
        for i in range(0, len(fechas)):
            nv.append(valores[i][0])
        
        # Merge los datos de cada país
        if df.empty == True:
            df = pd.DataFrame({"fechas": fechas, nombres[j]: nv})
        else:
            df2 = pd.DataFrame({"fechas": fechas, nombres[j]: nv})
            df = df.merge(df2, how="inner")
        j += 1    
      
    # Asigno a la columna fechas en el índice  
    df = df.set_index("fechas")
    
    # Creo una lista con el rango de `fechaini` - `fechafin``
    df.index = pd.period_range(fechaini, fechafin, freq=periodicidad)

    return df