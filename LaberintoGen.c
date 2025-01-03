#include "LaberintoGen.h"

char** crear_y_declarar_Tablero(int dimensiones){
    char** Tablero = malloc(sizeof(char *) * dimensiones);
    assert(Tablero != NULL);
    for(int i = 0; i < dimensiones; i++){
        Tablero[i] = malloc(sizeof(char) * dimensiones);
        assert(Tablero[i] != NULL);

        for(int j = 0; j < dimensiones; j++){
            Tablero[i][j] = LIBRE;
        }
    }

    return Tablero;
}

void imprimir_Tablero_en_archivo(struct Laberinto Laberinto, char* NombreArchivoSalida){
    FILE* archivoSalida = fopen(NombreArchivoSalida,"w");
    assert(archivoSalida != NULL);
    
    for(int i = 0; i < Laberinto.dimensiones; i++){
        for(int j = 0; j < Laberinto.dimensiones; j++){
            fprintf(archivoSalida,"%c",Laberinto.Tablero[i][j]);
        }
        fprintf(archivoSalida,"\n");
    }
    fclose(archivoSalida);
}

void poner_paredes_aleatorias_Tablero(struct Laberinto* Laberinto,int cantCaracteres){
    for(int i = 0; i < cantCaracteres; ){
        int filaAleatoria = rand() % Laberinto->dimensiones;
        int columnaAleatoria = rand() % Laberinto->dimensiones;

        if(Laberinto->Tablero[filaAleatoria][columnaAleatoria] == LIBRE){
           Laberinto->Tablero[filaAleatoria][columnaAleatoria] = PARED;
           i++; 
        }   
    }
}

int obtener_entero_del_archivo(FILE* Archivo){
    int entero;
    fscanf(Archivo,"%*[^\n]\n");
    fscanf(Archivo,"%d\n",&entero);
    return entero;
}

void obtener_posicion_del_archivo_y_poner_caracter(FILE* Archivo,struct Laberinto* Laberinto,char caracter){
    int Fila,Columna;
    fscanf(Archivo,"%*[^\n]\n");
    fscanf(Archivo,"(%d,%d)\n",&Fila,&Columna);
    assert(Fila >= 0 && Fila < Laberinto->dimensiones && Columna >= 0 && Columna < Laberinto->dimensiones);
    Laberinto->Tablero[Fila-1][Columna-1] = caracter;
}

void poner_obstaculos_fijos_del_archivo_en_Laberinto(FILE* Archivo,struct Laberinto* Laberinto,int* CantObstaculosFijos){
    int Fila,Columna;
    fscanf(Archivo,"%*[^\n]\n");
    while(fscanf(Archivo,"(%d,%d)\n",&Fila,&Columna) == 2){
        assert(Fila >= 0 && Fila < Laberinto->dimensiones && Columna >= 0 && Columna < Laberinto->dimensiones);
        Laberinto->Tablero[Fila-1][Columna-1] = PARED;
        (*CantObstaculosFijos)++;
    }
}

int comprobar_todos_los_campos_de_laberinto(struct Laberinto Laberinto,int CantParedesNecesarias){
    int CantParedesEncontradas = 0;
    int SalidaEncontrada = 0;
    int ObjetivoEncontrado = 0;

    for(int i = 0; i < Laberinto.dimensiones && !(CantParedesEncontradas == CantParedesNecesarias && SalidaEncontrada && ObjetivoEncontrado); i++){
        for(int j = 0; j < Laberinto.dimensiones && !(CantParedesEncontradas == CantParedesNecesarias && SalidaEncontrada && ObjetivoEncontrado); j++){
            if(Laberinto.Tablero[i][j] == PARED){
                CantParedesEncontradas++;

            }else if(Laberinto.Tablero[i][j] == SALIDA){
                SalidaEncontrada = 1;  

            }else if(Laberinto.Tablero[i][j] == OBJETIVO){
                ObjetivoEncontrado = 1; 
            }
        }
    }
    return CantParedesEncontradas == CantParedesNecesarias && SalidaEncontrada && ObjetivoEncontrado;
}

void pasar_archivo_a_Laberinto(struct Laberinto* Laberinto,char* direccionEntrada){
    FILE* Archivo = fopen(direccionEntrada,"r");
    assert(Archivo != NULL);

    Laberinto->dimensiones = obtener_entero_del_archivo(Archivo);
    assert(Laberinto->dimensiones >= MINIMA_DIMENSION_ACEPTABLE);

    Laberinto->Tablero = crear_y_declarar_Tablero(Laberinto->dimensiones);

    int CantObstaculosFijos = 0;
    poner_obstaculos_fijos_del_archivo_en_Laberinto(Archivo,Laberinto,&CantObstaculosFijos);

    int Aleatorios = obtener_entero_del_archivo(Archivo);
    assert(Aleatorios >= 0 && Aleatorios < (Laberinto->dimensiones * Laberinto->dimensiones) - 2);
    obtener_posicion_del_archivo_y_poner_caracter(Archivo,Laberinto,SALIDA);//Posicion Inicial

    obtener_posicion_del_archivo_y_poner_caracter(Archivo,Laberinto,OBJETIVO);//Objetivo

    fclose(Archivo);

    poner_paredes_aleatorias_Tablero(Laberinto,Aleatorios); //se llama una vez que se pusieron todos los demas elementos ya que 
                                                            //podria poner una pared en la posicion de inicio,etc
    assert(comprobar_todos_los_campos_de_laberinto(*Laberinto,CantObstaculosFijos + Aleatorios));
}

void liberar_Memoria_Tablero(struct Laberinto Laberinto){
    for(int i = 0; i < Laberinto.dimensiones; i++){
        free(Laberinto.Tablero[i]);
    }
    free(Laberinto.Tablero);
}

int main(int argc, char** argv){
    if(argc != 3){ //si no se pone el archivo de entrada ni el archivo de salida, el programa no corre
        printf("Cantidad incorrecta de archivos\n");
        printf("Como ejecutar el programa:\n");
        printf(".\\a.exe <Entrada> <Salida> (Windows)\n");
        printf("./a.out <Entrada> <Salida> (Linux)\n");
        return 1;
    }
    srand(time(NULL));//solo usado para la funcion rand()

    struct Laberinto Laberinto;
    pasar_archivo_a_Laberinto(&Laberinto,argv[1]);
    imprimir_Tablero_en_archivo(Laberinto,argv[2]);
    liberar_Memoria_Tablero(Laberinto);
    return 0;
}