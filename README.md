# Vinculación a las APIs de las principales instituciones económicas
El proyecto fue desarrollado por Mauricio Alvarado y Andrei Romero.

## Objetivo:
Vincularse con las APIs:
1. BCRP
2. YahooFinance
3. FRED
4. IMF
5. WorldBank
6. OCDE

</br>
<p align="center">
      <img src="figures/bcrp-logo.png" width="150" align="left">
      <img src="figures/yahoo-finance-logo.png" width="200">
      <img src="figures/imf-logo.png" width="150" align="right">
</p>
<p align="center">
      <img src="figures/fred-logo.png" width="150" align="left">
      <img src="figures/world-bank-logo.png" width="200">
      <img src="figures/ocde-logo.png" width="200" align="right">
</p>
</br> </br> </br> </br> </br>


## Métodos
Cada código tiene dos funciones comunes. La primera es:
```
get_data()
```
Sirve para extraer las series dado el periodo definidos en los insumos.

La segunda es: 
```
get_codes()
```
Dado palabras claves, se consigue la metadata asociada. Esto incluye principalmente los nombres de las series y códigos que servirán como complemento con la función anterior `get_data()`.

