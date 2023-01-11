import pandas as pd
import yfinance as yf



def get_data(series, tipo="Close", fechaini=None, fechafin=None):

    """ Importar multiples series de la API de Yahoo Finance
    
    Parámetros
    ----------
    series: dict
        Lista de los codigos de las series y nombres
    tipo: str
        Serie consultada. Default: Close.
        Otros: Open, High, Low, AdjClose, Volume
    fechaini: datetime
        Fecha de inicio de la serie 
    fechafin: datetime
        Fecha de fin de la serie

    Retorno
    ----------
    df: pd.DataFrame
        Series consultadas
    
    Documentación
    ----------
    https://pypi.org/project/yfinance/
    
    
    Series usuales
    ----------
    * ^GSPC: S&P 500
    * ^DJI: Dow Jones Industrail Average
    * ^IXIC: Nasdaq Composite
    * ^FTSE: FTSE 100
    * ^N225: Nikkei 225
    * ^HSI: HSI
    * ^TNX: Treasury Yield 10 Years
    * DX-Y.NYB: US/USDX Index
    * EURUSD=X: EUR/USD
    
    * HG=F: Copper Futures
    * SI=F: Silver Futures
    * CL=F: Crude Oil Futures
    * GC=F: Gold Futures
    * PL=F: Platinum Futures
    * NG=F: Natural Gas Futures
    * ZC=F: Corn Futures
    * ZM=F: Soybean Meal Futures
    
    * AMZN: Amazon Inc.
    * AAPL: Apple Inc.
    * MSFT: Microsoft
    * META: Meta Platforms Inc.
    * NFLX: Netflix Inc.
    * PYPL: Paypal Holdings Inc.
    * SHOP: Shopify
    * SPOT: Spotify
    * TCEHY: Tencent Holdings Limited
    * TSLA: Tesla


    @author: Mauricio Alvarado
    
    """
    
    
    keys = list(series.keys())
    df = pd.DataFrame()
    
    for key in keys:
        data = yf.Ticker(key)
        
        try:
            data = data.history(start=fechaini, end=fechafin)
        except:
            data = data.history(period="max")  
        
        data.reset_index(inplace=True)
        data[key] = data[tipo]
    
        # Merge
        df = pd.concat([df, data[["Date", key]]]) if df.empty is True else pd.merge(df, data[["Date", key]], how="left")

    df.set_index("Date", inplace=True)
    df = df.rename(series, axis = 1)


    return df





