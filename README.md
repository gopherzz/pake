# Pake
**Pake is Simple Makefile Generator written in Python**
## Using Pike
**pakeConfig.toml**

    [executable] 
    name = 'TestExe'
	exec_name = 'test'
	language = 'c'
	sources = 'main.c src/min.c'
#### Run:
Install Deps:

    pip install requirements.txt
Run (When  pake.py in root of project directory ):

    python3 pake.py

That generates that makefile:

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

## Options
|Global Option|Think|
|--|--|
| [executable] | For Generate Executable Project |
| [library] | For Generate shared/static Library|
#### For [executable]:
|Option| Think|
|--|--|
| name      | Package Name example (without spaces): |
|           | name = 'TestProject' |
| exec_name | Name of Executable File example:|
|           | exec_name = 'a.out' |
| language  | Programming Language example: |
|           | language = 'c' |
| sources   | Sources files example: 
|           |sources = 'main.cpp test.cpp'|

#### For [library]:
|Option| Think|
|--|--|
| type      | Type of library example: |
|           | type = 'shared' # or 'static' as default|
| lib_name | Name of Library example:|
|           | lib_name = 'TestLib' |
| language  | Programming Language example: |
|           | language = 'c' |
| sources   | Sources files example: 
|           |sources = 'main.cpp test.cpp'|
