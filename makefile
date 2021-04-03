COMPILER = gcc
SOURCES = main.c src/min.c 
BINARY = test
PROJECT_NAME = TestExe

main.o: main.c
	${COMPILER} -c main.c
	cp main.o build/objs/main.o

min.o: src/min.c
	${COMPILER} -c src/min.c
	cp min.o build/objs/min.o

TestExe: main.o min.o 
	${COMPILER} -o build/${BINARY} main.o min.o 
	rm *.c

all: TestExe
