import pandas as pd
import requests 

def api_fred(series, key, fechaini, fechafin):
    
    """
    Importar múltiples series de la API del FRED. 
    
    Parámetros
    ----------
    series: dict
        Diccionario de los códigos y nombres de las series.
    
    key: str
        API Key del desarrollador. 
        Se obtiene de: "https://fred.stlouisfed.org/docs/api/api_key.html".
        
        - key: abcdefghijklmnopqrstuvwxyz123456
        
    fechaini: str
        Fecha de inicio de la serie.
        -Diario: yyyy-mm-dd
        -Mensual: yyyy-mm
        -Anual: yyyy
        
    fechfin: str
        Fecha de fin de la serie.
        -Diario: yyyy-mm-dd
        -Mensual: yyyy-mm
        -Anual: yyyy
 
    Retorno: 
    ----------
    df: pd. DataFrame
       Series consultadas
    
    Documentación: 
    --------------
    https://fred.stlouisfed.org/docs/api/fred/
    
    @authot: Mauricio Alvarado
             Norbert Andrei Romero Escobedo
    
    """
    
    
    keys = list(series.keys())

    df = pd.DataFrame()
    
    for i in keys:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={i}&api_key={key}&file_type=json"
    
        response = requests.get(url) ## HTTP: GET
        
        if response.status_code == 200:
            pass
        else:
            print("Porfavor, revisa los datos ingresados.")
            break
    
        response = response.json()
        observations = response.get("observations")
    
        values_list = []
        time_list = []
        
        for obs in observations:
            values_list.append(float(obs["value"]))
            time_list.append( obs["date"])


        dictio = {
            "time": time_list,
            f"{i}": values_list
        }
        dictio = pd.DataFrame(dictio)
    
        if df.empty is True:
            df = dictio
        else:
            df = pd. merge(df, dictio, how = "outer")

    df.set_index("time", inplace=True)
    df.rename (series, axis = 1, inplace = True)
    return df.loc[fechaini:fechafin]


#search_text = ['MOnetary', 'iNDex']
#api_key = '5ea7806d8a7a82af62865307b8dbf7d0'

def get_codes (search_text, api_key):
    
    """Extear metadatos
    Parámetros
    ----------
    search_text: list
        Consultas
    
    api_key: str
        API Key del desarrollador. 
        Se obtiene de: "https://fred.stlouisfed.org/docs/api/api_key.html".
        
        - key: abcdefghijklmnopqrstuvwxyz123456
    
    Retorno: 
    ----------
    df: pd. DataFrame
       Series consultadas
       
    @author: Mauricio Alvarado
             Norbert Andrei Romero Escobedo
    """
    
    formato = ["+".join(search_text).lower() for i in search_text][0]

    url = f"https://api.stlouisfed.org/fred/series/search?search_text={formato}&api_key={api_key}&file_type=json"
    response = requests.get(url) 
    response.status_code

    response= response.json()['seriess']

    list_id = []
    list_title = []
    list_start = []
    list_end = []
    list_frequency = []
    list_seasonal_adjusment = []

    for i in response:
        list_id.append(i['id'])
        list_title.append(i['title'])
        list_start.append(i['observation_start'])
        list_end.append(i['observation_end'])
        list_frequency.append(i['frequency'])
        list_seasonal_adjusment.append(i['seasonal_adjustment'])


    df = pd.DataFrame({"id":list_id,
                    "title":list_title,
                    "start":list_start,
                    "end": list_end,
                    "frequency": list_frequency,
                    "seasonal_adjusment":list_seasonal_adjusment})


    df.set_index("id", inplace=True) 
    return df

