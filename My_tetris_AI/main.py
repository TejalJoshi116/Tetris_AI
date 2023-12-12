import pygame
from tetromino import *
from display import *
from board import *
from pcPlayer import *
from direction import *
from rotation import *
print("\n\n++++ Welcome to Tejal's Tetris++++\n")


#Bools that control game state
isOpen = True
newGame = True
gameOver = False
paused = False
selfPlay = False
locked = False
got_a_tetris = False
#Create game window and clock
window = Window()
draw = Draw(window)
draw.createScreen()
clock = pygame.time.Clock()

while isOpen:
    #Draw new Frame
    pygame.display.update()
    #Clear screen
    draw.screen.fill("White")

    #reset board
    if newGame:
        board = Board()
        pcPlayer = PcPlayer(board)
        tetromino = board.generatePiece()
        timeCount = 0
        draw.drawStartScreen(board)

    #newGame screen loop
        while newGame:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    newGame = False
                    isOpen = False
                keyInput = pygame.key.get_pressed()
                if keyInput[pygame.K_p]:
                    newGame = False
                    selfPlay = False
                if keyInput[pygame.K_b]:
                    selfPlay = True
                    newGame = False

    #Pause / Start screen loop
    while paused:
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False 
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_ESCAPE]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False
 
    gameFlags = [newGame, gameOver, paused, (not isOpen)]
    
    got_a_tetris = False
    #gamePlay Loop
    while (not any(gameFlags)):
        
        #Draw game elements to screen
        draw.refreshScreen(board, tetromino)
    
        #pcPlayer code
        if (selfPlay):
            if (board.isHeldPieceEmpty()):
                board.setHeldPiece(tetromino)
            
            if got_a_tetris==False :              
                tetromino = board.generatePiece()

            # print("post start generate piece")
            # pygame.time.delay(2000)  
            draw.refreshScreen(board, tetromino)
            
            locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
            draw.refreshScreen(board, tetromino)
            # ++++++THIS ONE pygame.time.delay(100)
            if (locked):
                tetromino = board.newPieceOrGameOver(tetromino)
                # print("post start newpieceorgameover")
                # pygame.time.delay(2000)  
                if tetromino == None:
                    gameOver = True
                    break
            # print("0")
            # Tetromino.printPiece(tetromino)  
            # print("next is choose piece")
            # pygame.time.delay(500)
                          
            (swapPiece, position) = pcPlayer.choosePieceAndPosition(board, tetromino)
            if (swapPiece):
                tetromino = board.swapWithHeldPiece(tetromino)
            # print("next is refresh1")
            # pygame.time.delay(1000)    
            draw.refreshScreen(board, tetromino)
            # print("next is Make move")
            # pygame.time.delay(1000)
                        
            pcPlayer.makeMove(board, tetromino, position, draw)
            # print("next is newpiece or gameover")
            # ++++++THIS ONE pygame.time.delay(300)
            tetromino = board.newPieceOrGameOver(tetromino)
            got_a_tetris=True
            # print("post newpiece gamover\n")
            # for y in range(board.height):
            #     for x in range(board.width):
            #         print(board.grid[y][x], end=' ')
            #     print()  # Move to the next line for the next row
            # print()
            # print("1")
            # Tetromino.printPiece(tetromino)
            # print("next is refresh2")

            # pygame.time.delay(2000)
            draw.refreshScreen(board, tetromino)
            # print("post refresh2 screen\n")
            
            # pygame.time.delay(2000)
            # print("2")
            # Tetromino.printPiece(tetromino)
            
            if tetromino == None:
                gameOver = True
                break

        #Step game forward
        timeCount += clock.get_rawtime()
        clock.tick()
        if (timeCount >= board.getDropInterval()):
            timeCount = 0
            # print("next is time: move or lock")
            # pygame.time.delay(2000)
            locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
            temp=True
            if (locked):
                # print("next is time: new piece or gameoverr")
                # pygame.time.delay(2000)
                #++++++++++May mess up+++++++ temp
                # temp_tetromino = board.newPieceOrGameOver(tetromino)
                if (tetromino.xOffset == 0) and (tetromino.yOffset == 0):
                    temp=False
                if temp == False:
                    gameOver = True
                    break
            # print("next is time: refreshscreen")
            # pygame.time.delay(2000)    
            draw.refreshScreen(board, tetromino)
            # print(" time: post refreshscreen")
            # pygame.time.delay(2000)

        #Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_ESCAPE]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True
            #Game controls only if not bot
            if (not selfPlay):
                if keyInput[pygame.K_LCTRL] or keyInput[pygame.K_RCTRL]:
                    board.rotatePiece(tetromino, Rotation.ANTICLOCKWISE)
                if keyInput[pygame.K_UP]:
                    board.rotatePiece(tetromino, Rotation.CLOCKWISE)
                if keyInput[pygame.K_RIGHT]:
                    board.moveOrLockPiece(tetromino, Direction.RIGHT)
                if keyInput[pygame.K_LEFT]:
                    board.moveOrLockPiece(tetromino, Direction.LEFT)
                if keyInput[pygame.K_DOWN]:
                    locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
                    if (locked):
                        tetromino = board.newPieceOrGameOver(tetromino)
                        if tetromino == None:
                            gameOver = True
                if keyInput[pygame.K_RETURN]:
                    board.dropAndLockPiece(tetromino)
                    tetromino = board.newPieceOrGameOver(tetromino)
                    if tetromino == None:
                        gameOver = True
                if keyInput[pygame.K_LSHIFT] or keyInput[pygame.K_RSHIFT]:
                    if (board.isHeldPieceEmpty()):
                        board.setHeldPiece(tetromino)
                        tetromino = board.generatePiece()
                    else:
                        tetromino = board.swapWithHeldPiece(tetromino)

        gameFlags = [newGame, gameOver, paused, (not isOpen)]

    #Game over screen loop
    while gameOver:
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                gameOver = False
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_ESCAPE]:
                newGame = True
                gameOver = False
           