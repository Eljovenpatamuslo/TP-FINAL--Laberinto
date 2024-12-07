#Estructuras de datos utilizadas--
'''
**Las posiciones son todas una tupla (int,int) del modo (fila,columna)

**Las filas y columnas empiezan desde el 0

**El laberinto se representa como un diccionario con las siguientes claves:
    -Tablero: list of strings, todos los caracteres del tablero
    -Dimensiones: int, tamaño del tablero (al ser cuadrado solo se necesita un numero)
    -posActual: (int,int), Posicion en la que se encuentra en la busqueda de un camino
    -posInicial (int,int), Posicion en la que esta el inicio del laberinto ("I")
    -posDestino: (int,int), Posicion en donde se debe llegar ("X")

**El camino desde el inicio hasta el destino se representa como una lista de de posiciones ordenadas empezando desde la posicion inicial hasta la posicion del destino

'''

#Funcionamiento del algoritmo
'''
El algoritmo hace siguiente:
    -cargar los datos del laberinto del archivo generado por el programa en c en el diccionario Laberinto
    -se toma la posicion actual como la posicion inicial
    -se busca en cual de las 4 direcciones de la posicion actual esta libre, las posibles posiciones se agregan a una lista

para que una posicion este libre debe: 
    -estar en las dimensiones del tablero
    -el caracter con las coordenadas asociadas debe ser "0"
    -no debe estar ni en la lista Solucion ni en el conjunto de soluciones invalidas

Apartir de esto pueden haber dos posibilidades:
    *hay posibles posiciones para elegir:
        -se intenta ver cual de todas las posiciones esta mas cerca del objetivo (si todas estan a igual distancia se elije la primera que tomo el valor mas chico)
        -la posicion elegida se toma como la posicion actual y ademas se agrega como ultimo elemento en la lista Solucion
    *no hay ninguna posicion para elegir:
        -si no hay ninguna posicion disponible entonces se agrega la posicion a el conjunto de posiciones invalidas, la lista solucion vuelve a ser vacia y
        se toma la posicion actual como la inicial

Este proceso se va repitiendo hasta que:
    *la posicion actual sea la posicion del destino
    *no hay posiciones para elegir y la posicion actual es la inicial

En cualquiera de los dos casos se retorna la solucion que puede tener el camino o ser una lista vacia:
    *la lista es vacia:
        -vuelve a generar otro laberinto y empezar el proceso devuelta
    *la lista no es vacia: 
        -sabemos que es el camino correcto por lo que lo imprime en pantalla

        
El algoritmo NO siempre generara el camino optimo, esto se debe a que si dos posiciones estan a misma distancia del destino, el algoritmo elegira el primer valor mas bajo

Las prioridades del algoritmo son 1.ir abajo,2.ir derecha,3.ir arriba,4.ir izquierda ya que asi decidí asignar la lista de direcciones
'''

import subprocess
import platform

#recibe el diccionario Laberinto
#en la clave "Tablero" se agregan strings siendo cada string una fila del tablero
#en la clave "Dimensiones" se le asigma el largo del tablero 
def pasar_archivo_a_Tablero(Laberinto:dict) -> None:
    archivoParaLeer = "SalidaLaberinto.txt"
    archivoParaC = "EntradaLaberinto.txt"
    tipoDeEjecutable = ""
    if platform.system() == "Windows":
        tipoDeEjecutable = "./a.exe"
    else:
        tipoDeEjecutable = "./a.out"
        
    response = subprocess.run([tipoDeEjecutable, archivoParaC])
    if response.returncode != 0:
        print("error en la ejecucion")
        exit()

    with open(archivoParaLeer,"r") as archivo:
        for linea in archivo: 
            Laberinto["Tablero"].append(linea.strip('\n\r'))
    Laberinto["Dimensiones"] = len(Laberinto["Tablero"])

#toma la lista de posiciones validas y la posicion del destino y devuelve la posicion mas cercana a destino
#en caso de que dos posiciones esten a igual distancia, se retornara la primera evaluada con menor longitud
def posicion_mas_cercana_a_destino(posValidas:list, posDestino:tuple) -> tuple:
    (filaDestino,columnaDestino) = posDestino
    menorLogitud = -1
    indice = -1
    for i in range(len(posValidas)):
        longitudActual = abs(filaDestino-posValidas[i][0]) + abs(columnaDestino-posValidas[i][1])
        if menorLogitud == -1 or longitudActual < menorLogitud:
            menorLogitud = longitudActual
            indice = i
    return posValidas[indice]

