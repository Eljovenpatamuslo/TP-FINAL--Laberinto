# Lamberti Lucas - TP FINAL

## Compilar y Ejecutar archivo de C
gcc -Wall -g LaberintoGen.c

.\a.exe <entrada> <salida> #Windows
./a.out <entrada> <salida> #Linux

## Ejecutar Programa de Python: 
python3 .\ResolverLaberinto.py #Windows
python3 ResolverLaberinto.py #Linux

## Test valgrind:
valgrind -s --leak-check=full ./a.out EntradaLaberinto.txt SalidaLaberinto.txt #solo Linux

## Test pytest:
python3 -m pytest -v .\ResolverLaberinto.py #Windows
python3 -m pytest -v ResolverLaberinto.py #Linux
