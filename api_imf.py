import pandas as pd
import requests

# pais = "GB"
# series = ["PMP_IX"]
# fechaini = "2010"
# fechafin = "2017"
# frequency = "M"


def get_imf_data(country, series, fechaini, fechafin, frequency, database="IFS"):
 
    """ Importar multiples series de la API del IMF
    
    Parametros
    ------
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
    ------
    df: pd.DataFrame
        Series consultadas
    
    
    Paises usuales
    ------
    * GB: Gran Bretaña
    
    
    Documentacion
    ------
    http://www.bd-econ.com/imfapi1.html
    https://data.imf.org/?sk=388DFA60-1D26-4ADE-B505-A05A558D9A42&sId=1479329132316
    
    
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
        
        r = r.json()["CompactData"]["DataSet"]["Series"]["Obs"]
        
        list_series = []
        for obs in r:
            list_series.append([obs.get("@TIME_PERIOD"), obs.get("@OBS_VALUE")])
        
        data = pd.DataFrame(list_series, columns=["Date", "values"])
        data["Date"] = pd.to_datetime(data["Date"])
        data["values"] = data["values"].astype('float')
    
    
        # Merge
        if df.empty is True:
            df = pd.concat([df, data])
            print(f"Has importado tu variable {i}! \n")
                
        else:
            df = pd.merge(df, data, how="outer")
            print(f"Has importado tu variable {i}! \n")
        
    
    df = df.set_index("Date")
    
    return df



def get_imf_codes(database):
    
    base = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
    method = f"DataStructure/{database}"
    url = f"{base}{method}"

    dimension_list = requests.get(url).json()\
                ['Structure']['KeyFamilies']['KeyFamily']\
                ['Components']['Dimension']
             
    
    # Extraccion de indicadores
    method = f"CodeList/{dimension_list[2]['@codelist']}"
    url = f"{base}{method}"

    code_list = requests.get(url).json()\
     	    ['Structure']['CodeLists']['CodeList']['Code']

    
    return (for code in code_list: print(f"{code['Description']['#text']}: {code['@value']}"))
