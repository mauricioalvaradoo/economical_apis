import pandas as pd
import requests



def get_data(country, series, fechaini, fechafin, frequency, database="IFS"):
 
    """ Importar multiples series de la API del IMF
    
    Parámetros
    ----------
    country: str
        Pais
    series: list
        Codigos de las series
    fechaini: str
        Fecha de inicio
    fechafin: str
        Fecha de fin
    frequency: str
        Frecuencia de series: (M, Q, A)
    database: str
        Base de datos. Default International Finance Statistics (IFS)
        Otras: Goverment Finance (GFS), Balance of Payments (BOP), entre otros
    
    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas
     
    Documentación
    ----------
    * http://www.bd-econ.com/imfapi1.html
    * https://data.imf.org/?sk=388DFA60-1D26-4ADE-B505-A05A558D9A42&sId=1479329132316
    
    
    @author: Mauricio Alvarado
    
    """
    
    df = pd.Dataframe()
    

    for i in series:
        
        base = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
        method = "CompactData"  
        
        date = f"startPeriod={fechaini}&endPeriod={fechafin}"
        url = f"{base}{method}/{database}/{frequency}.{country}.{i}?{date}"
              
        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print("Vinculacion no valida!")
            break
        
        r = r.json()["CompactData"]["DataSet"]["Series"]["Obs"]
        
        list_series = []
        for obs in r:
            list_series.append([obs.get("@TIME_PERIOD"), obs.get("@OBS_VALUE")])
        
        data = pd.DataFrame(list_series, columns=["Date", "values"])
        data["Date"] = pd.to_datetime(data["Date"])
        data["values"] = data["values"].astype('float')
    
        # Merge
        df = pd.concat([df, data]) if df.empty is True else pd.merge(df, data, how="outer")
    
    df = df.set_index("Date")
    
    return df




def get_codes(tipo, consulta=None):
    
    """ Extraer código de la consulta
    
    Parámetros
    ----------
    tipo: str
        Tipo de datos a consultar: "Indicadores", "Países", "Regiones", "Grupos"
    consulta: list
        Palabras claves de consulta

    Retorno
    ----------
    df: pd.DataFrame
        Consulta

    Documentación
    ----------
    https://www.imf.org/external/datamapper/api/help


    @author: Mauricio Alvarado
    
    """

    if tipo == "Indicadores":
        url = "https://www.imf.org/external/datamapper/api/v1/indicators"
        r = requests.get(url).json()["indicators"]
        df = get_codes_df1(r)  
    elif tipo == "Países":
        url = "https://www.imf.org/external/datamapper/api/v1/countries"
        r = requests.get(url).json()["countries"]
        df = get_codes_df2(r)  
    elif tipo == "Regiones":
        url = "https://www.imf.org/external/datamapper/api/v1/regions"
        r = requests.get(url).json()["regions"]
        df = get_codes_df2(r)
    elif tipo == "Grupos":
        url = "https://www.imf.org/external/datamapper/api/v1/groups"
        r = requests.get(url).json()["groups"]
        df = get_codes_df2(r)
    else:
        url = print("Revisa bien el tipo!")

    if consulta is not None:
            consulta = [x.lower() for x in consulta]
            
            for i in consulta:
                try:
                    filter = df["Nombres"].str.lower().str.contains(i)
                    df = df[filter]
                except:
                    pass

    return df




def get_codes_df1(r):
    codes = []
    names = []
    units = []

    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])
        units.append(i["unit"])
        
    df = pd.DataFrame({"Código": codes, "Nombres": names, "Unidades": units})

    return df




def get_codes_df2(r):
    codes = []
    names = []

    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])

    df = pd.DataFrame({"Código": codes, "Nombres": names})

    return df
