# This file will contains some instructions about compiling
.PHONY: all

all: program


main.o: main.c
	gcc main.c -g -o main.o -c -lpthread

module.o: module.c
	gcc module.c  -g -o module.o -c -lpthread

program: main.o module.o
	gcc -g -o program main.o main.o