#toma el Laberinto, el camino actual y las posiciones invalidas y retorna la lista de posiciones en las que se puede mover
#si no existen posiciones a las donde moverse, la funcion retornara lista vacia
def calcular_siguientes_pos(Laberinto:dict, caminoActual:list, posInvalidas:set) -> list:
    Pared = "1"
    (filaActual,columnaActual) = Laberinto["posActual"]
    Direcciones = [(1,0),(0,1),(-1,0),(0,-1)] # abajo,derecha,arriba,izquierda
    posValidas = []
    
    direccionActual=0
    while direccionActual < len(Direcciones):
        (filaDir,columnaDir) = Direcciones[direccionActual]
        (filaSumada,columnaSumada) = (filaActual + filaDir, columnaActual + columnaDir)

        if 0 <= filaSumada < Laberinto["Dimensiones"] and 0 <= columnaSumada < Laberinto["Dimensiones"]:
            caracterEnTablero = Laberinto["Tablero"][filaSumada][columnaSumada]

            if caracterEnTablero != Pared and (filaSumada,columnaSumada) not in posInvalidas and (filaSumada,columnaSumada) not in caminoActual:
                posValidas.append((filaSumada,columnaSumada))
        direccionActual+=1

    return posValidas

#toma el diccionario Laberinto y devuelve una lista que es el camino desde el inicio hasta el destino
#si devuelve una lista vacia entonces no es posible encontrar un camino con la configuracion del tablero
def buscar_solucion(Laberinto:dict) -> list:
    Laberinto["posActual"] = Laberinto["posInicial"]
    posInvalidas = set()
    caminoActual = []
    terminar = False

    while not terminar:
        caminoActual.append(Laberinto["posActual"])
        posValidas = calcular_siguientes_pos(Laberinto,caminoActual,posInvalidas)

        if posValidas != []:
            Laberinto["posActual"] = posicion_mas_cercana_a_destino(posValidas,Laberinto["posDestino"])
        else:
            if Laberinto["posActual"] == Laberinto["posInicial"]:
                terminar = True
            posInvalidas.add(Laberinto["posActual"])
            Laberinto["posActual"] = Laberinto["posInicial"]
            caminoActual = []

        (filaActual,columnaActual) = Laberinto["posActual"]
        if Laberinto["Tablero"][filaActual][columnaActual] == "X":
            caminoActual.append(Laberinto["posActual"])
            terminar = True

    return caminoActual

#toma la lista Solucion y suma 1 a cada una de las componentes
#solo sirve para mostrarlo en notacion matricial a la hora de imprimirlo
def trasnformar_a_notacion_matricial(Solucion:list) -> None:
    for i in range(len(Solucion)):
        Solucion[i] = (Solucion[i][0]+1,Solucion[i][1]+1)

#toma Laberinto y agrega a las claves "posInicial" y "posDestino" las posiciones donde se encuentran los caracteres que indican el inicio y el destino
def buscar_principio_y_final(Laberinto:dict) -> None:
    Inicio = "I"
    Destino = "X"
    obtener = 2 

    fila = 0
    while fila < Laberinto["Dimensiones"] and obtener != 0:
        columna = 0
        while columna < Laberinto["Dimensiones"] and obtener != 0:
            if Laberinto["Tablero"][fila][columna] == Inicio:
                Laberinto["posInicial"] = (fila,columna) 
                obtener -= 1

            if Laberinto["Tablero"][fila][columna] == Destino:
                Laberinto["posDestino"] = (fila,columna)
                obtener -= 1
            columna += 1
        fila += 1

#toma el Laberinto, la solucion del mismo y los intentos hasta llegar a un camino valido
 #imprime Intentos
 #Imprime cada elemento de la clave "Tablero" en Laberinto y si su posicion esta en Solucion lo imprime con fondo verde
 #Imprime la solucion             
def imprimir_informacion(Laberinto:dict, Solucion:list, Intentos:int) -> None:
    FONDO_VERDE = '\x1b[6;30;42m'
    FONDO_NORMAL = '\x1b[0m'
    print("Intentos hasta un camino valido:", Intentos)
    
    for x in range(Laberinto["Dimensiones"]):
        for y in range(Laberinto["Dimensiones"]):
            if (x,y) in Solucion:
                print(FONDO_VERDE + Laberinto["Tablero"][x][y] + FONDO_NORMAL, end = " ") #printear en verde los elementos que estan en Solucion
            else:
                print(Laberinto["Tablero"][x][y],end = " ")
        print("")

    trasnformar_a_notacion_matricial(Solucion)
    print("El camino es:",Solucion)

def main() -> None:
    Solucion = []
    Intentos = 0
    while Solucion == []:
        Laberinto = {"Tablero":[],"Dimensiones":-1,"posActual":(-1,-1),"posInicial":(-1,-1),"posDestino":(-1,-1)}
        pasar_archivo_a_Tablero(Laberinto)
        buscar_principio_y_final(Laberinto)

        Solucion = buscar_solucion(Laberinto)
        Intentos += 1

    imprimir_informacion(Laberinto,Solucion,Intentos)

if __name__ == "__main__":
    main()


#--------tests--------#

