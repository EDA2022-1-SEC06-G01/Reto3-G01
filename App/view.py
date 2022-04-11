"""
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
from DISClib.ADT import list as lt
assert cf


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

                input("\n>Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 2:

                input("\n>Hundir cualquier tecla para continuar...")
            

            elif int(inputs[0]) == 3:
                
                input("\n>Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 4:

                input("\n>Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 5:
                
                input("\n>Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 6:
                
                input("\n>Hundir cualquier tecla para continuar...")


            elif int(inputs[0]) == 7:
                print("Cargando información de los archivos ....")

                input("\n>Hundir cualquier numero para continuar...")
            

            elif int(inputs[0]) == 8:
                controller.clearConsole()
                controller.exitProgram()
                

    except:
        print("Por favor selecciona una opcion valida")
        input("\n>Hundir cualquier numero para continuar...")
        menuPrincipal()


# ================
# Iniciar programa
# ================
menuPrincipal()
