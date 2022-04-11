"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import os

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# =======================
# Construccion de modelos
# =======================

def newCatalog():
    """ 
    Crear un nuevo catalogo
    """
    catalog = {'listaGeneral_Datos': None,
                }

    catalog['listaGeneral_Datos'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=None)

    return catalog


# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================
def addPlayer(catalog, player):
    """
    """
    lt.addLast(catalog['listaGeneral_Datos'], player)
    return catalog


# ================================
# Funciones para creacion de datos
# ================================


# =====================
# Funciones de consulta
# =====================
def getPrimerosCinco_UltimosCinco(lst):
    players = lt.newList()
    lstSize = lt.size(lst)
    for _ in range(1, 6):
        player = lt.getElement(lst, _)
        lt.addLast(players, player)
    for _ in range(lstSize - 4, lstSize + 1):
        player = lt.getElement(lst, _)
        lt.addLast(players, player)
    lstSize = lt.size(players)
    return players, lstSize

def lstGet(lst, pos):
    return lt.getElement(lst, pos)
        



# ================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# ================================================================


# =========================
# Funciones de ordenamiento
# =========================


# =========================
# Funciones para consola
# =========================
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def exitProgram():
    os._exit(1)