def test_posicion_mas_cercana_a_destino():
    assert (posicion_mas_cercana_a_destino([(0,1),(1,0),(2,1),(3,1)],(6,6))) == (3,1)
    assert (posicion_mas_cercana_a_destino([(0,1),(1,0),(2,1)],(6,6))) == (2,1)
    assert (posicion_mas_cercana_a_destino([(0,1),(1,0)],(6,6))) == (0,1)
    assert (posicion_mas_cercana_a_destino([(5,6),(6,5)],(6,6))) == (5,6) # si estan a misma distancia, retorna el primero que comparo
    assert (posicion_mas_cercana_a_destino([(6,5),(5,6)],(6,6))) == (6,5) # si estan a misma distancia, retorna el primero que comparo
    assert (posicion_mas_cercana_a_destino([(0,0)],(6,6))) == (0,0) # si la lista es un solo elemento devuelve ese

def test_buscar_solucion():
    #laberinto de dimension par
    Tablero = [ "I101",
                "0001",
                "0101",
                "0X01" ]
    Laberinto = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(-1,-1),"posInicial":(0,0),"posDestino":(3,1)}
    assert(buscar_solucion(Laberinto) == [(0,0),(1,0),(2,0),(3,0),(3,1)])

    #probar laberintos de dimension par imposibles
    Tablero2 = ["I101",
                "1001",
                "0101",
                "0X01" ]
    Laberinto2 = {"Tablero":Tablero2,"Dimensiones":len(Tablero2),"posActual":(-1,-1),"posInicial":(0,0),"posDestino":(3,1)}
    assert(buscar_solucion(Laberinto2) == [])

    #laberinto de dimension impar donde hay dos posibles caminos de igual longitud
    Tablero3 = ["01I10",
                "00000",
                "01110",
                "01X10",
                "00000"]
    Laberinto3 = {"Tablero":Tablero3,"Dimensiones":len(Tablero3),"posActual":(-1,-1),"posInicial":(0,2),"posDestino":(3,2)}

    assert(buscar_solucion(Laberinto3) == [(0,2),(1,2),(1,3),(1,4),(2,4),(3,4),(4,4),(4,3),(4,2),(3,2)]) 
    
    #laberinto dimension impar imposible
    Tablero4 = ["00000",
                "00I00",
                "00001",
                "00010",
                "0001X"]
    Laberinto4 = {"Tablero":Tablero4,"Dimensiones":len(Tablero4),"posActual":(-1,-1),"posInicial":(1,2),"posDestino":(4,4)}
    assert(buscar_solucion(Laberinto4) == [])

def test_calcular_siguientes_pos():
    #laberinto donde tiene una unica posicion disponible
    Tablero = [ "I101",
                "0001",
                "0001",
                "0X01" ]
    Laberinto = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(0,0),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto,[],set()) == [(1,0)])

    #laberinto donde tiene dos posiciones disponibles
    Laberinto6 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(3,2),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto6,[],set()) == [(2,2),(3,1)])

    #laberinto donde tiene tres posiciones disponibles
    Laberinto7 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(1,2),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto7,[],set()) == [(2,2),(0,2),(1,1)])

    #laberinto donde tiene cuatro posiciones disponibles
    Laberinto8 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(2,1),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto8,[],set()) == [(3,1),(2,2),(1,1),(2,0)])

    #laberinto dimension impar donde una pared hace que no se tenga ninguna posicion disponible
    Tablero2 = ["I1010",
                "10010",
                "01000",
                "0X010",
                "00100"]
    Laberinto2 = {"Tablero":Tablero2,"Dimensiones":len(Tablero2),"posActual":(0,0),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto2,[],set()) == [])

    #laberinto dimension par donde el camino hace que no tenga ninguna posicion disponible
    caminoActual3 = [(1,0)]
    Tablero3 = ["I101",
                "0001",
                "0101",
                "0X01"]
    Laberinto3 = {"Tablero":Tablero3,"Dimensiones":len(Tablero3),"posActual":(0,0),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto3,caminoActual3,set()) == [])

    #laberinto de dimension impar donde tiene una unica posicion disponible
    Tablero4 = ["I0010",
                "10010",
                "01000",
                "0001X",
                "00100"]
    Laberinto4 = {"Tablero":Tablero4,"Dimensiones":len(Tablero4),"posActual":(2,0),"posInicial":(0,0),"posDestino":(3,4)}
    assert(calcular_siguientes_pos(Laberinto4,[],set()) == [(3,0)])

    #laberinto de dimension impar donde tanto las paredes como el camino actual hacen que no tenga ninguna posicion disponible
    caminoActual5 = [(0,0),(0,1),(1,1)]
    Tablero5 = ["I0010",
                "10010",
                "00000",
                "0001X",
                "00100"]
    Laberinto5 = {"Tablero":Tablero5,"Dimensiones":len(Tablero5),"posActual":(2,1),"posInicial":(0,0),"posDestino":(3,4)}
    posInvalidas5 = set([(2,0),(2,2),(3,1)])
    assert(calcular_siguientes_pos(Laberinto5,caminoActual5,posInvalidas5) == [])