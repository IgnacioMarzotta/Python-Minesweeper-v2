#                   Grupo 5
#   Ignacio Agustin Marzotta Díaz (23.601.779-6) / NRC 17337
#   Diego Angel Díaz Muñoz (20.552.571-8) / NRC 17337

import BM2Functions as b2

selection = b2.askForSelection()
emptyCellCounter = 0
finished = False

while(selection != '3'):

    #Generar tablero a partir de archivo
    if(selection == '1'):

        #Obtener la dificultad, tamaño y nombre del archivo.
        dimension, difficulty, fileName = b2.readFile()
        print("Tamaño: "+str(dimension)+"x"+str(dimension)+", Dificultad: "+str(difficulty))

        #Definir los numeros y letras
        sideLetters, topNumbers = b2.getNumsAndLetters(dimension)

        #Crear tablero
        board = b2.createBoard(dimension)

        #Obtener numero de minas
        amountOfMines = b2.getAmountOfMines(dimension, difficulty)

        #Generar lista con minas
        minesPosition = b2.createRandomMines(amountOfMines,sideLetters, topNumbers)

        #Generar archivo de salida con las minas y las dimensiones del tablero
        b2.generateOutputFile(minesPosition, dimension, fileName[:-4])

    if(selection == '2'):
        #Obtener minas y tamaño
        dimension, minesPosition = b2.loadFile()

        #Obtener letras y numeros de tablero
        sideLetters, topNumbers = b2.getNumsAndLetters(dimension)

        #Crear tablero
        board = b2.createBoard(dimension)

        #Colocar bombas en tablero
        board = b2.placeBombs(board, minesPosition, topNumbers, sideLetters)

        b2.play(board, sideLetters, topNumbers, emptyCellCounter, finished)

    selection = b2.askForSelection()
else:
    print("Saliendo.")