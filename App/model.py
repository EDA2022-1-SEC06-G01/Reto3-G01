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
from DISClib.ADT import orderedmap as om
assert cf
import os
import time
import datetime

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
    catalog['addPlayerShortName_playerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 1
    catalog['clubName_PlayersValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 2
    catalog['posicionJugador_PlayerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # requerimiento 3
    catalog['playerTag_PlayerValue'] = mp.newMap(numelements=19000, maptype="PROBING", loadfactor=0.5, comparefunction=None)

    # Requerimiento 4
    catalog['playerAge_playerTraits'] = mp.newMap(numelements=31, maptype='PROBING', loadfactor=0.5, comparefunction=None)

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
def addPlayerShortName_playerValue(catalog, player, pos):
    map = catalog['addPlayerShortName_playerValue']
    lst = catalog['listaGeneral_Datos']
    mp.put(map, player["short_name"], lt.getElement(lst, pos))

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

    ordered_map = CrearArbolBinario(clubPlayers, "club_joined")
    
    numeroAdquisiciones = lt.size(clubPlayers)
    ligaALaQuePertenece = lt.getElement(lt.getElement(clubPlayers, 1), 1)["league_name"]
    league_level = lt.getElement(lt.getElement(clubPlayers, 1), 1)["league_name"]

    lst = om.valueSet(ordered_map)
    lst = descomprimioListaDeListas(lst)
    tamanioMatrix = lt.size(lst)

    lst = sa.sort(lst, campare_requerimiento1)

    return lst, numeroAdquisiciones, ligaALaQuePertenece, tamanioMatrix, league_level


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
        if om.contains(mapa, value["overall"]) == False:
            lst = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapa, value["overall"], lst)
        else:
            lst = me.getValue(om.get(mapa, value["overall"]))
        lt.addLast(lst, player)
    players = om.values(mapa, limInferiorDesempenio, limSuperiorDesempenio)
    return players

def filtroPotential(lst, limInferiorPotencial, limSuperiorPotencial):
    mapa = om.newMap(comparefunction=compare_playerPotential)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        if om.contains(mapa, value["potential"]) == False:
            lst = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapa, value["potential"], lst)
        else:
            lst = me.getValue(om.get(mapa, value["potential"]))
        lt.addLast(lst, player)
    players = om.values(mapa, limInferiorPotencial, limSuperiorPotencial)
    return players

# Usado en req 2 y 3
def filtroSalario(lst, limInferiorSalario, limSuperiorSalario):
    mapa = om.newMap(comparefunction=compare_generalArboles)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        if om.contains(mapa, value["wage_eur"]) == False:
            lst = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapa, value["wage_eur"], lst)
        else:
            lst = me.getValue(om.get(mapa, value["wage_eur"]))
        lt.addLast(lst, player)
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
    lst = descomprimioListaDeListas(lst)
    lst = filtroPotential(lst, limInferiorPotencial, limSuperiorPotencial)
    lst = descomprimioListaDeListas(lst)
    lst = filtroSalario(lst, limInferiorSalario, limSuperiorSalario)
    lst = descomprimioListaDeListas(lst)
    lst = sa.sort(lst, compare_requerimiento2)
    lstSize = lt.size(lst)
    totalPlayerAmmount = lt.size(catalog["listaGeneral_Datos"])
    return lst, lstSize, totalPlayerAmmount
    

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
                lst = me.getValue(mp.get(map, tag))
            else:
                lst = lt.newList(datastructure='ARRAY_LIST')
                mp.put(map, tag, lst)
            lt.addLast(lst, lt.getElement(catalog['listaGeneral_Datos'], pos))

def descomprimioListaDeListas(lst):
    lstNueva = lt.newList(datastructure="ARRAY_LIST")
    for _ in range(lt.size(lst)):
        lista1 = lt.getElement(lst, _ + 1)
        for i in range(lt.size(lista1)):
            lt.addLast(lstNueva, lt.getElement(lista1, i + 1))
    return lstNueva

def requerimiento3(catalog, limInferiorSalario, limSuperiorSalario, playerTag):
    lst = me.getValue(mp.get(catalog["playerTag_PlayerValue"], playerTag))
    lst = filtroSalario(lst, limInferiorSalario, limSuperiorSalario)

    lst = descomprimioListaDeListas(lst)
    
    lstSize = lt.size(lst)
    lst = sa.sort(lst, campare_requerimiento3)
    return lst, lstSize

#Requerimiento 4

def playerAge_playerTraits(catalog, player, pos):
    """
    """
    map = catalog['playerAge_playerTraits']
    traits = player['player_traits']
    i = 0

    while i < len(traits):
        exist = mp.contains(map, traits[i])
        if exist == True:
           entry = mp.get(map, traits[i])
           lst = me.getValue(entry)
            
        else:
           lst = lt.newList('ARRAY_LIST') 
           mp.put(map, traits[i], lst)
        lt.addLast(lst, lt.getElement(catalog['listaGeneral_Datos'], pos))
        i += 1

    return catalog

def requerimiento4(catalog, lim_inf, lim_sup, trait):
    pareja = mp.get(catalog['playerAge_playerTraits'],trait)
    lst = me.getValue(pareja)
    lst = arbol_req4(lst, lim_inf, lim_sup)
    lstSize = lt.size(lst)
    lst = sa.sort(lst, campare_requerimiento3)
    return lst, lstSize

def arbol_req4(lst, limInferiorDob, limSuperiorDob):
    mapa = om.newMap(comparefunction=compareDates)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        om.put(mapa, value["dob"], player)
    players = om.values(mapa, limInferiorDob, limSuperiorDob)
    return players

