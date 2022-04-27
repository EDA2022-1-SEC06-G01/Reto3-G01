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


from xmlrpc.server import list_public_methods
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
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

    # No sirve para ningun requerimiento hasta ahora
    catalog['playerID_playerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 1
    catalog['clubName_PlayersValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 2
    catalog['posicionJugador_PlayerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 3
    catalog['playerTag_PlayerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # Requerimiento 4
    catalog['playerAge_playerTraits'] = om.newMap(omaptype='BST', comparefunction= compareDates)

    return catalog


# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================
def addPlayer(catalog, player):
    """
    """
    lstPlayer = lt.newList(datastructure="ARRAY_LIST", cmpfunction=None)
    player = lt.addLast(lstPlayer, player)
    lt.addLast(catalog['listaGeneral_Datos'], lstPlayer)
    return catalog

# No sirve para ningun requerimiento hasta ahora
def addPlayerID_playerValue(catalog, player, pos):
    map = catalog['playerID_playerValue']
    lst = catalog['listaGeneral_Datos']
    mp.put(map, player["sofifa_id"], lt.getElement(lst, pos))

# requerimiento 1
def clubName_PlayersValue(catalog, player, pos):
    map = catalog['clubName_PlayersValue']
    club = player["club_name"]
    exist = mp.contains(map, club)
    if exist:
        entry = mp.get(map, club)
        lst = me.getValue(entry)
    else:
        lst = lt.newList(datastructure='ARRAY_LIST')
        mp.put(map, club, lst)
    lt.addLast(lst, lt.getElement(catalog['listaGeneral_Datos'], pos))

def requerimiento1(catalog, club):
    clubPlayers = me.getValue(mp.get(catalog['clubName_PlayersValue'], club))
    ordered_map = om.newMap(comparefunction=compare_clubJoinedDate)
    for player in lt.iterator(clubPlayers):
        value = lt.getElement(player, 1)
        om.put(ordered_map, value["club_joined"], player)
    upperLimit = om.maxKey(ordered_map)
    lowerLimit = om.select(ordered_map, om.size(ordered_map)-5)
    lstPlayers = om.values(ordered_map, lowerLimit, upperLimit)
    lstSize = lt.size(lstPlayers)
    lstPlayers = sa.sort(lstPlayers, campare_requerimiento1)
    return lstPlayers, lstSize 


#requerimiento 2 - Le suma un segundo a la carga
def posicionJugador_PlayerValue(catalog, player, pos):
    map = catalog["posicionJugador_PlayerValue"]
    playerPositions = player["player_positions"]
    for position in playerPositions:
        exist = mp.contains(map, position)
        if exist:
            entry = mp.get(map, position)
            lst = me.getValue(entry)
        else:
            lst = lt.newList(datastructure='ARRAY_LIST')
            mp.put(map, position, lst)
            # cuidado iba uno abajo posible error
        lt.addLast(lst, lt.getElement(catalog['listaGeneral_Datos'], pos))

def filtroDesempenio(lst, limInferiorDesempenio, limSuperiorDesempenio):
    mapa = om.newMap(comparefunction=compare_playerOverall)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        om.put(mapa, value["overall"], player)
    players = om.values(mapa, limInferiorDesempenio, limSuperiorDesempenio)
    return players

def filtroPotential(lst, limInferiorPotencial, limSuperiorPotencial):
    mapa = om.newMap(comparefunction=compare_playerPotential)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        om.put(mapa, value["potential"], player)
    players = om.values(mapa, limInferiorPotencial, limSuperiorPotencial)
    return players

# Usado en req 2 y 3
def filtroSalario(lst, limInferiorSalario, limSuperiorSalario):
    mapa = om.newMap(comparefunction=compare_playerPotential)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        om.put(mapa, value["wage_eur"], player)
    players = om.values(mapa, limInferiorSalario, limSuperiorSalario)
    return players

def requerimiento2(catalog,
                   playerPosition,
                   limInferiorDesempenio,
                   limSuperiorDesempenio,
                   limInferiorPotencial,
                   limSuperiorPotencial,
                   limInferiorSalario,
                   limSuperiorSalario):
    lst = me.getValue(mp.get(catalog["posicionJugador_PlayerValue"], playerPosition))
    lst = filtroDesempenio(lst, limInferiorDesempenio, limSuperiorDesempenio)
    lst = filtroPotential(lst, limInferiorPotencial, limSuperiorPotencial)
    lst = filtroSalario(lst, limInferiorSalario, limSuperiorSalario)
    lst = sa.sort(lst, compare_ageAndShortName)
    lstSize = lt.size(lst)
    return lst, lstSize
    

# Requerimiento 3 - Basado en req 2 - Incrementa 0.8 seg
def playerTag_PlayerValue(catalog, player, pos):
    map = catalog["playerTag_PlayerValue"]
    tags = player["player_tags"]
    for tag in tags:
        if tag == "Unknown":
            continue
        else:
            exist = mp.contains(map, tag)
            if exist:
                entry = mp.get(map, tag)
                lst = me.getValue(entry)
            else:
                lst = lt.newList(datastructure='ARRAY_LIST')
                mp.put(map, tag, lst)
            lt.addLast(lst, lt.getElement(catalog['listaGeneral_Datos'], pos))

def requerimiento3(catalog, limInferiorSalario, limSuperiorSalario, playerTag):
    lst = me.getValue(mp.get(catalog["playerTag_PlayerValue"], playerTag))
    lst = filtroSalario(lst, limInferiorSalario, limSuperiorSalario)
    lstSize = lt.size(lst)
    lst = sa.sort(lst, campare_requerimiento3)
    return lst, lstSize




def playerAge_playerTraits(catalog, player):
    map = catalog['playerAge_playerTraits']
    dob = player['dob']
    date = dob
    exist = om.contains(map, dob)
    trait = playerTraits(player)
    if exist == 0:
        om.put(map, date, trait)
    else:
        om.put(map, date, trait)

    return map

def playerTraits(player):
    lst = lt.newList(datastructure='SINGLE_LINKED')
    traits = player['player_traits'].split()
    for trait in traits:
        if trait not in traits:
            a = trait
            lt.addLast(lst, a)
    return lst

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
# Funciones de comparacion
# ================================================================
def compare_clubJoinedDate(date1, date2):
    """
    Compara dos crimenes
    """
    if (date1 == date2):
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1

def compare_playerOverall(player1, player2):
    """
    Compara dos crimenes
    """
    if (player1 == player2):
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1

def compare_playerPotential(player1, player2):
    """
    Compara dos crimenes
    """
    if (player1 == player2):
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1


def compare_ageAndShortName(player1, player2):
    player1 = lt.getElement(player1, 0)
    player2 = lt.getElement(player2, 0)
    if player1["age"] == player2["age"]:
        return player1["short_name"] > player2["short_name"]
    else:
        return player1["age"] > player2["age"]


def campare_requerimiento1(player1, player2):
    player1 = lt.getElement(player1, 0)
    player2 = lt.getElement(player2, 0)
    if player1["club_joined"] == player2["club_joined"]:
        if player1["age"] == player2["age"]:
            if player1["dob"] == player2["dob"]:
                return player1["short_name"] > player2["short_name"]
            else:
                return player1["dob"] > player2["dob"]
        else:
            return player1["age"] > player2["age"]
    else:
        return player1["club_joined"] > player2["club_joined"]


def campare_requerimiento3(player1, player2):
    player1 = lt.getElement(player1, 0)
    player2 = lt.getElement(player2, 0)
    if player1["overall"] == player2["overall"]:
        if player1["potential"] == player2["potential"]:
            return player1["long_name"] > player2["long_name"]
        else:
            return player1["potential"] > player2["potential"]
    else:
        return player1["overall"] > player2["overall"]


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

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