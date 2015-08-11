import pygame, random, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 850
BOARDWIDTH = 550
BOARDHEIGHT = 850
X_MARGIN = (WINDOWWIDTH - BOARDWIDTH)/2

POS_AMOUNT = 4

REDPEG = "r"
ORANGEPEG = "o"
YELLOWPEG = "y"
GREENPEG = "g"
BLUEPEG = "b"
PURPLEPEG = "p"
PEG_COLORS = [REDPEG, ORANGEPEG, YELLOWPEG, GREENPEG, BLUEPEG, PURPLEPEG]

RED = (222, 18, 18)
ORANGE = (245, 113, 20)
YELLOW = (240, 236, 24)
GREEN = (26, 140, 15)
BLUE = (32, 79, 232)
PURPLE = (100, 13, 158)
LIGHTBLUE = (179, 229, 232)
LIGHTBROWN = (171, 147, 130)
BROWN = (143, 73, 59)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (97, 97, 97)
DARKGRAY = (71, 71, 71)
TURQUOISE = (57, 184, 159)
LIGHTGREEN = (102, 255, 204)

BGCOLOR = LIGHTBLUE
BOARDCOLOR = LIGHTBROWN
TEXTCOLOR = BLACK
BUTTONCOLOR = BROWN
HIGHLIGHTCOLOR = LIGHTGREEN

PEGDICT = {"r":RED,
           "o":ORANGE,
           "y":YELLOW,
           "g":GREEN,
           "b":BLUE,
           "p":PURPLE,
           None:BLACK}

KEYDICT = {K_r:"r",
           K_o:"o",
           K_y:"y",
           K_g:"g",
           K_b:"b",
           K_p:"p"}

def main():
    global DISPLAYSURF, FPSCLOCK, FONTOBJ
    
    pygame.init()
    FONTOBJ = pygame.font.Font('freesansbold.ttf', 32)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption("MasterMind")
    pygame.display.set_icon(pygame.image.load("windowicon.png"))

    while True:
        if runGame() == False:
            pygame.quit()
            sys.exit()
        
