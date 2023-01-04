def api_bcrp(series, fechaini, fechafin):

    """
    Importar multiples series de la API del BCRP.
    De preferencia, deben ser de la misma frecuencia.
    Idealmente, este codigo es util para series diarias, donde habrán missing values en algunos dias, por lo que las series no coincidaran en longitud.
    El codigo hara "match" en aquellos valores de la misma fecha y mantendra aquellas donde no.

    @author: Mauricio Alvarado
    """

    import pandas as pd
    import requests

    """
    Formato para fechas:
    -diario: y-m-d (ej: 2013-02-20)
    -mensual: y-m (ej: 2015-05)
    -trimestral: yTt (ej: 2017T2)
    -año: y
    """


    #Importacion
    #-----------------------------------------
    df = pd.DataFrame()
    base = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
        
    #Comenzaremos con el loop    
    for i in series:
        url = f"{base}/{i}/json/{fechaini}/{fechafin}/ing"
            

        r = requests.get(url)
        
        if r.status_code == 200:
            pass
        else:
            print("Revisa los datos ingresados!")
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
                            
        # Merge al DataFrame vacio
        if df.empty is True:
            df = pd.concat([df, dic])
            print(f"Has importado tu variable {i}! \n")
                
        else:
            df = pd.merge(df, dic, how="outer")
            print(f"Has importado tu variable {i}! \n")

    df = df.set_index("time")


    # Algunas modificaciones adicionales:
    #-----------------------------------------
    try:
        df.index = df.index.str.replace('Set', 'Sep')
    except:
        pass
    try: 
        # Para series diarias
        df.index = pd.to_datetime(df.index, format="%d.%b.%y")
    except:
        pass
    try:
        # Para series mensuales
        df.index = pd.to_datetime(df.index, format="%b.%Y")
    except:
        pass

    # Ordenando el indice
    df.sort_index(inplace=True)

    
    return df

