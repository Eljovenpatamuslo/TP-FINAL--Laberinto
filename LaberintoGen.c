#include "LaberintoGen.h"

char** crear_declarar_Tablero(int dimensiones){
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

void imprimir_Tablero_en_archivo(struct Laberinto Laberinto){
    FILE* fileSalida = fopen(ARCHIVO_SALIDA,"w");
    assert(fileSalida != NULL);
    for(int i = 0; i < Laberinto.dimensiones; i++){
        for(int j = 0; j < Laberinto.dimensiones; j++){
            fprintf(fileSalida,"%c",Laberinto.Tablero[i][j]);
        }
        fprintf(fileSalida,"\n");
    }
    fclose(fileSalida);
}

void poner_paredes_aleatorias_Tablero(struct Laberinto* Laberinto,int cantCaracteres){
    for(int i=0;i<cantCaracteres;){
        int filaAleatoria = rand() % Laberinto->dimensiones;
        int columnaAleatoria = rand() % Laberinto->dimensiones;

        if(Laberinto->Tablero[filaAleatoria][columnaAleatoria] == LIBRE){
           Laberinto->Tablero[filaAleatoria][columnaAleatoria] = PARED;
           i++; 
        }   
    }
}

void pasar_archivo_a_Laberinto(struct Laberinto* Laberinto,char* pathEntrada){
    char buffer[256];
    int aleatorios;
    FILE* fileEntrada = fopen(pathEntrada,"r");
    assert(fileEntrada != NULL);

    while(fscanf(fileEntrada,"%[^\n]\n",buffer) != EOF){
        int Fila,Columna;
        
        if(strcmp(buffer,TXT_DIMENSION) == 0){
            fscanf(fileEntrada,"%d\n",&Laberinto->dimensiones);
            Laberinto->Tablero = crear_declarar_Tablero(Laberinto->dimensiones);

        }else if(strcmp(buffer,TXT_OBSTACULOS_ALEATORIOS) == 0){
            fscanf(fileEntrada,"%d\n",&aleatorios);

        }else if(strcmp(buffer,TXT_POSICION_INICIAL) == 0){
            fscanf(fileEntrada,"(%d,%d)\n",&Fila,&Columna);
            Laberinto->Tablero[Fila-1][Columna-1] = SALIDA;

        }else if(strcmp(buffer,TXT_OBJETIVO) == 0){
            fscanf(fileEntrada,"(%d,%d)\n",&Fila,&Columna);
            Laberinto->Tablero[Fila-1][Columna-1] = OBJETIVO;

        }else if(strcmp(buffer,TXT_OBSTACULOS_FIJOS) != 0){
            //"(fila,columna)"
            Fila = buffer[1]-'0';
            Columna = buffer[3]-'0';
            Laberinto->Tablero[Fila-1][Columna-1] = PARED;
        }
    }
    fclose(fileEntrada);
    poner_paredes_aleatorias_Tablero(Laberinto,aleatorios); //se llama una vez que se pusieron todos los demas elementos ya que 
                                                            //podria poner una pared en la posicion de inicio,etc
}

void liberar_Memoria_Tablero(struct Laberinto Laberinto){
    for(int i = 0; i < Laberinto.dimensiones; i++){
        free(Laberinto.Tablero[i]);
    }
    free(Laberinto.Tablero);
}

int main(int argc, char** argv){
    if(argc != 2){ //si no se pone el archivo de entrada, el programa no corre
        printf("Cantidad incorrecta de archivos\n");
        return 1;
    }
    srand(time(NULL));//solo usado para la funcion rand()

    struct Laberinto Laberinto;
    pasar_archivo_a_Laberinto(&Laberinto,argv[1]);
    imprimir_Tablero_en_archivo(Laberinto);
    liberar_Memoria_Tablero(Laberinto);
    return 0;
}