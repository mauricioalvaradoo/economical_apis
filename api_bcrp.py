import pandas as pd
import requests



def get_data(series, fechaini, fechafin):

    """ Importar multiples series de la API del BCRP
    
    Parametros
    ----------
    series: dict
        Diccionario de los códigos y nombres de las series
    
    fechaini: str
        Fecha de inicio de la serie 
        
        - Diario: yyyy-mm-dd
        - Mensual: yyyy-mm
        - Trimestral: yyyy-q
        - Anual: yyyy
    
    fechafin: str
        Fecha de fin de la serie
        
        - Diario: yyyy-mm-dd
        - Mensual: yyyy-mm
        - Trimestral: yyyy-q 
        - Anual: yyyy
        
    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas
    
    
    Ruta
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api
    
    
    @author: Mauricio Alvarado
    
    """

    keys = list(series.keys())
    
    
    df = pd.DataFrame()
    base = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
        

    for i in keys:
        url = f"{base}/{i}/json/{fechaini}/{fechafin}/ing"

        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print("Vinculacion inválida!")
            break
        
        r = r.json()
        periods = r.get("periods")
        
        values_list = []
        time_list = []
                
        for value in periods:
            value = value["values"][0]
            values_list.append(float(value))

        for time in periods:
            time = time["name"]
            time_list.append(time)
                
        dic = {"time": time_list, f"{i}": values_list}
        dic = pd.DataFrame(dic)
                            
        # Merge
        if df.empty is True:
            df = pd.concat([df, dic])
                
        else:
            df = pd.merge(df, dic, how="outer")

    df.set_index("time", inplace=True)
    df.rename(series, axis=1, inplace=True)


    # Modificaciones adicionales
    try:
        df.index = df.index.str.replace('Set', 'Sep')
    except:
        pass
    try:
        # Diarias
        df.index = pd.to_datetime(df.index, format="%d.%b.%y")
    except:
        pass
    try:
        # Mensuales
        df.index = pd.to_datetime(df.index, format="%b.%Y")
    except:
        pass
    try:
        # Trimestral
        df.index = pd.period_range(fechaini, fechafin, freq="Q")
    except:
        pass

    return df




def get_documentation(consulta, grupo=None, frecuencia=None):

    """ Extraer microdatos de la consulta
    
    Parametros
    ----------
    consulta: list
        Palabras claves de las series

    grupo: list
        Palabras claves de los grupos

    frecuencia: str
        Frecuencia de la serie consultada. Default: None.
        Opciones: "Diario", "Mensual", "Trimestral", "Anual"


    Retorno
    ----------
    df: pd.DataFrame
        Metadatos de las series consultadas
    
    
    Ruta
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/metadatos
    
    
    @author: Mauricio Alvarado
    
    """
    
    metadatos = "data/BCRPData-metadata.csv"
    df = pd.read_csv(metadatos, index_col=0, sep=";", encoding="latin-1").reset_index()
    df = df[["Código de serie", "Grupo de serie", "Nombre de serie", "Frecuencia", "Fecha de inicio", "Fecha de fin"]]
    consulta = [x.lower() for x in consulta]

    # Frecuencia
    if frecuencia is not None:
        try:
            df = df[df["Frecuencia"] == str(frecuencia)]
        except:
            pass
    
    # Grupo
    if grupo is not None:
        grupo = [x.lower() for x in grupo]
        
        for i in grupo:
            try:
                filter = df["Grupo de serie"].str.lower().str.contains(i)
                df = df[filter]
            except:
                pass

    # Series
    for i in consulta:           
        try:
            filter = df["Nombre de serie"].str.lower().str.contains(i)
            df = df[filter]
        except:
            df = print("Consulta no encontrada!")
    
    df.set_index("Código de serie", inplace=True)
    return df
