import cryptocompare
import requests
# para en un futuro hacerlo por terminal     
import argparse
from pyfiglet import Figlet
from colors import bcolors

# API crypto url 
URL = "https://min-api.cryptocompare.com/data"

def showMenu():
    print("Escoja el servicio deseado: ")
    print("\n\t [" + f"{bcolors.OKCYAN}a{bcolors.ENDC}" + "]: Top crypto-monedas por valor de mercado")
    print("\n\t [" + f"{bcolors.OKCYAN}b{bcolors.ENDC}" + "]: Precio de una cripto-moneda en base otra(s) moneda(s)")
    print("\n\t [" + f"{bcolors.OKCYAN}q{bcolors.ENDC}" + "]: Cerrar menú")

def topCoins(numero, ruta):
    # Ruta con esa cantidad de coins
    ruta = ruta.replace("$topcoins",numero)
    # request 
    x = requests.get(URL+ruta)
    print()
    for i in range(0, int(numero)):
        moneda = x.json()["Data"][i]["CoinInfo"]["Name"]
        valor_mercado = x.json()["Data"][i]["DISPLAY"]["USD"]["MKTCAP"]
        simbolo = valor_mercado[0]
        valor_mercado = valor_mercado.split(" ")
        unidad_medida = valor_mercado[2]
        valor_mercado = valor_mercado[1]
        valor_mercado = valor_mercado +  unidad_medida + " " + simbolo
        print("\t\t" + str(i+1) + ".- " + f"{moneda:<8}{valor_mercado:>10}")
    print()

def compareCripto(cripto, compare):
    # nos construimos el endpoint bueno
    endpoint = "/price?fsym=$moneda&tsyms=$comparaciones"
    endpoint = endpoint.replace("$moneda",cripto)
    endpoint = endpoint.replace("$comparaciones",compare)
    # request
    x = requests.get(URL+endpoint)
    print()
    # iteramos
    for criptomoneda,valor in x.json().items():
        print("\t\t 1 " + cripto + " = " + f"{valor:<10}{criptomoneda:<40}")
    print()


# banner
custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Crypto Compare'))

acabar = False
while (not acabar):
    showMenu()
    resultado = input("\n" + f"{bcolors.BOLD}Elección{bcolors.ENDC}: ")
    if resultado in ["a","b","q"]:
        if resultado == "a":
            # ¿Cuántas criptos quiere que le mostremos por pantalla?
            numero = input("\n\t [*] Cantidad de crypto-monedas en la lista (1-100): ")
            topCoins(numero, "/top/mktcapfull?limit=$topcoins&tsym=USD")
        elif resultado == "b":
            cripto = input("\n\t [*] Introduzca la cripto-moneda: ")
            cripto = cripto.upper()
            comparaciones = input("\n\t [*] Introduzca las monedas con las que desea comparar " + cripto+ " (si son varias, separe por comas): ")
            comparaciones = comparaciones.upper()
            compareCripto(cripto, comparaciones)
        elif resultado == "q":
            print("\nCerrando servicio. Espero que le haya sido de utilidad!\n")
            acabar = True
        
    else:
        print("\n" + f"{bcolors.FAIL}Opción inválida{bcolors.ENDC}\n")
        
