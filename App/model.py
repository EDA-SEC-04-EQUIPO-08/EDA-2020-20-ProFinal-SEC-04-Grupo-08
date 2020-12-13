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
from DISClib.ADT import minpq as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import queue as qu
from DISClib.DataStructures import edge as e
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import heap as hp
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
                    "companies":{
                                "list":lt.newList("ARRAY_LIST",compare),
                                "taxis":lt.newList("ARRAY_LIST",compare),
                                "total_taxis":mp.newMinPQ(compare),
                                "total_services":mp.newMinPQ(compare),
                                "diccio":{"top_taxis":[],"top_services":[]}},
                    "NumTrips": 0,
                    "NumTaxis": 0,
                    "date":m.newMap(1000,
                                   maptype='CHAINING',
                                   loadfactor=5,
                                   comparefunction=compareMap),
                    "list_dates":lt.newList("ARRAY_LIST", compare),
                    "arbol_dates":om.newMap(omaptype='RBT',
                                      comparefunction=compare)
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
    inicial_date = originDate[:10]
    destinationArea = trip['dropoff_community_area']
    originArea = trip["pickup_community_area"]
    strDur = trip['trip_seconds']
    company = trip['company']
    taxi = trip['taxi_id']
    millas = trip["trip_miles"]
    total_money = trip["trip_total"]
    if (total_money!="") and (millas!="") and (float(millas)!=0) and (float(total_money)!=0):
        addDate(analyzer, inicial_date, float(millas), float(total_money), taxi)
    if (strDur != "") and (destinationArea != "") and (originArea != ""):
        duration = float(strDur)
        hourPos = hourPosition(originTime)
        graph = lt.getElement(analyzer["hours"],hourPos)["grafo"]
        addComunity(graph, originArea)
        addComunity(graph, destinationArea)
        addConnection(graph, originArea, destinationArea, duration)
        addCompanyTaxis(analyzer,company,taxi)
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

def addCompanyTaxis (analyzer, company, taxi):
    lst=analyzer["companies"]
    if lt.isPresent(lst["list"],company)>0:
        iterator=it.newIterator(lst["taxis"])
        while it.hasNext(iterator):
            element=it.next(iterator)
            if element["company"] == company:
                element["services"]+=1
                if lt.isPresent(element["taxis_id"],taxi)==0:
                    lt.addLast(element["taxis_id"],taxi)
    else:
        dicc={"company":company, "taxis_id":lt.newList("ARRAY_LIST",compare), "services":1}
        lt.addLast(dicc["taxis_id"],taxi)
        lt.addLast(lst["list"],company)
        lt.addLast(lst["taxis"],dicc)

def addTaxisServices (analyzer):
    iterator=it.newIterator(analyzer["companies"]["taxis"])
    while it.hasNext(iterator):
        company=it.next(iterator)
        mp.insert(analyzer["companies"]["total_taxis"],(lt.size(company["taxis_id"])*-1),company["company"])
        mp.insert(analyzer["companies"]["total_services"],(company["services"])*-1,company["company"])
        analyzer["NumTaxis"]+=lt.size(company["taxis_id"])
    for i in range(0,mp.size(analyzer["companies"]["total_taxis"])):
        analyzer["companies"]["diccio"]["top_taxis"].append(mp.delMin(analyzer["companies"]["total_taxis"]))
    for j in range (0,mp.size(analyzer["companies"]["total_services"])):
        analyzer["companies"]["diccio"]["top_services"].append(mp.delMin(analyzer["companies"]["total_services"]))

def addDate(analyzer, inicial_date, millas, money, idTaxi):
    """
    Adiciona una fecha al mapa
    """
    mapa=analyzer["date"]
    if m.get(mapa,inicial_date) == None:
        lt.addLast(analyzer["list_dates"], inicial_date)
        value={"map":m.newMap(1000,
                        maptype='CHAINING',
                        loadfactor=5,
                        comparefunction=compareMap),
                "taxis":lt.newList("ARRAY_LIST",compare)
                }
        m.put(value["map"],idTaxi,{"idTaxi": idTaxi, "millas": millas, "money": money, "services": 1})
        #print(value["map"],"1")
        lt.addLast(value["taxis"],idTaxi)
        #print(value["taxis"],"2")
        m.put(mapa, inicial_date, value)
        #print(mapa,"3")
    else:
        changeDateInfo(mapa, inicial_date, millas, money, idTaxi)

