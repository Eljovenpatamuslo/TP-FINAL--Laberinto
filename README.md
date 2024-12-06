# Lucas Lamberti - TP FINAL

## Compilación archivo en C

gcc -Wall -g LaberintoGen.c -o LaberintoGenerado

LaberintoGenerado <direccion de la entrada del laberinto>

## Compilar archivo de python: 

python3 ResolvedorLaberinto.py

## Testear valgrind:
valgrind -s --leak-check=full LaberintoGenerado EntradaLaberinto.txt

## Testear pytest:
python3 -m pytest -v .\ResolvedorLaberinto.py