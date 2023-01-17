import pandas as pd
import requests



def get_data(countries, series, fechaini, fechafin, frequency, tipo="by_countries", database="IFS"):
 
    """ Importar multiples series de la API del IMF
    
    Parámetros
    ----------
    countries: dict
        Códigos de países
    series: dict
        Codigos de las series
    fechaini: str
        Fecha de inicio
    fechafin: str
        Fecha de fin
    frequency: str
        Frecuencia de series: (M, Q, A)
    tipo: str
        Tipo de pedido. Default: by_countries
        - by_countries: Varios países y una serie
        - by_series: Un país y varias series
    database: str
        Base de datos. Default: International Finance Statistics (IFS)
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
    
    df = pd.DataFrame()

    base = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
    method = "CompactData"
    date = f"startPeriod={fechaini}&endPeriod={fechafin}"
    

    if tipo == "by_countries":
        
        serie = list(series.keys())[0]
        countries = list(countries.keys())

        for i in countries:
        
            url = f"{base}{method}/{database}/{frequency}.{i}.{serie}" # ?{date}"   
            r = requests.get(url)         
            response = r.json()#["CompactData"]["DataSet"]#["Series"]["Obs"]
            
            # list_series = []
            # for obs in response:
            #     list_series.append([obs.get("@TIME_PERIOD"), obs.get("@OBS_VALUE")])
            
            # data = pd.DataFrame(list_series, columns=["Date", "values"])
            # data["Date"] = pd.to_datetime(data["Date"])
            # data["values"] = data["values"].astype('float')
        
            # # Merge
            # df = pd.concat([df, data]) if df.empty is True else pd.merge(df, data, how="outer")
    

    # if tipo == "by_series":

    #     country = list(countries.keys())[0]
    #     series = list(series.keys())

    #     for i in series:

    #         url = f"{base}{method}/{database}/{frequency}.{country}.{i}?{date}"
    #         r = requests.get(url)
    #         response = r.json()["CompactData"]["DataSet"]["Series"]["Obs"]
            
    #         list_series = []
    #         for obs in response:
    #             list_series.append([obs.get("@TIME_PERIOD"), obs.get("@OBS_VALUE")])
            
    #         data = pd.DataFrame(list_series, columns=["Date", "values"])
    #         data["Date"] = pd.to_datetime(data["Date"])
    #         data["values"] = data["values"].astype('float')
        
    #         # Merge
    #         df = pd.concat([df, data]) if df.empty is True else pd.merge(df, data, how="outer")
        
    
    
    # df = df.set_index("Date")
    
    return response




def get_codes(tipo, consulta=None):
    
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


def get_codes_df1(r):
    codes = []
    names = []
    units = []

    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])
        units.append(i["unit"])
            
    df1 = pd.DataFrame({"Código": codes, "Nombres": names, "Unidades": units})

    return df1

def get_codes_df2(r):
    codes = []
    names = []

    for i in list(r.keys()):
        codes.append(i)
    for i in list(r.values()):
        names.append(i["label"])
        
    df2 = pd.DataFrame({"Código": codes, "Nombres": names})

    return df2

    
