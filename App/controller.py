"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(analyzer, tripsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    tripsfile = cf.data_dir + tripsfile
    input_file = csv.DictReader(open(tripsfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(analyzer, trip)
    return analyzer

def loadFiles(analyzer,totalFiles):
    """
    Carga todos los archivos
    """
    for filename in totalFiles:
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadTrips(analyzer, filename)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getBestRoute(analyzer, originArea, destinArea, initHour, endHour):
    """
    Busca la mejor ruta entre dos estaciones
    """
    originArea += ".0"
    destinArea +=".0"
    initPos = model.hourPosition(model.roundedTime(initHour))
    endPos = model.hourPosition(model.roundedTime(endHour))
    if initPos > endPos:
        x = initPos
        initPos = endPos
        endPos = x
    return model.getBestRoute(analyzer, originArea, destinArea, initPos, endPos)

def totalTrips(analyzer):
    """
    Informa la cantidad total de viajes cargados
    """
    return model.totalTrips(analyzer)
  
def getTopCompanies (analyzer):
    """
    Retorna un diccionario con un reporte general
    (total de taxis, compañias y tops de compañías de acuerdo a taxis y servicios)
    """
    model.addTaxisServices(analyzer)
    return model.getTopCompanies (analyzer)
