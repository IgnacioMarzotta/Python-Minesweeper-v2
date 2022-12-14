#                   Grupo 5
#   Ignacio Agustin Marzotta Díaz (23.601.779-6) / NRC 17337
#   Diego Angel Díaz Muñoz (20.552.571-8) / NRC 17337

import math
import string as st
import random as rd

def askForSelection():
    selection = str(input("Escoge una opción: (1) Generar tablero (2) Cargar tablero (3) Salir: "))
    valid = ['1','2','3']
    while(selection not in valid):
        selection = str(input("Error, escoge una opción valida: "))
    return selection

#File manipulation related
def readFile():
    fileName = input("Ingresa el nombre del archivo: ").lower().strip()
    try:
        fileInput = open(fileName, "r")
    except FileNotFoundError:
        fileName = input("Error, Intenta ingresar el nombre del archivo correctamente: ").lower().strip()
        fileInput = open(fileName, "r")
    lisFileInput = []
    for row in fileInput:
        lisFileInput.append(row.strip())
    fileInput.close()
    return int(lisFileInput[0]), lisFileInput[1], fileName

def loadFile():
    fileName = input("Ingresa el nombre del archivo: ").lower().strip()
    try:
        fileInput = open(fileName, "r")
    except FileNotFoundError:
        fileName = input("Error, Intenta ingresar el nombre del archivo correctamente: ").lower().strip()
        fileInput = open(fileName, "r")
    mines = []
    for row in fileInput:
        mines.append(row.upper().strip())
    size = mines.pop(0)
    fileInput.close()
    return int(size), mines

def generateOutputFile(mines, dimension, fileName):
    fileName = open(fileName+".sal", 'w')
    fileName.write(str(dimension)+'\n')
    for i in mines:
        fileName.write(i+'\n')
    fileName.close()

#Mines related
def placeBombs(board, mines, numbers, letters):
    #Funcion encargada de colocar bombas en el tablero
    for i in mines:
        if(len(i) <= 2):
            board[letters.index(i[0])][numbers.index(int(i[1]))] = "B"
        else:
            board[letters.index(i[0])][numbers.index(int(i[-2:]))] = "B"
    return board

def getAmountOfMines(dimension, difficulty):
    #Calcular cantidad de bombas dependiendo de la dificultad
    amountOfMines = 0
    if(difficulty == "F"):
        amountOfMines = (dimension**2)*0.1
    elif(difficulty == "M"):
        amountOfMines = (dimension**2)*0.15
    elif(difficulty == "D"):
        amountOfMines = (dimension**2)*0.2
    elif(difficulty == "X"):
        amountOfMines = (dimension**2)*0.3
    return math.trunc(amountOfMines)

def chooseRandomChars(letters, numbers):
    #Elige numero y letra aleatoria para las coordenadas de las bombas
    letterPos = rd.choice(letters)
    numberPos = rd.choice(numbers)
    return str(numberPos), str(letterPos)

def createRandomMines(amountOfMines, letters, numbers):
    #Crear minas aleatorias dependiendo de la cantidad calculada en base a la dificultad
    mines = []
    for i in range(amountOfMines):
        numberPos, letterPos = chooseRandomChars(letters, numbers)
        coord = letterPos+numberPos
        while(coord in mines):
            numberPos, letterPos = chooseRandomChars(letters, numbers)
            coord = letterPos+numberPos
        else:
            mines.append(coord)
    return mines

def calculateBombs(board, guessPosition, letters, numbers, emptyCellCounter):
    #Calcula si el usuario golpea una bomba y cuantas tiene alrededor
    finished = False
    bombsNearCounter = 0
    numericPart = int(list(filter(str.isdigit, guessPosition))[0])

    if(board[letters.index(guessPosition[0])][numbers.index(numericPart)] != "B"):
        #Si no está en la fila A
        if(board[letters.index(guessPosition[0])] != board[0]):
            #Si no es la columna 1
            if(numericPart != 1):
                try:
                    #Esq. Arriba Izquierda
                    if(board[letters.index(guessPosition[0])-1][numbers.index(numericPart)-1] == "B"):
                        bombsNearCounter += 1
                except IndexError:
                    pass

            try:
                #Arriba
                if(board[letters.index(guessPosition[0])-1][numbers.index(numericPart)] == "B"):
                    bombsNearCounter += 1
            except IndexError:
                pass

            try:
                #Esq. Arriba Derecha
                if(board[letters.index(guessPosition[0])-1][numbers.index(numericPart)+1] == "B"):
                    bombsNearCounter += 1
            except IndexError:
                pass

        if(numericPart != 1):
            try:
                #Esq. Abajo Izquierda
                if(board[letters.index(guessPosition[0])+1][numbers.index(numericPart)-1] == "B"):
                    bombsNearCounter += 1
            except IndexError:
                pass

            try:
                #Izquierda
                if(board[letters.index(guessPosition[0])][numbers.index(numericPart)-1] == "B"):
                    bombsNearCounter += 1
            except IndexError:
                pass

        try:
            #Abajo
            if(board[letters.index(guessPosition[0])+1][numbers.index(numericPart)] == "B"):
                bombsNearCounter += 1
        except IndexError:
            pass

        try:
            #Derecha
            if(board[letters.index(guessPosition[0])][numbers.index(numericPart)+1] == "B"):
                bombsNearCounter += 1
        except IndexError:
            pass

        try:
            #Esq. Abajo Derecha
            if(board[letters.index(guessPosition[0])+1][numbers.index(numericPart)+1] == "B"):
                bombsNearCounter += 1
        except IndexError:
            pass

    else:
        bombsNearCounter = "*"
        finished = True

    return bombsNearCounter, finished

