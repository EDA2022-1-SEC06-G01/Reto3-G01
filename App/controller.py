﻿"""
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
 """

import config as cf
import model
import csv
from datetime import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# =====================================
# Inicialización del Catálogo de libros
# =====================================
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog

# ================================
# Funciones para la carga de datos
# ================================
def loadData(catalog, fileName):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    fileName = cf.data_dir + fileName
    input_file = csv.DictReader(open(fileName, encoding="utf-8"),
                                delimiter=",")
    contador = 1
    for player in input_file:
        player["club_joined"] = datetime.strptime(player["club_joined"], '%Y-%m-%d')
        model.addPlayer(catalog, player)
        model.addPlayerID_playerValue(catalog, player, contador)
        model.clubName_PlayersValue(catalog, player, contador)
        contador += 1
    return catalog

# =====================
# Funciones de requerimientos
# =====================

def requerimiento1(catalog, club):
    return model.requerimiento1(catalog, club)



# =====================
# Funciones de consulta
# =====================
def getPrimerosCinco_UltimosCinco(lst):
    return model.getPrimerosCinco_UltimosCinco(lst)

def lstGet(lst, pos):
    return model.lstGet(lst, pos)


# =========================
# Funciones de ordenamiento
# =========================


# =======================================
# Funciones de consulta sobre el catálogo
# =======================================


# =========================
# Funciones para consola
# =========================
def clearConsole():
    model.clearConsole()

def exitProgram():
    model.exitProgram()