# Requerimiento 5
def requerimiento5(catalog, segmentos, niveles, propiedad):
    lstJugadores = catalog["listaGeneral_Datos"]
    lstSizeJugadores = lt.size(lstJugadores)
    mapa = om.newMap(omaptype="RBT", comparefunction=compare_generalArboles)
    for _ in lt.iterator(lstJugadores):
        valor = lt.getElement(_, 0)
        existe = om.contains(mapa, valor[propiedad.lower()])
        if existe == True:
            llave = me.getValue(om.get(mapa, valor[propiedad.lower()]))
            llave += 1
            om.put(mapa, valor[propiedad.lower()], llave)
        else:
            om.put(mapa, valor[propiedad.lower()], 1)

    minKey = om.minKey(mapa)
    maxKey = om.maxKey(mapa)
    sizeMapa = om.size(mapa)
    sizeMapa = lt.size(lstJugadores) # verificar
    razonDeCambio = (maxKey - minKey) / segmentos
    lstConteo = lt.newList(datastructure="ARRAY_LIST")
    i = 0
    min = None
    max = None
    while i < 7:
        if i == 0:
            min = minKey
            max = min + razonDeCambio
            floor_max = om.floor(mapa, max)
        elif i == 6:
            min = max
            max = maxKey
            floor_max = max
        else:
            min = max
            max = min + razonDeCambio
            floor_max = om.floor(mapa, max)
        
        number = om.values(mapa, min, floor_max)
        contador = 0
        for _ in lt.iterator(number):
            contador += _
        lt.addLast(lstConteo, contador)
        i += 1
    lstMark = lt.newList(datastructure="ARRAY_LIST")
    for _ in lt.iterator(lstConteo):
        lt.addLast(lstMark, _ // niveles)
    return lstSizeJugadores, sizeMapa, razonDeCambio, lstConteo, lstMark, minKey, maxKey


def requerimiento6(catalog, playerShortName, posicion):
    posicionJugadores = catalog["posicionJugador_PlayerValue"]
    shortName_PlayerValue = catalog["addPlayerShortName_playerValue"]
    jugadorPorRemplazar = me.getValue(mp.get(shortName_PlayerValue, playerShortName))
    lstPosicionJugadores = me.getValue(mp.get(posicionJugadores, posicion))
    mapaPotential = om.newMap(omaptype="RBT", comparefunction=compare_generalArboles)
    mapaAge = om.newMap(omaptype="RBT", comparefunction=compare_generalArboles)
    mapaHeight = om.newMap(omaptype="RBT", comparefunction=compare_generalArboles)
    mapaPosition = om.newMap(omaptype="RBT", comparefunction=compare_generalArboles)
    for _ in lt.iterator(lstPosicionJugadores):
        value = lt.getElement(_, 1)
        existe = om.contains(mapaPotential,value["potential"])
        if existe == True:
            lst = me.getValue(om.get(mapaPotential, value["potential"]))
        else:
            lst = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapaPotential, value["potential"], lst)
        lt.addLast(lst, _)


    print(jugadorPorRemplazar)
    print()
    print(lstPosicionJugadores)
    input("llegamos al 6")


# ================================
# Funciones para creacion de datos
# ================================

def CrearArbolBinario(lst, llave):
    mapa = om.newMap(comparefunction=compare_generalArboles)
    for player in lt.iterator(lst):
        value = lt.getElement(player, 1)
        if om.contains(mapa, value[llave]) == False:
            lst_new = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapa, value[llave], lst_new)
        else:
            lst_new = me.getValue(om.get(mapa, value[llave]))
        lt.addLast(lst_new, player)
    return mapa

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

def compare_generalArboles(player1, player2):
    """
    Compara dos crimenes
    """
    if (player1 == player2):
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1

def compare_requerimiento2(player1, player2):
    player1 = lt.getElement(player1, 1)
    player2 = lt.getElement(player2, 1)
    if player1["overall"] == player2["overall"]:
        if player1["potential"] == player2["potential"]:
            if player1["wage_eur"] == player2["wage_eur"]:
                if player1["age"] == player2["age"]:
                    return player1["short_name"] > player2["short_name"]
                else:
                    return player1["age"] > player2["age"]
            else:
                return player1["wage_eur"] > player2["wage_eur"]
        else:
            return player1["potential"] > player2["potential"]
    else:
        return player1["overall"] > player2["overall"]


def campare_requerimiento1(player1, player2):
    player1 = lt.getElement(player1, 1)
    player2 = lt.getElement(player2, 1)
    clubJoined1 = time.strptime(player1['club_joined'], "%Y-%m-%d")
    clubJoined2 = time.strptime(player2['club_joined'], "%Y-%m-%d")
    dob1 = player1['dob'].timestamp()
    dob2 = player2['dob'].timestamp()
    
    if clubJoined1 == clubJoined2:
        if player1['age'] == player2['age']:
            if dob1 == dob2:
                return player1['short_name'] > player2['short_name']
            else:
                return dob1 > dob2
        else:
            return player1['age'] > player2['age']
    else:
        return clubJoined1 > clubJoined2


def campare_requerimiento3(player1, player2):
    player1 = lt.getElement(player1, 0)
    player2 = lt.getElement(player2, 0)
    if player1["wage_eur"] == player2["wage_eur"]:
        if player1["overall"] == player2["overall"]:
            if player1["potential"] == player2["potential"]:
                return player1["long_name"] > player2["long_name"]
            else:
                return player1["potential"] > player2["potential"]
        else:
            return player1["overall"] > player2["overall"]
    else:
        return player1["wage_eur"] > player2["wage_eur"]

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    date1 = date1.timestamp()
    date2 = date2.timestamp()
    if (date1 == date2):
            return 0
    elif date1 > date2:
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