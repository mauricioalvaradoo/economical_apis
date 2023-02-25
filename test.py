## Testeo
from ecoapis import BCRP          # Hecho
from ecoapis import BM            # Hecho
from ecoapis import FRED          # Hecho
from ecoapis import IMF           # Por revisar
from ecoapis import OECD          # Por revisar
from ecoapis import YFinance      # Hecho

import warnings
warnings.simplefilter("ignore")




## BCRP ====================================================
# get_codes
consulta = BCRP.search(
    ["Interbancario"],
    grupo=["Tipo", "Cambio"],
    frecuencia="Mensual"
)
consulta

# get_data
df = BCRP.get_data(
    {
        "PN01207PM": "TC Interbancario promedio - pdp",
        "PN01205PM": "TC Interbancario compra - pdp",
        "PN01206PM": "TC Interbancario venta - pdp"
    },
    fechaini = "2000-01",
    fechafin = "2022-01"
)
df.head()

# get_documentation
metadata = BCRP.documentation("PN01207PM")
metadata




## Banco Mundial ===========================================
# get_codes
consulta = BM.search(
    ["life", "expectancy"]
)
consulta

# get_data
df = BM.get_data(
    {
        "BR": "Brasil",
        "CL": "Chile",
        "PE": "Perú"
    },
    indicator = "SP.DYN.LE60.MA.IN", # Life expectancy at age 60, male
    fechaini = "1970",
    fechafin = "2022"
)
df.head()




## FRED ====================================================
# get_codes
consulta = FRED.search(
    ["Gross", "Domestic", "Product"],
    api_key="#################################"
)
consulta

# get_data
df = FRED.get_data(
    {
        "GDPC1": "Real Gross Domestic Product s.a."
    },
    api_key="#################################",
    fechaini = "2000-01",
    fechafin = "2022-01"
)
df.head()




## IMF =====================================================
# get_codes 1 -> Serie
consulta = IMF.search(
    "Indicadores",
    consulta = ["GDP"] # Overall Fiscal Balance
)
consulta

# get_codes 2 -> País
consulta = IMF.search(
    "Países",
    consulta = ["China"] # USA
)
consulta

# get_data
df = IMF.get_data(
    {
        "USA": "United States",
        "CHN": "China"
    },
    {
        "NGDP_RPCH": "Real GDP growth"  
    },
    fechaini = "2000-01-01",
    fechafin = "2020-01-01"
    )

df




## OECD ====================================================
# get_data
df = OECD.get_data(
    identifier = "SNA_TABLE1",
    countries = 
    {
        "COL": "Colombia"
    },
    serie = "G1_PA", # Gross Product
    fechaini = "2000",
    fechafin = "2020",
    periodicidad = "Q"
)

df




## Yahoo Finance ===========================================
# get_codes
consulta = YFinance.search(
    ["Tesla"]
)
consulta

# get_data 1 -> con fecha
df = YFinance.get_data(
    {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "TSLA": "Tesla"
    },
    fechaini = "2015-01-01",
    fechafin = "2022-12-31"
)
df.tail()

# get_data 2 -> sin fecha
df = YFinance.get_data(
    {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "TSLA": "Tesla"
    }
)
df.tail()

