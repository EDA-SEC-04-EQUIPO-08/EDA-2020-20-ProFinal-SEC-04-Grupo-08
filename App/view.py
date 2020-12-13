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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
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
taxis_super_small = "taxi-trips-wrvz-psew-subset-small copy.csv"
taxis_small = "taxi-trips-wrvz-psew-subset-small.csv"
taxis_medium = "taxi-trips-wrvz-psew-subset-medium.csv"
taxis_large= "taxi-trips-wrvz-psew-subset-large.csv"
total_taxis = []
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
    if ("1" in archivosCargar):
        total_taxis.append(taxis_small)
    if ("2" in archivosCargar):
        total_taxis.append(taxis_medium)
    if ("3" in archivosCargar):
        total_taxis.append(taxis_large)
    if (len(total_taxis) == 0):
        print("No se escogio ninguna opción valida, intente de nuevo.")
    else:
        print("\nCargando información de rutas ....")
        controller.loadFiles(analyzer, total_taxis)
        numTrips = controller.totalTrips(analyzer)
        print('Numero de viajes: ' + str(numTrips))
def optionThree():
    try:
        diccio=controller.getTopCompanies(analyzer)
        print ("\n")
        if topM<=len(diccio["top_taxis"]) and topN<=len(diccio["top_services"]):
            print ("El total de taxis es: "+ str(diccio["total_taxis"]))
            print ("El total de compañías es: "+ str(diccio["total_companies"])+"\n")
            print ("El top "+str(topM)+" de compañías de acuerdo a su cantidad de taxis es: \n")
            for i in range(0,topM):
                print ("#"+str(i+1))
                print (diccio["top_taxis"][i][1]+" con "+str(diccio["top_taxis"][i][0]*-1)+" taxis afiliados.\n")
            print ("\nEl top "+str(topN)+" de compañías de acuerdo a su cantidad de servicios prestados es: \n")
            for j in range(0,topN):
                print ("#"+str(j+1))
                print (diccio["top_services"][j][1]+" con "+str(diccio["top_services"][j][0]*-1)+" servicios prestados.\n")
        else:
            print("No hay suficientes datos para un top tan grande. Ingrese un valor menor.")
    except:
        print("Hubo un error en la búsqueda")
def optionFourOne():
    try:
        if n.isdigit():
            top=controller.points(analyzer, date)
            if top != None:
                topLst,size=top
                print("Los "+str(n)+" taxis con más puntos, en la fecha " +str(date)+" son: ")
                x=0
                while (x+1 <= size) and (x<int(n)):
                    puntos,id = lt.getElement(topLst,size-x)
                    print(str(x+1)+". Taxi "+str(id)+" con "+str(puntos)+" puntos.")
                    x+=1
                if x<int(n):
                    print("No hay suficientes taxis registrados en la fecha ingresada para completar el tamaño del top ingresado")
            else:
                print("No hay top de taxis para esa fecha, pruebe con otra.")
        else:
            print("La entrada tiene que ser un numero natural, intente con entradas diferentes")
    except:
        print("Hubo un error en la busqueda")
def optionFourTwo():
    try:
        if m.isdigit():
            top=controller.pointsInRange(analyzer, int(m), in_date, fi_date)
            if top != None:
                topLst,size=top
                print("Los "+str(m)+" taxis con más puntos, en el rango de fechas " +str(in_date)+"-"+str(fi_date)+" son: ")
                x=0
                while (x+1 <= size) and (x<int(m)):
                    puntos,id = lt.getElement(topLst,size-x)
                    print(str(x+1)+". Taxi "+str(id)+" con "+str(puntos)+" puntos.")
                    x+=1
                if x<int(m):
                    print("No hay suficientes taxis registrados en la fecha ingresada para completar el tamaño del top ingresado")
            else:
                print("No hay top de taxis para esa rango de fechas, pruebe con otras fechas.")
        else:
            print("La entrada tiene que ser un numero natural, intente con entradas diferentes")
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
            print("Escoja los archivos que quiere cargar: \n")
            print("1- Taxi-trips-small")
            print("2- Taxi-trips-medium")
            print("3- Taxi-trips-large")
            archivosCargar = input("Ingrese los archivos que quiere cargar(en caso de que sean más de uno, dilimitar con ,): ")
            executiontime = timeit.timeit(optionTwo, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
            datos = True
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 3:
        if analizadorCargado() and datos:
            topM=int(input("Ingrese el tamaño del top de acuerdo a cantidad de taxis: "))
            topN=int(input("Ingrese el tamaño del top de acuerdo a cantidad de servicios: "))
            executiontime = timeit.timeit(optionThree, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado y con datos antes de ejecutar esta opción")
    elif int(inputs[0]) == 4:
        if analizadorCargado() and datos:
            print("Opciones de consulta: ")
            print(" 1- Identificar los N taxis con más puntos en una fecha determinada")
            print(" 2- Identificar los M taxis con más puntos en un rango de fechas \n")
            opcion= input("Seleccione la opccion que desea consultar: ")
            if opcion=="1":
                n=input('Ingrese la cantidad, de taxis, que desea consultar: ')
                date=input("Ingrese la fecha que desea consultar, en el formato (AA-MM-DD): ")
                executiontime = timeit.timeit(optionFourOne, number=1)
                print("Tiempo de ejecución: " + str(executiontime))
            elif opcion=="2":
                m=input('Ingrese la cantidad, de taxis, que desea consultar: ')
                in_date=input("Ingrese la fecha de inicio, en el formato (AA-MM-DD): ")
                fi_date=input("Ingrese la fecha final, en el formato (AA-MM-DD): ")
                executiontime = timeit.timeit(optionFourTwo, number=1)
                print("Tiempo de ejecución: " + str(executiontime))
            else:
                print("La opcion seleccionada no es valida, intente otra opcion")
        else:
            print("Se necesita tener el analizador inicializado y con datos antes de ejecutar esta opción")
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