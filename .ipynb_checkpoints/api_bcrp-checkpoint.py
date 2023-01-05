import pandas as pd
import requests


def get_bcrp_data(series, fechaini, fechafin):

    """ Importar multiples series de la API del BCRP
    
    Parametros
    ----------
    series: list
        Lista de los codigos de las series
    
    fechaini: str
        Fecha de inicio de la serie 
        
        - Diario: yyyy-mm-dd
        - Mensual: yyyy-mm
        - Trimestral: yyyy'Q'm 
        - Anual: yyyy
    
    fechafin: str
        Fecha de fin de la serie
        
        - Diario: yyyy-mm-dd
        - Mensual: yyyy-mm
        - Trimestral: yyyy'Q'm 
        - Anual: yyyy
        
    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas
    
    
    Series usuales (nombre, frecuencia, unidad)
    ----------
    * PN02526AQ: PBI, trimestral, var% real anual
    * PN02518AQ: Consumo privado, trimestral, var% real anual
    * PN02522AQ: Inversion bruta fija - privada, trimestral , var% real anual
    * PN02524AQ: Exportaciones, trimestral , var% real anual
    * PN02525AQ: Importaciones, trimestral , var% real anual
    * PN02517AQ: Demanda interna, trimestral , var% real anual
    * PN02527AQ: Demanda interna sin inventarios, trimestral , var% real anual
    * PN02499AQ: PBI Agropecuario, trimestral , var% real anual
    * PN02501AQ: PBI Minería e hidrocarburos, trimestral , var% real anual
    * PN02502AQ: PBI Manufactura, trimestral, var% real anual
    * PN02504AQ: PBI Construcción, trimestral , var% real anual
    * PN02505AQ: PBI Comercio, trimestral , var% real anual
    * PN02506AQ: PBI Servicios, trimestral , var% real anual
    * PN01273PM: IPC, mensual, var% anual
    * PN01277PM: IPC sin alimentos y energia, mensual, var% anual
    * PN09819PM: IPC alimentos y energia, mensual, var% anual
    * PN09821PM: IPC importado, mensual, var% anual
    * PN01207PM: Tipo de cambio pdp (S/ por $US) interbancario promedio, mensual
    * PD04722MM: Tasa de referencia de politica monetaria, mensual, %
    * PN02218FM: Resultado economico del sector publico no financiero, mensual, S/ millones 
    * PD37965AM: Demanda de electricidad, mensual, var% anual
    * PD37967GM: Consumo interno de cemento, mensual, var% anual
    * PD38046AM: Indice de expectativas del sector a 3 meses, mensual, pts
    * PD38047AM: Indice de expectativas de la demanda a 3 meses, mensual, pts
    * PD12912AM: Expectativa de Inflación a 12 meses, mensual, pts
    
    
    Documentacion
    ----------
    https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api
    
    
    @author: Mauricio Alvarado
    
    """
    
    
    df = pd.DataFrame()
    base = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
        

    for i in series:
        url = f"{base}/{i}/json/{fechaini}/{fechafin}/ing"

        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print("Vinculacion no valida!")
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
            print(f"Has importado tu variable {i}! \n")
                
        else:
            df = pd.merge(df, dic, how="outer")
            print(f"Has importado tu variable {i}! \n")

    df = df.set_index("time")


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

    
    return df

