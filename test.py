## Testeo
import api_BCRP
import api_BM
import api_FRED
import api_IMF
import api_OECD
import api_YahooFinance


## BCRP ====================================================
# get_codes
consulta = api_BCRP.get_codes(
    ["Interbancario"],
    grupo=["Tipo", "Cambio"],
    frecuencia="Mensual"
)
consulta

# get_data
df = api_BCRP.get_data({
    "PN01207PM": "TC Interbancario promedio - pdp",
    "PN01205PM": "TC Interbancario compra - pdp",
    "PN01206PM": "TC Interbancario venta - pdp"
    },
    fechaini = "2000-01",
    fechafin = "2022-01"
)
df.head()

# get_documentation
metadata = api_BCRP.get_documentation("PN01207PM")
metadata


## Banco Mundial ===========================================


## FRED ====================================================


## IMF =====================================================
# get_codes
consulta = api_IMF.get_codes(
    "Indicadores",
    consulta = ["GDP"]
)
consulta
consulta = api_IMF.get_codes(
    "Países",
    consulta = ["Chi"]
)
consulta

# get_data
df = api_IMF.get_data(
    {
        "PER": "Peru",
        "ARG": "Argentina",
        "CHL": "Chile"
    },
    {
        "PMP_IX": "Importaciones"
    },
    fechaini = "2000",
    fechafin = "2020",
    frequency = "Q",
    tipo = "by_countries"
    )

df

## OCDE ====================================================


## Yahoo Finance ===========================================
# get_codes
consulta = api_YahooFinance.get_codes(
    ["Tesla"]
)
consulta

# get_data 1 -> con fecha
df = api_YahooFinance.get_data({
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "TSLA": "Tesla"
    },
    fechaini = "2015-01-01",
    fechafin = "2022-12-31"
)

df.tail()

# get_data 2 -> sin fecha
df = api_YahooFinance.get_data({
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "TSLA": "Tesla"
    }
)

df.tail()