def runGame():
    patterns = []
    for i in range(12):
        patterns.append([None] * POS_AMOUNT)

    pegs = []
    for i in range(12):
        pegs.append([[None, None], [None, None]])

    currentPattern = 0
    computerPattern = getComputerPattern()
    patternRevealed = False
    buttonAvailable = False
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        playerPatternGuess, currentButton, patterns = getPlayerPatternGuess(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable)
        blackPegs, whitePegs = getPegs(computerPattern, playerPatternGuess)
        pegs = addPegsToList(blackPegs, BLACK, pegs, currentPattern)
        pegs = addPegsToList(whitePegs, WHITE, pegs, currentPattern)
            
        currentPattern += 1
        if isGameWon(blackPegs):
            patternRevealed = True
            drawBoard(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable)
            return endGameScreen(True)
        elif currentPattern == 12:
            patternRevealed = True
            drawBoard(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable)
            return endGameScreen(False)

        drawBoard(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def addPegsToList(pegNum, pegColor, pegs, currentPattern):
    for i in range(pegNum):
        row = random.randint(0, 1)
        x = random.randint(0, 1)
        while pegs[currentPattern][row][x] != None:
            row = random.randint(0, 1)
            x = random.randint(0, 1)
        pegs[currentPattern][row][x] = pegColor

    return pegs

def getPlayerPatternGuess(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable):
    patternGuess = [None, None, None, None]
    currentButton = 0
    buttonColorIndex = [len(PEG_COLORS) - 1, len(PEG_COLORS) - 1, len(PEG_COLORS) - 1, len(PEG_COLORS) - 1]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    currentButton -= 1
                    if currentButton < 0:
                        currentButton = 4
                elif event.key == K_RIGHT:
                    currentButton += 1
                    if currentButton > 4:
                        currentButton = 0
                elif event.key == K_SPACE:
                    if currentButton == 4:
                        if buttonAvailable:
                            return patternGuess, currentButton, patterns
                    else:
                        buttonColorIndex[currentButton] += 1
                        if buttonColorIndex[currentButton] > len(PEG_COLORS) - 1:
                            buttonColorIndex[currentButton] = 0
                        buttonColor = PEG_COLORS[buttonColorIndex[currentButton]]
                        patterns[currentPattern][currentButton] = buttonColor
                        patternGuess[currentButton] = buttonColor
                elif event.key in (K_r, K_o, K_y, K_g, K_b, K_p):
                    buttonColor = KEYDICT[event.key]
                    patterns[currentPattern][currentButton] = buttonColor
                    patternGuess[currentButton] = buttonColor
        completedItems = 0
        for item in patternGuess:
            if item in PEG_COLORS:
                completedItems += 1
        if completedItems == POS_AMOUNT:
            buttonAvailable = True
            
        drawBoard(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable)
        drawHighlight(currentPattern, currentButton)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawHighlight(currentPattern, currentButton):
    pegRect = pygame.Rect(0, 0, BOARDWIDTH/6, BOARDHEIGHT/13)
    if currentButton == 4:
        pegRect.topleft = (X_MARGIN + BOARDWIDTH/6 * 4, BOARDHEIGHT/13 * currentPattern)
        buttonSurf = FONTOBJ.render("Enter", True, BLACK, BUTTONCOLOR)
        buttonRect = buttonSurf.get_rect()
        buttonRect.center = (pegRect.center)
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (buttonRect.left - 3, buttonRect.top - 3, buttonRect.width + 6, buttonRect.height + 6), 4)
    else:
        pegRect.topleft = (X_MARGIN + BOARDWIDTH/6 * currentButton, BOARDHEIGHT/13 * currentPattern)
        pygame.draw.circle(DISPLAYSURF, HIGHLIGHTCOLOR, pegRect.center, int(pegRect.height/2 - 11), 4)
        
