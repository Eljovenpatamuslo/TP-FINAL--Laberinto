# Lucas Lamberti - TP FINAL

## Compilación archivo en C

gcc -Wall -g LaberintoGen.c

.\a.exe <direccion de la entrada del laberinto> #Windows
./a.out <direccion de la entrada del laberinto> #Linux

## Compilar archivo de python: 

python3 ResolverLaberinto.py

## Testear valgrind:
valgrind -s --leak-check=full ./a.out EntradaLaberinto.txt

## Testear pytest:
python3 -m pytest -v ResolverLaberinto.py