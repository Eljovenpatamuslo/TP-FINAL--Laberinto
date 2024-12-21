#ifndef LABERINTOGEN
#define LABERINTOGEN
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h> //se usa para rand()

//representaciones de los objetos del laberinto
#define PARED '1'
#define SALIDA 'I'
#define OBJETIVO 'X'
#define LIBRE '0'

//campos de EntradaLaberinto que separan los datos
//por si se cambia el nombre en el archivo de entrada es mas rapido modificarlo aca
#define TXT_DIMENSION "dimension"
#define TXT_OBSTACULOS_ALEATORIOS "obstaculos aleatorios"
#define TXT_OBJETIVO "objetivo"
#define TXT_POSICION_INICIAL "posicion inicial"
#define TXT_OBSTACULOS_FIJOS "obstaculos fijos"

#define MINIMA_DIMENSION_ACEPTABLE 2

struct Laberinto{
    char** Tablero; //todos los caracteres que requiere el tablero
    int dimensiones; //tamaño del tablero cuadrado
};
//toma el archivo de entrada con el formato estatico y almacena cada dato en la estructura Laberinto
void pasar_archivo_a_Laberinto(struct Laberinto* Laberinto,char* pathEntrada);

//toma la direccion de memoria del laberinto y la cantidad de caracteres que se quiere poner
//pone paredes en lugares libres
void poner_paredes_aleatorias_Tablero(struct Laberinto* Laberinto,int cantCaracteres);

//imprime el tablero final en el archivo de salida que le paso el usuario
void imprimir_Tablero_en_archivo(struct Laberinto Laberinto, char* NombreArchivoSalida);

//pide la memoria necesaria y declara todos los elementos de Tablero como LIBRE
char** crear_y_declarar_Tablero(int dimensiones);

//libera la memoria de Tablero
void liberar_Memoria_Tablero(struct Laberinto Laberinto);

//toma el archivo de entrada, el puntero estructura Laberinto y pone paredes en las distintas posiciones debajo del texto "obstaculos fijos" y pone en CantObstaculosFijos la cantidad de obstaculos fijos
void poner_obstaculos_fijos_del_archivo_en_Laberinto(FILE* Archivo,struct Laberinto* Laberinto,int* CantObstaculosFijos);

//toma el archivo de entrada, el puntero estructura laberinto, un caracter e inserta el caracter en la posicion leida debajo del texto
void obtener_posicion_del_archivo_y_poner_caracter(FILE* Archivo,struct Laberinto* Laberinto,char caracter);

//toma el archivo de entrada y devuelve el valor entero debajo del texto
int obtener_entero_del_archivo(FILE* Archivo);

//toma el laberinto y la cantidad de paredes que se tendrian que haber colocado y devuelve 1 si todos los campos del laberinto estan presentes, de lo contrario 0
int comprobar_todos_los_campos_de_laberinto(struct Laberinto Laberinto,int CantParedesNecesaria);

#endif