def endGameScreen(won):
    WINNEROBJ = pygame.font.Font("freesansbold.ttf", 30)
    if won:
        msg = "You correctly guessed the pattern and won the game!"
    else:
        msg = "You didn't guess my code in time and lost the game!"
    msg2 = "Want to play again?"
    msgSurface = WINNEROBJ.render(msg, True, BLACK, TURQUOISE)
    msg2Surface = WINNEROBJ.render(msg2, True, BLACK, TURQUOISE)
    msgRect = msgSurface.get_rect()
    msg2Rect = msg2Surface.get_rect()
    msgRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2 - 60))
    msg2Rect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2 - 7.5))
    FONTOBJ2 = pygame.font.Font("freesansbold.ttf", 30)
    yesSurface = FONTOBJ2.render("Yes", True, BLACK, TURQUOISE)
    yesRect = yesSurface.get_rect()
    yesRect.center = (int(WINDOWWIDTH/2-yesRect.width), int(WINDOWHEIGHT/2 + 50))
    noSurface = FONTOBJ2.render("No", True, BLACK, TURQUOISE)
    noRect = noSurface.get_rect()
    noRect.center = (int(WINDOWWIDTH/2+noRect.width), int(WINDOWHEIGHT/2 + 50))
    while True:
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        if mouseClicked and yesRect.collidepoint(mousex, mousey):
            return True
        elif mouseClicked and noRect.collidepoint(mousex, mousey):
            return False
        DISPLAYSURF.blit(msgSurface, msgRect)
        DISPLAYSURF.blit(msg2Surface, msg2Rect)
        DISPLAYSURF.blit(yesSurface, yesRect)
        DISPLAYSURF.blit(noSurface, noRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard(patterns, pegs, currentPattern, computerPattern, patternRevealed, buttonAvailable):
    DISPLAYSURF.fill(BGCOLOR)
    pygame.draw.rect(DISPLAYSURF, BOARDCOLOR, (X_MARGIN, 0, BOARDWIDTH, BOARDHEIGHT))
    pegRect = pygame.Rect(X_MARGIN, 0, BOARDWIDTH/6, BOARDHEIGHT/13)

    for y in range(12):
        for x in range(4):
            peg = patterns[y][x]
            pegColor = PEGDICT[peg]
            pygame.draw.circle(DISPLAYSURF, BLACK, pegRect.center, int(pegRect.height/2 - 15))
            pygame.draw.circle(DISPLAYSURF, pegColor, pegRect.center, int(pegRect.height/2 - 17))
            pegRect.left += BOARDWIDTH/6
        pegRect.left = X_MARGIN
        pegRect.top += BOARDHEIGHT/13

    for x in range(4):
        peg = computerPattern[x]
        pegColor = PEGDICT[peg]
        pygame.draw.circle(DISPLAYSURF, BLACK, pegRect.center, int(pegRect.height/2 - 15))
        pygame.draw.circle(DISPLAYSURF, pegColor, pegRect.center, int(pegRect.height/2 - 15))
        pegRect.left += BOARDWIDTH/6

    if patternRevealed == False:
        pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, (X_MARGIN + 10, BOARDHEIGHT - pegRect.height - 5, pegRect.width * 4 - 10, pegRect.height - 5))

    if currentPattern < 12:
        if buttonAvailable == True:
            buttonSurf = FONTOBJ.render("Enter", True, BLACK, BUTTONCOLOR)
        else:
            buttonSurf = FONTOBJ.render("Enter", True, DARKGRAY, GRAY)
        buttonRect = buttonSurf.get_rect()
        pegRect.topleft = (X_MARGIN + BOARDWIDTH/6 * 4, BOARDHEIGHT/13 * currentPattern)
        buttonRect.center = pegRect.center
        DISPLAYSURF.blit(buttonSurf, buttonRect)

    pegRect = pygame.Rect(X_MARGIN + BOARDWIDTH/6 * 5, 0, BOARDWIDTH/6, BOARDHEIGHT/13)
    circleCenter = [int(X_MARGIN + BOARDWIDTH/6 * 5 + pegRect.width/4), int(pegRect.height/4)]

    for y in range(12):
        for row in range(2):
            for x in range(2):
                circleColor = pegs[y][row][x]
                if circleColor == None:
                    circleColor = BOARDCOLOR
                pygame.draw.circle(DISPLAYSURF, BLACK, (circleCenter[0], circleCenter[1]), int(pegRect.height/4 - 4))
                pygame.draw.circle(DISPLAYSURF, circleColor, (circleCenter[0], circleCenter[1]), int(pegRect.height/4 - 5))
                circleCenter[0] += int(pegRect.width/2)
            circleCenter[0] = int(X_MARGIN + BOARDWIDTH/6 * 5 + pegRect.width/4)
            circleCenter[1] += int(pegRect.height/2)
        circleCenter[1] += 1
        if y != 0:
            pygame.draw.line(DISPLAYSURF, BLACK, (X_MARGIN, int(pegRect.height/4 * y * 4)), (X_MARGIN + BOARDWIDTH, int(pegRect.height/4 * y * 4)), 2)

def getComputerPattern():
    pattern = []
    for i in range(POS_AMOUNT):
        pattern.append(random.choice(PEG_COLORS))

    return pattern
        
def isGameWon(blackPegs):
    return blackPegs == POS_AMOUNT

def getPegs(code, codeGuess):
    blackPegs = 0
    whitePegs = 0
    index = 0
    codeCopy = code[:]
    
    while index < POS_AMOUNT:
        if codeGuess[index] == code[index]:
            blackPegs += 1
            codeGuess[index] = "!"
            codeCopy[index] = "@"
        index += 1

    for item in codeGuess:
        if item in codeCopy:
            whitePegs += 1
            codeGuess[codeGuess.index(item)] = "!"
            codeCopy[code.index(item)] = "@"

    return blackPegs, whitePegs

if __name__ == "__main__":
    main()    
