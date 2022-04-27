﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
assert cf
from DISClib.ADT import list as lt
from prettytable import PrettyTable
from DISClib.ADT import map as mp



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Reportar las cinco adquisiciones mas recientes e un club | Requerimiento #1 (Grupal)")
    print("2- Reportar los jugadores de cierta posicion detro de un rango de desempeño, potencial y salario | Requerimiento #2 (Grupal)")
    print("3- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta | Requerimiento #3 (Individual)")
    print("4- Reportar los jugadores con cierto rasgo caracteristico y nacidos en un periodo de tiempo | Requerimiento #4 (Individual)")
    print("5- Graficar el historigrama de una propiedad para los jugadores de FIFA | Requerimiento #5 (Grupal)")
    print("6- Encontrar posibles sustituciones para los jugadores FIFA | Requerimiento #6 (Bono)")
    print("7- Cargar información en el catálogo")
    print("8- Cualquier tecla para salir")


def AskForFileSize():
    controller.clearConsole()
    print("Cual archivo te gustaria cargar?")
    print("1- Small\n" +
          "2- Large\n" +
          "3- 5%\n" +
          "4- 10%\n" +
          "5- 20%\n" +
          "6- 30%\n" +
          "7- 50%\n" +
          "8- 80%\n")
    try:
        size = int(input("> "))
        if (size < 1) or (size > 8):
            controller.clearConsole()
            print("Por favor introduzca una opcion valida")
            input("\n> Hundir cualquier tecla para continuar...")
            size = AskForFileSize()
    except:
        controller.clearConsole()
        print("Por favor introduzca una opcion valida")
        input("\n> Hundir cualquier tecla para continuar...")
        size = AskForFileSize()
    controller.clearConsole()
    return size


def getFileSize():
    file = "fifa-players-2022-utf8-"
    fileSize = AskForFileSize()
    if fileSize == 1:
        file += "small.csv"
    elif fileSize == 2:
        file += "large.csv"
    elif fileSize == 3:
        file += "5pct.csv"
    elif fileSize == 4:
        file += "10pct.csv"
    elif fileSize == 5:
        file += "20pct.csv"
    elif fileSize == 6:
        file += "30pct.csv"
    elif fileSize == 7:
        file += "50pct.csv"
    elif fileSize == 8:
        file += "80pct.csv"
    return file        


def printPrimerosCinco_UltimosCinco_Players(lstPlayers, lstSize):
    table = PrettyTable()
    table.field_names = ["Nombre", "Edad", "Altura", "Peso", "Nacionalidad", "Valor (€)", "Salario (€)", "Clausula de liberacion (€)", "Liga", "Club", "Fecha de vinculacion", "Posiciones", "Reputacion", "Tags", "Comentarios"]
    for _ in range(1, 6):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["short_name"],
                       player["age"],
                       player["height_cm"],
                       player["weight_kg"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["release_clause_eur"],
                       player["league_name"],
                       player["club_name"],
                       player["club_joined"],
                       player["player_positions"],
                       player["international_reputation"],
                       player["player_tags"],
                       player["player_traits"],
                       ])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    for _ in range(lstSize - 4, lstSize + 1):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["short_name"],
                       player["age"],
                       player["height_cm"],
                       player["weight_kg"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["release_clause_eur"],
                       player["league_name"],
                       player["club_name"],
                       player["club_joined"],
                       player["player_positions"],
                       player["international_reputation"],
                       player["player_tags"],
                       player["player_traits"],
                       ])
    return print(table.get_string())


def printRequerimiento1(lstPlayers, lstSize):
    table = PrettyTable()
    table.field_names = ["Nombre", "Edad", "Fecha de nacimiento", "Nacionalidad", "Valor Contrato", "Salario Jugador", "Valor Clausula Liberacion", "Fecha Vinculaicon a club", "Posiciones", "Comentarios", "Tags"]
    for _ in range(1, 6):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["short_name"],
                       player["age"],
                       player["dob"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["release_clause_eur"],
                       player["club_joined"],
                       player["player_positions"],
                       player["player_traits"],
                       player["player_tags"],
                       ])
    return print(table.get_string())


def printRequerimiento2(lstPlayers, lstSize):
    table = PrettyTable()
    table.field_names = ["Nombre", "Edad", "Fecha de nacimiento", "Nacioinalidad", "Valor de contrato", "Salario", "Valor clausula de liberacion", "Potencial", "Desempenio", "Posiciones del jugador", "Comentarios", "Etiquetas"]
    for _ in range(1, 4):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["short_name"],
                       player["age"],
                       player["dob"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["release_clause_eur"],
                       player["potential"],
                       player["overall"],
                       player["player_positions"],
                       player["player_traits"],
                       player["player_tags"]
                       ])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    for _ in range(lstSize - 2, lstSize + 1):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["short_name"],
                       player["age"],
                       player["dob"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["release_clause_eur"],
                       player["potential"],
                       player["overall"],
                       player["player_positions"],
                       player["player_traits"],
                       player["player_tags"]
                       ])
    return print(table.get_string())