def replaceOnBoard(board, guessPosition, bombCounter, letters, numbers):
    #En base a la cantidad de bombas que tiene cerca, las reemplaza en el tablero
    numericPart = int(list(filter(str.isdigit, guessPosition))[0])
    board[letters.index(guessPosition[0])][numbers.index(numericPart)] = bombCounter
    return board

#Board related
def createBoard(dimension):
    #Crear el tablero en base a las dimensiones, con todas las casillas vacias.
    board = []
    for i in range(dimension):
        board.append([])
        for y in range(dimension):
            board[i].append('N')
    return board

def displayBoard(board, sideLetters,topNumbers,emptyCellCounter):
    #Muestra el tablero con las bombas ocultas y calcula cuantas casillas sin descubrir le quedan al usuario

    emptyCellCounter = 0
    
    y = 0
    print("    ", end="")
    for i in topNumbers:
        if(i < 10):
            print(topNumbers[y], end="   ")
        else:
            print(topNumbers[y], end="  ")
        y += 1
    print( )

    x = 0
    for i in board:
        print(sideLetters[x].upper(), end="  ")
        for j in i:
            if(j == 'N'):
                print(" . ", end=" ")
                emptyCellCounter += 1
            elif(j == "B"):
                print(" . ", end=" ")
            else:
                print(' '+str(j)+' ', end=" ")
        x += 1
        print( )
    print()
    return emptyCellCounter

def getNumsAndLetters(size):
    #En base a las dimensiones del tablero, conseguir las letras y numeros que se usaran.
    letters = st.ascii_uppercase
    sideLetters = []
    topNumbers = []
    for i in range(size):
        sideLetters.append(letters[i])
        topNumbers.append(i+1)
    return sideLetters, topNumbers

def getUserGuess(letters, numbers):
    #Procesar la coordenada que ingresa el usuario para saber si es valida
    validGuess = False
    guessPosition = str(input("Ingresa la casilla del tablero que quieres abrir: ")).upper()
    while(len(guessPosition) < 2):
        print("Error, ingresa una posicion valida")
        guessPosition = str(input("Ingresa la casilla del tablero que quieres abrir: ")).upper()
    else:
        while(validGuess == False):
            if((guessPosition[0] in letters) and (int(list(filter(str.isdigit, guessPosition))[0]) in numbers)):
                validGuess = True
                break
            else:
                print("Error, ingresa una posicion valida")
                guessPosition = str(input("Ingresa la casilla del tablero que quieres abrir: ")).upper()
    return guessPosition

#Game related
def play(board, letters, numbers, emptyCellCounter, finished):
    #Funcion de jugar principal, se repite si "finished" es falso, finished cambia a True si el jugadror golpea una bomba o descubre todas las casillas
    emptyCellCounter = displayBoard(board, letters, numbers, emptyCellCounter)
    finished = False
    while(finished == False):
        guessPosition = getUserGuess(letters, numbers)
        bombsNear, finished = calculateBombs(board, guessPosition, letters, numbers, emptyCellCounter)
        board = replaceOnBoard(board, guessPosition, bombsNear, letters, numbers)
        if(emptyCellCounter >= 1 and finished == False):
            emptyCellCounter = displayBoard(board, letters, numbers, emptyCellCounter)
        if(emptyCellCounter == 0):
            finished = True
    else:
        playerFinished(board, numbers, letters, emptyCellCounter)

def playerFinished(board, numbers, letters, emptyCellCounter):
    #Mostrar el ultimo tablero con las bombas descubiertas y cambiar finished a True
    y = 0
    print("    ", end="")
    for i in numbers:
        if(i < 9):
            print(numbers[y], end="   ")
        else:
            print(numbers[y], end="  ")
        y += 1
    print()

    x = 0
    for i in board:
        print(letters[x].upper(), end="  ")
        for j in i:
            if(j == 'N'):
                print(" . ", end=" ")
            elif(j == "B"):
                print(" * ", end=" ")
            else:
                print(' '+str(j)+' ', end=" ")
        x += 1
        print( )

    if(emptyCellCounter == 0):
        print("GANASTE")
    else:
        print("PERDISTE")
