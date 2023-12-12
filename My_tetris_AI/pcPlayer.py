import copy
from tetromino import *
from board import *
from direction import *
# from tetromino import generate_all_tetrominos

class PcPlayer:

    def clearPositionScores(self, board):
        self.positionScores = {}
        self.emptyRow = []
        for x in range(board.width):
            self.emptyRow.append(0)
        for rotationCount in range(4):
            dictRow = {rotationCount : copy.copy(self.emptyRow)}
            self.positionScores.update(dictRow)

    def __init__(self, board, holeWeight = 3, heightWeight = 9, columnWeight = 5,rowfillweight = -10):
        self.holeWeight = holeWeight
        self.heightWeight = heightWeight
        self.columnWeight = columnWeight
        self.columnHeightLimit = 3
        self.clearPositionScores(board)
        self.rowfillweight = rowfillweight

    def moveFarLeft(self, board, tetromino):
        while not (board.isOutOfBounds(tetromino) or board.isGridBlocked(tetromino)):
            tetromino.incrementCoords(-1)
        tetromino.incrementCoords(1)
    
    def scoreBranches(self, copyBoard, Tet, depth, futureTetriminos):        
        if depth == 0:
            print("0.5: Here")
            return self.getPositionScore(copyBoard, Tet)
        
        minScore = float('inf')
        for nextTetromino in futureTetriminos:
            scores_for_position = []
            print("2: Here")
            rotationCount=nextTetromino.rotations  

            for xPos in range(copyBoard.width):
                copyTet = copy.deepcopy(Tet) 
                print("3: Here")
                copyBoard.rotatePiece(copyTet, Rotation.CLOCKWISE, rotationCount)
                self.moveFarLeft(copyBoard, copyTet)
                copyBoard.moveOrLockPiece(copyTet, Direction.RIGHT, xPos)
                copyBoard.dropPieceWithoutLock(copyTet)
                copyBoard.moveLeftAndLockPiece(copyTet, 2)
                print("4: Here")
                score = self.scoreBranches(copyBoard, nextTetromino, depth - 1, futureTetriminos)
                scores_for_position.append(score)

            # Find the minimum score for the current piece position and accumulate it
            minScore = min(minScore, min(scores_for_position))
            print("5: Here")

        return minScore
    
    def scoreAllPositions(self, board, tetromino):
        futureTetriminos = Tetromino.generate_all_tetrominos(self)

        board.holeCount = self.getHoleAndColumnCount(board.grid)[0]
        board.columnCount = self.getHoleAndColumnCount(board.grid)[1]
        board.linesClearedThisMove = self.getHoleAndColumnCount(board.grid)[2]
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
                depth=1
                # print("linecleared:",self.getLinesClearedScore(copyBoard))
                print("1: Here")
                B_score = self.scoreBranches(copyBoard, copyTet, depth, futureTetriminos)
                self.positionScores[rotationCount][xPos] = copy.copy(score + B_score)
                # self.positionScores[rotationCount][xPos] = copy.copy(score)
                copyBoard = copy.deepcopy(board)
                copyTet = copy.deepcopy(tetromino)

                
    
                # B_score = self.scoreBranches(copyBoard, copyTet, depth, futureTetriminos)

                # self.positionScores[rotationCount][xPos] = copy.copy(score + B_score)

    # def scoreBranches(self, board, tetromino, depth, futureTetriminos):
    #     if depth == 0:
    #         # return self.getPositionScore(board, tetromino)
    #         return

    #     board.holeCount = self.getHoleAndColumnCount(board.grid)[0]
    #     board.columnCount = self.getHoleAndColumnCount(board.grid)[1]
    #     board.linesClearedThisMove = self.getHoleAndColumnCount(board.grid)[2]
    #     copyTet = copy.deepcopy(tetromino)
    #     copyBoard = copy.deepcopy(board) 
    #     minScore = float('inf')
        
    #     for nextTetrimino in futureTetriminos:
    #         scores_for_position = []  
            
    #         for rotationCount in range(0, 4):
    #             for xPos in range(board.width):
    #                 copyBoard.rotatePiece(copyTet, Rotation.CLOCKWISE, rotationCount)
    #                 self.moveFarLeft(board, copyTet)
    #                 copyBoard.moveOrLockPiece(copyTet, Direction.RIGHT, xPos)
    #                 copyBoard.dropPieceWithoutLock(copyTet)
    #                 copyBoard.moveLeftAndLockPiece(copyTet, 2)

    #                 # Recursive call to get the minimum score for the next Tetrimino
    #                 score = self.scoreAllPositions(copyBoard, nextTetrimino, depth - 1, futureTetriminos[1:])
    #                 scores_for_position.append(score) 

    #                 # Update self.positionScores for the current position
    #                 self.positionScores[rotationCount][xPos] = copy.copy(score)

    #                 copyBoard = copy.deepcopy(board)
    #                 copyTet = copy.deepcopy(tetromino)

    #         # Find the minimum score for the current piece position and accumulate it
    #         minScore = min(minScore, min(scores_for_position))

    def choosePieceAndPosition(self, board, tetromino):
        # futureTetriminos = Tetromino.generate_all_tetrominos(self)
        print(tetromino.rotations)
            
        swapPiece = False
        # depth = 1
        # min = self.scoreAllPositions(board, tetromino, depth, futureTetriminos)
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
        position = (tetMin[1], tetMin[2])
        
        return (swapPiece, position)

        # position = (tetMin[1], tetMin[2])
        
        # return (False, position)

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
        # print("Chosen minscore:", minScore)                
        return (minScore, minScoreRotation, minScoreXPos)

    def getPositionScore(self, board, tetromino):
        (holeScore, columnScore, rowfillScore) = self.getHoleAndColumnScore(board, tetromino)
        heightScore = self.getHeightScore(board, tetromino)

        tempBoard = copy.deepcopy(board)
        tempBoard.lockPieceOnGrid(tetromino)
       
        positionScore = holeScore + heightScore + columnScore + rowfillScore
        # print("pos_score: ",positionScore," | HoleScore: ",holeScore," | height_score: ",heightScore," |rowfill_score: ",rowfillScore)
        return positionScore
    
    def getHeightScore(self, board, tetromino):
        positionHeight = board.height - tetromino.getMinYCoord()
        #Take the ratio of the min height point of the peice placed and the total height.
        #~~~~~~~~~~~~~~~~~Try taking max y~~~~~~~~~~~
        heightScore = (positionHeight / board.height) * self.heightWeight
        return heightScore
    
    
    def getHoleAndColumnScore(self, board, tetromino):
        grid = copy.deepcopy(board.grid)
        for coord in tetromino.blockCoords:
            y = int(coord[1])
            x = int(coord[0])
            grid[y][x] = 1
        # grid = self.makeGrid(board, tetromino)
        (newHoleCount, newColumnCount, newRowCount) = self.getHoleAndColumnCount(grid)
        holeScore = ((newHoleCount - board.holeCount)) * self.holeWeight
        columnScore = ((newColumnCount - board.columnCount)) * self.columnWeight
        #~~~~~~~~ITHEE
        rowfillScore = newRowCount*self.rowfillweight
        return (holeScore, columnScore,rowfillScore)

    def getHoleAndColumnCount(self, grid):
        gridHeight = len(grid.keys())
        gridWidth = len(grid[0])
        holeCount = 0
        columnCount = 0
        
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
        
       
        filledRows=0
        for y in range(gridHeight - 1, 0, -1):
            has_hole = any(grid[y][x] == 0 for x in range(gridWidth))
            if not has_hole:
                filledRows += 1

        # print("Filled_rows:", filledRows)
        
       
    
        return (holeCount, columnCount,filledRows)

    def makeMove(self, board, tetromino, position, draw):
        
        rotationCount = position[0]
        xPos = position[1]
        board.rotatePiece(tetromino, Rotation.CLOCKWISE, rotationCount)        
        pygame.time.delay(2000)
        draw.refreshScreen(board, tetromino)
        self.moveFarLeft(board, tetromino)
        board.moveOrLockPiece(tetromino, Direction.RIGHT, xPos)
        board.dropPieceWithoutLock(tetromino)
        board.moveLeftAndLockPiece(tetromino, 2)
        draw.refreshScreen(board, tetromino)
















        # def makeMove(self, board, tetromino, position, draw):
        #     print("Before rotation:")
        # Tetromino.printPiece(tetromino)  # Print the current state of the tetromino before rotation

        # rotationCount = position[0]
        # xPos = position[1]
        # board.rotatePiece(tetromino, Rotation.CLOCKWISE, rotationCount)        
        # print("After rotation:")
        # Tetromino.printPiece(tetromino)  # Print the state of the tetromino after rotation

        # pygame.time.delay(2000)
        # draw.refreshScreen(board, tetromino)

        # self.moveFarLeft(board, tetromino)
        # print("After moving left:")
        # Tetromino.printPiece(tetromino)  # Print the state of the tetromino after moving left

        # board.moveOrLockPiece(tetromino, Direction.RIGHT, xPos)
        # print("After moving right or locking:")
        # Tetromino.printPiece(tetromino)  # Print the state of the tetromino after moving right or locking

        # board.dropPieceWithoutLock(tetromino)
        # print("After dropping without locking:")
        # Tetromino.printPiece(tetromino)  # Print the state of the tetromino after dropping without locking

        # board.moveLeftAndLockPiece(tetromino, 2)
        # print("After moving left and locking:")
        # Tetromino.printPiece(tetromino)  # Print the state of the tetromino after moving left and locking

        # draw.refreshScreen(board, tetromino)
        # print("After screen refresh:")
        # Tetromino.printPiece(tetromino)
        
        