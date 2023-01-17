import pandas as pd
import requests 
import sys


def get_data(countries, indicator, startTime, endTime):
    """
    Importar múltiples series de la API del BM (Banco Mundial).
    
    Parámetros
    ----------
    countries: dict
        Diccionario de los códigos y nombres de los países.
        - countries = {
            "BR": "Brasil",
            "CL": "Chile",
            "PE": "Perú"
        }
        
    indicator: str
        
        Código del indicador o serie. 
        Se obtiene de: "https://datos.bancomundial.org/indicator/"
        
        - indicator = 'BX.KLT.DINV.WD.GD.ZS'
        
    startTime: str
        Fecha de inicio de la serie. 
        -Anual: yyyy
        
    endTime: str
        Fecha de fin de la serie. 
        -Anual: yyyy
        
    Retorno: 
    --------
    df: pd.DataFrame
        Países con las series consultadas.    
    
    Documentación:
    -------------
    https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure
    
    
    @author: Mauricio Alvarado
             Norbert Andrei Romero Escobedo
    """

    
    keys = list(countries.keys())
    df = pd.DataFrame()
    
    for key in keys:
        url = f'http://api.worldbank.org/v2/country/{key}/indicator/{indicator}?format=json'
         
        response = requests.get(url) 
                
        if response.status_code == 200:
            pass
        else:
            print("Porfavor, revisa los datos ingresados")
            break
    
        response = response.json()
        observations = response[1]
    
        values_list = []
        time_list = []
    
        for obs in observations: 
            values_list.append((obs['value']))
            time_list.append(obs["date"])
    
        dictio = {
            "time": time_list, 
            f"{key}": values_list
        }
        dictio = pd.DataFrame(dictio)
                   
        if df.empty is True:
             df = pd.concat([df, dictio])
        else:
            df = pd.merge(df, dictio, how = "outer")
    
    df.set_index('time', inplace = True)
    df.sort_index(ascending=True, inplace=True)
    df.rename(countries, axis=1, inplace=True)
            
    return df
      
      
      
      
      
def get_codes(search_text):
        
    """Extraer metadatos
    Parámetros
    ----------
    search_text: list
        Dos palabras clave de la consulta. 
        
        -search_text =['life','expectancy']
        
    Retorno: 
    ---------
    df: pd. DataFrame
       Series consultadas
                  
    @author: Mauricio Alvarado
             Norbert Andrei Romero Escobedo  
    """

    formato = ["%20".join(search_text).lower() for i in search_text][0]   
   
    url = f"http://api.worldbank.org/v2/sources/2/search/{formato}?format=json"
    response = requests.get(url) 
    response = response.json()['source'][0]['concept'][1]['variable']#[0]['id']
    
    list_id= []
    list_names= []
    
    
    for i in response: 
        list_id.append(i['id'])
        list_names.append(i['name'])
        
        
    df= pd.DataFrame({
        "id":list_id,
        "title":list_names
    })

    return df