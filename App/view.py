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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


taxis_small = "taxi-trips-wrvz-psew-subset-small.csv"
taxis_medium = "taxi-trips-wrvz-psew-subset-medium.csv"
taxis_large= "taxi-trips-wrvz-psew-subset-large.csv"
total_taxis = [taxis_small]

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Top compañías")
    print("4- Top taxis")
    print("5- Mejor horario")
    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
def optionTwo():
    print("\nCargando información de rutas citybike ....")
    controller.loadFiles(analyzer, total_taxis)
    numTrips = controller.totalTrips(analyzer)
    print('Numero de viajes: ' + str(numTrips))

def optionThree():
    try:
        print('El número de componentes conectados es: ' +
              str(controller.connectedComponents(analyzer)))
        if id1.isdigit() and id2.isdigit():
            connected = controller.verticesSCC(analyzer, id1, id2)
            if connected:
                print("Las estaciones con codigo "+id1+" y "+id2+" pertenecen al mismo cluster")
            elif connected is None:
                print("No se puede hacer la busqueda, intente con estaciones diferentes")
            else:
                print("Las estaciones con codigo "+id1+" y "+id2+" no pertenecen al mismo cluster")
        else:
            print("Los ID tienen que ser un numero natural, intente con entradas diferentes")
    except:
        print("Hubo un error en la busqueda")

def optionFour():
    try:
        contador=1
        ruta=controller.getCircularRoute(analyzer, stationId, minTime, maxTime)
        print ("\n")
        print("La cantidad de rutas circulares disponibles en su tiempo conveniente son: "+str(len(ruta)))
        for i in ruta:
            print ("Ruta #"+str(contador)+":")
            print ("\n")
            for j in i:
                print ("Estación Origen: "+controller.getStationName(analyzer,j["station1"]))
                print ("Estación Destino: "+controller.getStationName(analyzer,j["station2"]))
                print ("Duración estimada: "+str(round(j["time"]))+" minutos")
                print ("\n")
            contador+=1
    except:
        print("Hubo un error en la busqueda")

def optionFive():
    try:
        if (":" not in initHour) and (":" not in endHour):
            print("Ingrese la hora en el formato valido")
        elif originArea.isdigit() and destinArea.isdigit():
            menorTime,menorRoute,hour = controller.getBestRoute(analyzer, originArea, destinArea, initHour, endHour)
            if (menorRoute == "") and (hour==0):
                print("No hay viajes entre las zonas ingresadas en el rango de tiempo ingresado. Intente de nuevo con valores distintos.")
            else:
                print("La mejor hora para movilizarse entre la Community Area "+str(originArea)+ " y la Community Area "+str(destinArea)+ " es a las "+str(hour))
                print("Con la ruta "+menorRoute+ " y con una duración de "+str(menorTime)+ " segundos")
        else:
            print("No se puede hacer la busqueda con los valores ingresados, intente con nuevos valores")
    except:
        print("Hubo un error en la busqueda")

def analizadorCargado():
    if analyzer is None:
        return False
    else:
        return True

"""
Menu principal
"""
analyzer = None
datos=False
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        analyzer = controller.init()
        print("\nAnalizador iniciado con éxito")

    elif int(inputs[0]) == 2:
        if analizadorCargado():
            executiontime = timeit.timeit(optionTwo, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
            datos = True
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")

    elif int(inputs[0]) == 3:
        if analizadorCargado() and datos:
            id1 = input('Ingrese el ID de la primera estacion: ' )
            id2 = input('Ingrese el ID de la segunda estacion: ' )
            executiontime = timeit.timeit(optionThree, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado y con datos antes de ejecutar esta opción")

    elif int(inputs[0]) == 4:
        stationId=input("Ingrese su estación de Origen: ")
        minTime=float(input("Ingrese la cantidad mínima de tiempo de la que dispone: "))
        maxTime=float(input("Ingrese la cantidad máxima de tiempo de la que dispone: "))
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        if analizadorCargado() and datos:
            originArea = input('Ingrese el ID del área de origen: ' )
            destinArea = input('Ingrese el ID del área de destino: ' )
            initHour = input('Ingrese la hora (HH:MM) menor en el rango: ' )
            endHour = input('Ingrese la hora (HH:MM) mayor en el rango: ' )
            executiontime = timeit.timeit(optionFive, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado y con datos antes de ejecutar esta opción")
    else:
        sys.exit(0)
sys.exit(0)