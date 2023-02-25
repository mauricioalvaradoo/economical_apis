import pandas as pd
import pandas_datareader.data as web
import requests



def get_data(countries, series, fechaini, fechafin, database='IMF_WEOPUB'):
 
    """ Importar multiples series de la API del IMF
    
    Parámetros
    ----------
    list_countries: dict
        Códigos de países
    list_series: dict
        Codigos de las series
    fechaini: str
        Fecha de inicio
    fechafin: str
        Fecha de fin
    database: str
        Base de datos
    
    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas

    Ejemplo
    ----------
    Formato de fechas incluso para anual con el formato de mes:
    >>> yyyy-mm-dd
    
    Donde:
    >>> Anual:   yyyy-01-01
    >>> Mensual: yyyy-mm-01

    Para el caso de las bases de datos:
    >>> World Economic Outlook: IMF_WEOPUB
    >>> 

    Documentación
    ----------
    * https://www.econdb.com/tree
    
    
    @author: Mauricio Alvarado
    
    """
    
    series_codes    = list(series.keys())
    countries_codes = list(countries.keys())
    
    df = web.DataReader(
        '&'.join([
            'dataset={database}', 
            'v=Reference area', 
            'h=TIME', 
            f'from={fechaini}', 
            f'to={fechafin}', 
            'CONCEPT=[NGDP_RPCH]', 
            f'FROM=[{fechaini}]', 
            f'TO=[{fechafin}]'
        ]),
        'econdb'
    )
    
    return df



def search(tipo, consulta=None):
    
    """ Extraer código de la consulta
    
    Parámetros
    ----------
    tipo: str
        Tipo de datos a consultar: "Indicadores", "Países", "Regiones", "Grupos"
    consulta: list
        Palabras claves de consulta. Default: None

    Retorno
    ----------
    df: pd.DataFrame
        Consulta

    Documentación
    ----------
    * https://www.imf.org/en/Data
    * https://www.imf.org/external/datamapper/api/help


    @author: Mauricio Alvarado
    
    """


    if tipo == "Indicadores":
        url = "https://www.imf.org/external/datamapper/api/v1/indicators"
        r = requests.get(url).json()["indicators"]
        df = search_df1(r)  
    elif tipo == "Países":
        url = "https://www.imf.org/external/datamapper/api/v1/countries"
        r = requests.get(url).json()["countries"]
        df = search_df2(r)  
    elif tipo == "Regiones":
        url = "https://www.imf.org/external/datamapper/api/v1/regions"
        r = requests.get(url).json()["regions"]
        df = search_df2(r)
    elif tipo == "Grupos":
        url = "https://www.imf.org/external/datamapper/api/v1/groups"
        r = requests.get(url).json()["groups"]
        df = search_df2(r)
    else:
        url = print("Revisa bien el tipo!")

    df.dropna(inplace=True)


    if consulta is not None:
        consulta = [x.lower() for x in consulta]
            
        for i in consulta:
            filter = df["Nombres"].str.lower().str.contains(i)
            df = df[filter]

    else:
        pass

    df.set_index("Código", inplace=True)

    return df


def search_df1(r):
    codes    = []
    names    = []
    units    = []
    datasets = []
    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])
        units.append(i["unit"])
        datasets.append(i["dataset"])
            
    df1 = pd.DataFrame({
        "Código": codes, "Nombres": names, "Unidades": units, "Dataset": datasets
    })

    return df1

def search_df2(r):
    codes = []
    names = []
    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])
        
    df2 = pd.DataFrame({"Código": codes, "Nombres": names})

    return df2

    
