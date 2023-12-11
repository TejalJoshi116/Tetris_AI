import copy
from tetromino import *
from board import *
from direction import *

class PcPlayer:

    def clearPositionScores(self, board):
        self.positionScores = {}
        self.emptyRow = []
        for x in range(board.width):
            self.emptyRow.append(0)
        for rotationCount in range(4):
            dictRow = {rotationCount : copy.copy(self.emptyRow)}
            self.positionScores.update(dictRow)

    def __init__(self, board, holeWeight = 3, heightWeight = 9, columnWeight = 5):
        self.holeWeight = holeWeight
        self.heightWeight = heightWeight
        self.columnWeight = columnWeight
        self.columnHeightLimit = 3
        self.clearPositionScores(board)

    def moveFarLeft(self, board, tetromino):
        while not (board.isOutOfBounds(tetromino) or board.isGridBlocked(tetromino)):
            tetromino.incrementCoords(-1)
        tetromino.incrementCoords(1)
    
    def scoreAllPositions(self, board, tetromino):
        board.holeCount = self.getHoleAndColumnCount(board.grid)[0]
        board.columnCount = self.getHoleAndColumnCount(board.grid)[1]
        copyTet = copy.deepcopy(tetromino)
        copyBoard = copy.deepcopy(board)
        for rotationCount in range(0, 4):
            for xPos in range(board.width):
                copyBoard.rotatePiece(copyTet, Rotation.CLOCKWISE, rotationCount)
                self.moveFarLeft(board, copyTet)
                copyBoard.moveOrLockPiece(copyTet, Direction.RIGHT, xPos)
                copyBoard.dropPieceWithoutLock(copyTet)
                copyBoard.moveLeftAndLockPiece(copyTet, 2)
                score = self.getPositionScore(board, copyTet)
                # print("linecleared:",self.getLinesClearedScore(copyBoard))
                self.positionScores[rotationCount][xPos] = copy.copy(score)
                copyBoard = copy.deepcopy(board)
                copyTet = copy.deepcopy(tetromino)
        
    def choosePieceAndPosition(self, board, tetromino):
        swapPiece = False
        
        self.scoreAllPositions(board, tetromino)
        tetMin = self.getMinScoreAndPosition()
        self.clearPositionScores(board)
        
        # heldPiece = copy.deepcopy(board.heldPiece)
        # board.centrePiece(heldPiece)
        # heldPiece.incrementCoords(tetromino.xOffset, tetromino.yOffset)
        # self.scoreAllPositions(board, heldPiece)
        # heldPieceMin = self.getMinScoreAndPosition()
        # self.clearPositionScores(board)
        # #Compare
        # if (heldPieceMin[0] < tetMin[0]):
        #     position = (heldPieceMin[1], heldPieceMin[2])
        #     swapPiece = True
        # else:
        #     position = (tetMin[1], tetMin[2])
        # return (swapPiece, position)

        position = (tetMin[1], tetMin[2])
        print("++++++++++++++++++++++++++++++++ CHOSEN ++++++++++++++++++++++++++++++++++++++++++++")
        return (False, position)

    def getMinScoreAndPosition(self): 
        minScore = self.positionScores[0][0]
        width = len(self.positionScores[0])
        minScoreRotation = 0
        minScoreXPos = 0
        for rotation in self.positionScores.keys():
            for xPos in range(width):
                if (self.positionScores[rotation][xPos] < minScore):
                        minScore = self.positionScores[rotation][xPos]
                        minScoreRotation = rotation
                        minScoreXPos = xPos
        return (minScore, minScoreRotation, minScoreXPos)

    def getPositionScore(self, board, tetromino):
        (holeScore, columnScore) = self.getHoleAndColumnScore(board, tetromino)
        heightScore = self.getHeightScore(board, tetromino)

        tempBoard = copy.deepcopy(board)
        tempBoard.lockPieceOnGrid(tetromino)
        #+++++Hereeeeee++++++++
        clearedRowCount = tempBoard.clearFullRows()
        linesClearedScore = clearedRowCount
        #print("filled rows=",linesClearedScore)

        #positionScore = holeScore + heightScore + columnScore + linesClearedScore
        positionScore = holeScore + heightScore + columnScore
        print("pos_score: ",positionScore," | HoleScore: ",holeScore," | height_score: ",heightScore,"\n")
        return positionScore
    #+++++Hereeeeee++++++++
    def getLinesClearedScore(self, board):
        linesClearedCount = 0
        grid = copy.deepcopy(board.grid)
        for y in range(board.height-1, 0, -1):
            if all(grid[y][x] == 1 for x in range(board.width)):
                linesClearedCount += 1
            
        #board.linesClearedThisMove = linesClearedCount

        #Ithe adjust kar
        linesClearedScore = linesClearedCount * 10
        return linesClearedScore

    def getHeightScore(self, board, tetromino):
        positionHeight = board.height - tetromino.getMinYCoord()
        #Take the ratio of the min height point of the peice placed and the total height.
        #~~~~~~~~~~~~~~~~~Try taking max y~~~~~~~~~~~
        heightScore = (positionHeight / board.height) * self.heightWeight
        return heightScore
    
    # def makeGrid(self, board, tetromino):
    #     grid = copy.deepcopy(board.grid)
    #     for coord in tetromino.blockCoords:
    #         y = int(coord[1])
    #         x = int(coord[0])
    #         grid[y][x] = 1
    #     return grid    
        
    
    def getHoleAndColumnScore(self, board, tetromino):
        grid = copy.deepcopy(board.grid)
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            grid[y][x] = 1
        # grid = self.makeGrid(board, tetromino)
        (newHoleCount, newColumnCount) = self.getHoleAndColumnCount(grid)
        holeScore = ((newHoleCount - board.holeCount)) * self.holeWeight
        columnScore = ((newColumnCount - board.columnCount)) * self.columnWeight
        return (holeScore, columnScore)

    def getHoleAndColumnCount(self, grid):
        gridHeight = len(grid.keys())
        gridWidth = len(grid[0])
        holeCount = 0
        columnCount = 0
        filledRowCount = 0
        columnList = [None] * gridWidth
        for x in range(gridWidth):
            emptyCount = 0

            for y in range(gridHeight-1, 0, -1):
                if (grid[y][x] == 0):
                    emptyCount += 1
                else:
                    holeCount += emptyCount
                    emptyCount = 0
            columnList[x] = emptyCount
        if columnList[0] >= (columnList[1] + self.columnHeightLimit):
            columnCount += 1
        if columnList[gridWidth-1] >= (columnList[gridWidth-2]+self.columnHeightLimit):
            columnCount += 1
        for i in range(1, gridWidth-2, 1):
            if ((columnList[i] >= (columnList[i-1] + self.columnHeightLimit)) and (columnList[i] >= (columnList[i+1] + self.columnHeightLimit))):
                columnCount += 1     
        #print(grid)
        
        holedrow=0
        filledrow=0
        
        for y in range(gridHeight-1, 0, -1):
            x=0
            is_fill=0
            while x <(gridWidth):               
                if (grid[y][x] == 0):    
                    holedrow+=1                                                       
                    break
                else:
                    is_fill+=1
            if(is_fill==10):
                filledrow+=1
                   
            
        print("Filled_rows:",filledrow) 
        
        #+++++Hereeeeee++++++++
        # for row_key, row_values in grid.items():
        #     if all(val != 0 for val in row_values):
        #         filled_rows += 1

        # print("FIlled_rows:",filled_rows)

        return (holeCount, columnCount)

    def makeMove(self, board, tetromino, position, draw):
        rotationCount = position[0]
        xPos = position[1]
        board.rotatePiece(tetromino, Rotation.CLOCKWISE, rotationCount)
        draw.refreshScreen(board, tetromino)
        self.moveFarLeft(board, tetromino)
        board.moveOrLockPiece(tetromino, Direction.RIGHT, xPos)
        board.dropPieceWithoutLock(tetromino)
        board.moveLeftAndLockPiece(tetromino, 2)
        draw.refreshScreen(board, tetromino)