def changeDateInfo(mapa, inicial_date, millas, money, idTaxi):
    fecha = m.get(mapa,inicial_date)
    fechaDict = me.getValue(fecha)
    taxi = m.get(fechaDict["map"],idTaxi)
    if taxi == None:
        m.put(fechaDict["map"],idTaxi,{"idTaxi": idTaxi, "millas": millas, "money": money, "services": 1})
        lt.addLast(fechaDict["taxis"],idTaxi)
    else:
        taxiDict = me.getValue(taxi)
        taxiDict["millas"]+=millas
        taxiDict["money"]+=money
        taxiDict["services"]+=1
    #print(fecha,"4")
    #print(fechaDict["taxis"],"5")
    #print(taxi,"6")

def orderPoints(analyzer):
    lista=analyzer["list_dates"]
    #print(lista,"7")
    mapa= analyzer["date"]
    #print(mapa,"8")
    arbol= analyzer["arbol_dates"]
    for i in range(1, lt.size(lista)+1):
        date=lt.getElement(lista, i)
        #print(date,"9")
        taxis=me.getValue(m.get(mapa, date))
        #print(taxis,"10")
        taxisLst = taxis["taxis"]
        #print(taxisLst,"11")
        taxisMap = taxis["map"]
        #print(taxisMap,"12")
        max_pq=hp.newHeap(compare)
        for j in range (1, lt.size(taxisLst)+1):
            taxiId = lt.getElement(taxisLst,j)
            #print(taxiId,"13")
            taxiDict = me.getValue(m.get(taxisMap,taxiId))
            #print(taxiDict,"14")
            point=(taxiDict["millas"]/taxiDict["money"])*taxiDict["services"]
            #print(point,"15")
            hp.insertMax(max_pq,point, taxiId)
        #print(max_pq,"16")
        lst = max_pq['elements']
        #print(lst,"17")
        size = lt.size(lst)
        #print(size,"18")
        while size>1:
            lt.exchange(lst,1,size)
            size -=1
            sinksort(lst,1,size)
        #print(lst,"19")
        om.put(arbol,date, lst)
    #print(arbol,"20")
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

def getTopCompanies (analyzer):
    heap=analyzer["companies"]["diccio"]
    diccio={"total_taxis":analyzer["NumTaxis"],"total_companies":lt.size(analyzer["companies"]["list"]),"top_taxis":heap["top_taxis"],"top_services":heap["top_services"]}
    return diccio

def points(analyzer, date):
    arbol=analyzer["arbol_dates"]
    print(arbol,"21")
    lista=om.get(arbol, date)["value"]
    print(lista,"22")
    if lista is None:
        return None
    return (lista,lt.size(lista))

def pointsInRange(analyzer, n, in_date, fi_date):
    arbol=analyzer["arbol_dates"]
    taxis = lt.newList("ARRAY_LIST",compare)
    lista=om.values(arbol, in_date, fi_date)
    if lt.isEmpty(lista):
        return None
    iterator=it.newIterator(lista)
    mapTaxis = m.newMap(100,maptype='CHAINING',loadfactor=5,comparefunction=compareMap)
    while it.hasNext(iterator):
        date=it.next(iterator)
        for i in range(1,lt.size(date)+1):
            element = lt.getElement(date,i)
            num,taxiId = element
            entry = m.get(mapTaxis,taxiId)
            if entry == None:
                lt.addLast(taxis, taxiId)
                m.put(mapTaxis,taxiId,num)
            else:
                num2 = entry["value"]
                numNew = num2 + num
                entry["value"] = numNew
    max_pq=hp.newHeap(compare)
    for j in range (1, lt.size(taxis)+1):
        taxiId = lt.getElement(taxis,j)
        points = me.getValue(m.get(mapTaxis,taxiId))
        hp.insertMax(max_pq,points, taxiId)
    lst = max_pq['elements']
    size = lt.size(lst)
    while size>1:
        lt.exchange(lst,1,size)
        size -=1
        sinksort(lst,1,size)
    return (lst,lt.size(lst))
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

def sinksort (lst, pos, size):
    if (2*pos>size):
        return lst
    dad = lt.getElement(lst,pos)
    left = lt.getElement(lst,2*pos)
    right = lt.getElement(lst,(2*pos)+1)
    if ((2*pos)+1 > size):
        num,id = left
        right = ((num-1),id)
    if ((dad > left) and (dad > right)):
        return lst
    else:
        if left >= right:
            lt.exchange(lst,2*pos,pos)
            sinksort(lst,2*pos,size)
        else:
            lt.exchange(lst,(2*pos)+1,pos)
            sinksort(lst,(2*pos)+1,size)
    return lst

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
