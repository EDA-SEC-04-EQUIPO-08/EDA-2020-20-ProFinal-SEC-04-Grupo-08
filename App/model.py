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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import queue as qu
from DISClib.DataStructures import edge as e
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
    """
    try:
        analyzer = {
                    "hours":lt.newList("ARRAY_LIST", compare),
                    "NumTrips": 0
                    }
        createHoursGraph(analyzer["hours"])
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def createHoursGraph(lst):
    """
    Crea un grafo para cada rango de hora en la lista
    """
    hour=-1
    min = 59
    for i in range(0,96):
        min += 15
        if min >= 60:
            hour += 1
            min = 00
        hourTime = datetime.time(hour,min)
        graph = gr.newGraph(datastructure='ADJ_LIST',
                            directed=True,
                            size=1500,
                            comparefunction=compareGraph)
        dict = {"hora":hourTime,"grafo":graph}
        lt.addLast(lst,dict)
    return lst

# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    """
    Añade informacion de cada viaje
    """
    originDate = trip['trip_start_timestamp']
    originTime =  originDate[11:]
    destinationArea = trip['dropoff_community_area']
    originArea = trip["pickup_community_area"]
    strDur = trip['trip_seconds']
    if (strDur != "") and (destinationArea != "") and (originArea != ""):
        duration = float(strDur)
        hourPos = hourPosition(originTime)
        graph = lt.getElement(analyzer["hours"],hourPos)["grafo"]
        addComunity(graph, originArea)
        addComunity(graph, destinationArea)
        addConnection(graph, originArea, destinationArea, duration)
        analyzer["NumTrips"] += 1
        

def addComunity(graph, comunity):
    """
    Adiciona una community area como un vertice del grafo
    """
    if not gr.containsVertex(graph, comunity):
            gr.insertVertex(graph, comunity)
    return graph

def addConnection(graph, origin, destination, duration):
    """
    Adiciona un arco entre dos community areas
    """
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, duration)
    else:
        weight = e.weight(edge)
        prom = (duration + weight)/2
        edge['weight'] = prom
    return graph

# ==============================
# Funciones de consulta
# ==============================

def getBestRoute(analyzer, originArea, destinArea, initPos, endPos):
    """
    Busca la mejor ruta entre dos estaciones
    """
    lst = analyzer["hours"]
    menorTime = float("inf")
    menorRoute = ""
    hour = 0
    for i in range(initPos,(endPos+1)):
        dict = lt.getElement(lst, i)
        if (gr.containsVertex(dict["grafo"], originArea)) and (gr.containsVertex(dict["grafo"], destinArea)):
            if destinArea == originArea:
                edge = gr.getEdge(dict["grafo"],originArea,destinArea)
                if edge is not None:
                    time = edge['weight']
                    if time < menorTime:
                        menorTime = time
                        menorRoute = originArea+"-"+destinArea
                        hour = dict["hora"]
            else:
                search = djk.Dijkstra(dict["grafo"],originArea)
                queuePath = djk.pathTo(search, destinArea)
                size = -1
                if queuePath is not None:
                    size = qu.size(queuePath)
                strRoute = ""
                time = 0
                for i in range(0,size):
                    stat = qu.dequeue(queuePath)
                    strRoute = strRoute + str(stat['vertexA'])+ " - "
                    time += stat['weight']
                strRoute = strRoute + stat['vertexB']
                if (time < menorTime) and (queuePath is not None):
                    menorTime = time
                    menorRoute = strRoute
                    hour = dict["hora"]
    return (menorTime,menorRoute,hour)

def totalTrips(analyzer):
    """
    Informa la cantidad total de viajes cargados
    """
    return analyzer["NumTrips"]

# ==============================
# Funciones Helper
# ==============================

def roundedTime (strTime):
    lst=strTime.split(":")
    if (int(lst[1])) <15:
        minute = "00"
    elif (int(lst[1])) <30:
        minute = "15"
    elif (int(lst[1])) <45:
        minute = "30"
    else:
        minute = "45"
    new = lst[0]+":"+minute
    return new

def hourPosition(strTime):
    lst=strTime.split(":")
    minPosDict = {"00":1,"15":2,"30":3,"45":4}
    hour = int(lst[0])
    minutes = minPosDict[lst[1]]
    pos = (hour*4)+minutes
    return pos
    
# ==============================
# Funciones de Comparacion
# ==============================

def compareGraph(vertId, keyvalueVert):
    """
    Comparacion en grafos
    """
    vertCode = keyvalueVert['key']
    if (vertId == vertCode):
        return 0
    elif (vertId > vertCode):
        return 1
    else:
        return -1

def compare(item1, item2):
    """
    Compara dos elementos
    """
    if (item1 == item2):
        return 0
    elif (item1 > item2):
        return 1
    else:
        return -1

def compareMap(keyname, entry):
    """
    Compara un nombre con una llave de una entrada
    """
    pc_entry = me.getKey(entry)
    if (keyname == pc_entry):
        return 0
    elif (keyname > pc_entry):
        return 1
    else:
        return -1