def printRequerimiento3(lstPlayers, lstSize):
    table = PrettyTable()
    table.field_names = ["Nombre", "Edad", "Fecha de nacimiento", "Nacioinalidad", "Valor de contrato", "Salario", "club", "Liga", "Potencial", "Desempenio", "Posiciones del jugador", "Comentarios", "Etiquetas"]
    for _ in range(1, 4):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["long_name"],
                       player["age"],
                       player["dob"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["club_name"],
                       player["league_name"],
                       player["potential"],
                       player["overall"],
                       player["player_positions"],
                       player["player_traits"],
                       player["player_tags"]
                       ])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    table.add_row(["...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "...", "..."])
    for _ in range(lstSize - 2, lstSize + 1):
        player = controller.lstGet(lstPlayers, _)
        player = controller.lstGet(player, 0)
        table.add_row([player["long_name"],
                       player["age"],
                       player["dob"],
                       player["nationality_name"],
                       player["value_eur"],
                       player["wage_eur"],
                       player["club_name"],
                       player["league_name"],
                       player["potential"],
                       player["overall"],
                       player["player_positions"],
                       player["player_traits"],
                       player["player_tags"]
                       ])
    return print(table.get_string())


catalog = None

"""
Menu principal
"""
def menuPrincipal():
    try:
        while True:
            controller.clearConsole()
            printMenu()
            inputs = input('Seleccione una opción para continuar\n> ')
            controller.clearConsole()


            if int(inputs[0]) == 1:
                club = input("Por favor introduce el club que deseas buscar")
                lstPlayers, lstSize  = controller.requerimiento1(catalog, club)
                printRequerimiento1(lstPlayers, lstSize)
                
                input("\n> Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 2:
                '''
                playerPosition = input("Por favor introducir la posicion de el jugador: ")
                limInferiorDesempenio = float(input("Por favor introducir el limite inferior del desempenio: "))
                limSuperiorDesempenio = float(input("Por favor introducir el limite superior del desempenio: "))
                limInferiorPotencial = float(input("Por favor introducir el limite superior del potencial: "))
                limSuperiorPotencial = float(input("Por favor introducir el limite superior del potencial: "))
                limInferiorSalario = float(input("Por favor introducir el limite superior del salario: "))
                limSuperiorSalario = float(input("Por favor introducir el limite superior del salario: "))
                '''
                playerPosition = "CB"
                limInferiorDesempenio = 55
                limSuperiorDesempenio = 71
                limInferiorPotencial = 33
                limSuperiorPotencial = 90
                limInferiorSalario = 950
                limSuperiorSalario = 13000
                lstPlayers, lstSize = controller.requerimiento2(catalog,
                                                                playerPosition,
                                                                limInferiorDesempenio,
                                                                limSuperiorDesempenio,
                                                                limInferiorPotencial,
                                                                limSuperiorPotencial,
                                                                limInferiorSalario,
                                                                limSuperiorSalario)
                printRequerimiento2(lstPlayers, lstSize)
                input("\n> Hundir cualquier tecla para continuar...")
            

            elif int(inputs[0]) == 3:
                '''
                playerTag = input("Por favor introducir el tag que desea consultar: ")
                limInferiorSalario = float(input("Por favor introducir el limite superior del salario: "))
                limSuperiorSalario = float(input("Por favor introducir el limite superior del salario: "))
                '''
                playerTag = "#Tactician"
                limInferiorSalario = 10000
                limSuperiorSalario = 87000
                lstPlayers, lstSize = controller.requerimiento3(catalog, limInferiorSalario, limSuperiorSalario, playerTag)
                printRequerimiento3(lstPlayers, lstSize)
                input("\n> Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 4:
                
                input("\n> Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 5:
                
                input("\n> Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 6:
                
                input("\n> Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 7:
                fileSize = getFileSize()
                print("Cargando información de los archivos ....")
                import time
                start = time.process_time()
                controller.loadData(catalog, fileSize)
                lstPlayers, lstSize = controller.getPrimerosCinco_UltimosCinco(catalog["listaGeneral_Datos"])
                printPrimerosCinco_UltimosCinco_Players(lstPlayers, lstSize)
                print(time.process_time() - start)
                input("\n>Hundir cualquier numero para continuar...")
            

            elif int(inputs[0]) == 8:
                controller.clearConsole()
                controller.exitProgram()
                

    except Exception as ex:
        controller.clearConsole()
        print("Por favor selecciona una opcion valida")
        print(ex.message)
        input("\n>Hundir cualquier numero para continuar...")
        menuPrincipal()


# ================
# Iniciar programa
# ================
catalog = controller.init()
menuPrincipal()
