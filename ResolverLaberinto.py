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
import subprocess
import platform

#recibe el Laberinto y:
#en la clave "Tablero" se agregan strings siendo cada string una fila del tablero
#en la clave "Dimensiones" se le asigma el largo del tablero 
def obtener_dimensiones_y_tablero_de_archivo(Laberinto:dict) -> None:
    archivoParaLeer = "SalidaLaberinto.txt"
    archivoParaC = "EntradaLaberinto.txt"
    tipoDeEjecutable = ""
    if platform.system() == "Windows":
        tipoDeEjecutable = "./a.exe"
    else:
        tipoDeEjecutable = "./a.out"
        
    response = subprocess.run([tipoDeEjecutable, archivoParaC, archivoParaLeer])
    if response.returncode != 0:
        print("error en la ejecucion")
        exit()

    with open(archivoParaLeer,"r") as archivo:
        for linea in archivo: 
            Laberinto["Tablero"].append(linea.strip('\n\r'))
    Laberinto["Dimensiones"] = len(Laberinto["Tablero"])

#toma las posiciones validas, la posicion del destino y devuelve la posicion mas cercana al destino
#en caso de que dos posiciones esten a igual distancia, se retorna la primera que se evaluo con menor longitud
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

#toma el Laberinto, el camino actual y las posiciones invalidas y retorna la lista de posiciones a las que se puede mover
#si no existen posiciones a las donde moverse, la funcion retorna una lista vacia
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

#toma el Laberinto y devuelve una la solucion de ese laberinto
#si devuelve una lista vacia entonces no es posible encontrar un camino con la configuracion del tablero
def buscar_solucion(Laberinto:dict) -> list:
    Laberinto["posActual"] = Laberinto["posInicial"]
    posInvalidas = set()
    caminoActual = []
    posValidas = []
    terminar = False
    Destino = "X"

    caminoActual.append(Laberinto["posActual"])
    while not terminar:
        posValidas = calcular_siguientes_pos(Laberinto,caminoActual,posInvalidas)
        if posValidas != []:
            Laberinto["posActual"] = posicion_mas_cercana_a_destino(posValidas,Laberinto["posDestino"])
            caminoActual.append(Laberinto["posActual"])
        elif Laberinto["posActual"] != Laberinto["posInicial"]:
            posInvalidas.add(Laberinto["posActual"])
            caminoActual.remove(Laberinto["posActual"])
            Laberinto["posActual"] = caminoActual[-1]
        else:
            terminar = 1
            caminoActual = []

        (filaActual,columnaActual) = Laberinto["posActual"]
        if Laberinto["Tablero"][filaActual][columnaActual] == Destino:
            terminar = True

    return caminoActual

#toma la solucion y suma 1 a cada una de las componentes
#solo sirve para mostrarlo en notacion matricial a la hora de imprimirlo
def trasnformar_a_notacion_matricial(Solucion:list) -> None:
    for i in range(len(Solucion)):
        (filaActual,columnaActual) = Solucion[i]
        Solucion[i] = (filaActual+1,columnaActual+1)

#toma Laberinto y agrega a las claves "posInicial" y "posDestino" las posiciones donde se encuentran los caracteres que indican el inicio y el destino
def buscar_principio_y_final(Laberinto:dict) -> None:
    Inicio = "I"
    Destino = "X"
    posParaEncontrar = 2
    posEncontradas = 0

    fila = 0
    while fila < Laberinto["Dimensiones"] and posEncontradas != posParaEncontrar:
        columna = 0
        while columna < Laberinto["Dimensiones"] and posEncontradas != posParaEncontrar:
            if Laberinto["Tablero"][fila][columna] == Inicio:
                Laberinto["posInicial"] = (fila,columna) 
                posEncontradas += 1

            if Laberinto["Tablero"][fila][columna] == Destino:
                Laberinto["posDestino"] = (fila,columna)
                posEncontradas += 1
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
    print("Tablero:")
    for Fila in range(Laberinto["Dimensiones"]):
        for Columna in range(Laberinto["Dimensiones"]):
            if (Fila,Columna) in Solucion:
                print(FONDO_VERDE + Laberinto["Tablero"][Fila][Columna] + FONDO_NORMAL, end = " ") #printear en verde los elementos que estan en Solucion
            else:
                print(Laberinto["Tablero"][Fila][Columna],end = " ")
        print("")

    trasnformar_a_notacion_matricial(Solucion)
    print("El camino es:",Solucion)

def main() -> None:
    Solucion = []
    Intentos = 0
    Laberinto = {"Tablero":[],"Dimensiones":-1,"posActual":(-1,-1),"posInicial":(-1,-1),"posDestino":(-1,-1)}
    while Solucion == []:
        Laberinto["Tablero"] = []
        obtener_dimensiones_y_tablero_de_archivo(Laberinto)

        #este if se hace para no llamar a la funcion buscar_principio_y_final cada vez que se hace un nuevo intento
        #ya que tiene que pasar por todos los elementos de tablero por una informacion que ya se conoce
        if Intentos == 0:
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

    #laberinto de dimension par imposible
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

    #laberinto de dimension par donde hay dos posibles caminos de igual longitud
    Tablero5 = ["1111",
                "0I01",
                "0101",
                "0X01"]
    Laberinto5 = {"Tablero":Tablero5,"Dimensiones":len(Tablero5),"posActual":(-1,-1),"posInicial":(1,1),"posDestino":(3,2)}
    assert(buscar_solucion(Laberinto5) == [(1,1),(1,2),(2,2),(3,2),(3,1)])

def test_calcular_siguientes_pos():
    #laberinto donde tiene una unica posicion disponible
    Tablero = [ "I101",
                "0001",
                "0001",
                "0X01" ]
    caminoActual = []
    posInvalidas = set()
    Laberinto = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(0,0),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto,caminoActual,posInvalidas) == [(1,0)])

    #laberinto donde tiene dos posiciones disponibles
    Laberinto2 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(3,2),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto2,caminoActual,posInvalidas) == [(2,2),(3,1)])

    #laberinto donde tiene tres posiciones disponibles
    Laberinto3 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(1,2),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto3,caminoActual,posInvalidas) == [(2,2),(0,2),(1,1)])

    #laberinto donde tiene cuatro posiciones disponibles
    Laberinto4 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(2,1),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto4,caminoActual,posInvalidas) == [(3,1),(2,2),(1,1),(2,0)])

    #laberinto donde el camino hace que no tenga ninguna posicion disponible
    caminoActual2 = [(1,0)]
    Laberinto5 = {"Tablero":Tablero,"Dimensiones":len(Tablero),"posActual":(0,0),"posInicial":(0,0),"posDestino":(3,1)}
    assert(calcular_siguientes_pos(Laberinto5,caminoActual2,posInvalidas) == [])

    #laberinto de dimension impar donde tanto las paredes como el camino actual hacen que no tenga ninguna posicion disponible
    caminoActual3 = [(0,0),(0,1),(1,1)]
    posInvalidas2 = set([(2,0),(2,2),(3,1)])
    Tablero2 = ["I0010",
                "10010",
                "00000",
                "0001X",
                "00100"]
    Laberinto6 = {"Tablero":Tablero2,"Dimensiones":len(Tablero2),"posActual":(2,1),"posInicial":(0,0),"posDestino":(3,4)}
    assert(calcular_siguientes_pos(Laberinto6,caminoActual3,posInvalidas2) == [])