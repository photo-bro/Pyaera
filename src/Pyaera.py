 #####################################################################
# Pyaera.py
# 
# CSCI 220
# Created: 11/25/12  
# Due:     12/12/12 
# Authors: Josh Harmon
#          Kali McKee
#          Christof Kenworthy
#        
# A simple Tic-Tac-Toe based game
#####################################################################

import pygame, sys, os  #Library imports
import Shape, Board #Local imports
from pygame.locals import * #~Namespace

#####################################################################  
# Game Logic variables and constants	
#####################################################################  
  
# Create shapes
redShape = []
blueShape = []
for x in range(6):
    redShape.append(Shape.Shape(x,  'Red',  None, False, (0,0)))
    blueShape.append(Shape.Shape(x, 'Blue', None, False, (0,0)))
    
# Create boards
redBoard = Board.Board()
blueBoard = Board.Board()
masterBoard = Board.Board()
   
# Global Booleans
## "They're a 'boolean' miles away" -Kali
WINDOWED = True
debug_mode = False
shape_box_visible = True
shape_placed = False        # Controls shape drag and drop 
game_won = False

# Event Vars
curShape = redShape[0]

#####################################################################
# Game Logic Functions
#####################################################################
# Coordinate form: ('a', '0'), where the first parameter of the tuple can 
#    be from a through d, or bu or p. The second parameter can be from 0 
#    through 3. A value of '-1' anywhere indicates an offboard or illegal
#    position
# Board form: The representation of coordinate form as a 16 bit unsigned
#    binary number. Example ('a', '0') = 0b1000000000000000. The first
#    parameter argument can only be from a - d.

def isSpotOpen(intBoard):
    #Description: Check's if a spot is open based upon a given board
    #Pre: intBoard only has one bit flipped (i.e. 0001000 not 01100100)
    #Arguments: intBoard is an integer
    #Returns: True if spot is open, false if not
    if intBoard & masterBoard.getBoard() == intBoard:
        return False
    return True

def posToSpot((x,y)):
    #Description:  Puts the piece on the board
    #Pre:  
    #Arguments: (x,y) in coordinate form
    #Returns:  the position of the spot in board form
    if x == 'a':
        if y == '0':
            return 0b1000000000000000
        elif y == '1':
            return 0b100000000000000
        elif y == '2':
            return 0b10000000000000
        elif y == '3':
            return 0b1000000000000     
    elif x == 'b':
        if y == '0':
            return 0b100000000000
        elif y == '1':
            return 0b10000000000
        elif y == '2':
            return 0b1000000000
        elif y == '3':
            return 0b100000000   
    elif x == 'c':
        if y == '0':
            return 0b10000000
        elif y == '1':
            return 0b1000000
        elif y == '2':
            return 0b100000
        elif y == '3':
            return 0b10000
    elif x == 'd':
        if y == '0':
            return 0b1000
        elif y == '1':
            return 0b100
        elif y == '2':
            return 0b10
        elif y == '3':
            return 0b1    
    else:
        return 0   
    return 0 #fail safe return

def updateMasterBoard (redBoard, blueBoard):
    #Description: Updates the masterBoard 
    #Pre:
    #Arguments: redBoard, blueBoard are Board objects
    #Returns: Void
    newBoardVal = redBoard.getBoard() | blueBoard.getBoard()
    masterBoard.setBoard(newBoardVal)
    
def isSolved():
    #Description: Checks to see if the masterBoard is solved
    #Pre:  
    #Arguments: 
    #Returns: True if solved, otherwise false
    
    solution = [ 0b1111000000000000, 0b0000111100000000, 0b0000000011110000, 0b0000000000001111, 0b1000100010001000, 0b0100010001000100, 0b0010001000100010, 0b0001000100010001, 0b1000010000100001, 0b0001001001001000]
    for x in range (10):
        if redBoard.getBoard() & solution[x] == solution[x]:
            return True
        if blueBoard.getBoard() & solution[x] == solution[x]:
            return True 
    return False

def PlaceShape(shape, (x,y)):
    #Description: Places the shape on board
    #Pre: 
    #Arguments: shape is a Shape object in coordinate form, (x,y) in coordinate form
    #Returns: True if the shape has been placed, otherwise false if the spot is not open
    if isSpotOpen(posToSpot((x,y))):
        #Save previous spot
        Pos_x, Pos_y = shape.getPosition()
        shape.setPrevPos(getPos((Pos_x + 10, Pos_y + 10)))
        # Set new position and parameters for the shape
        shape.setSpot((x,y))
        shape.setPosition(dropPos((x,y)))
        shape.setVisible(True)
        return True
    else:
        return False        

def AcceptTurn(shape):
    #Description: Updates the boards and returns to the next shape
    #Pre: 
    #Arguments: shape is a Shape object
    #Returns: If board is not solved returns the next shape, if solved
    # returns the fist shape
    
    # Variables
    newCurShape = shape #To be returned
    Pos_x, Pos_y = shape.getPosition()
    
    #Remove shape from board if all are placed
    redTemp = blueTemp = 0
    shape.setActive(False)
    for x in range (6):
        if redShape[x].isVisible():
            redTemp += 1
        if blueShape[x].isVisible():
            blueTemp += 1
    
    # Update boards
    if shape.getPlayer() == 'Red':
        # Remove past position from board
        if redTemp > 5:
            boardVal = redBoard.getBoard() ^ posToSpot(shape.getPrevPos())
            redBoard.setBoard(boardVal)
        boardVal = redBoard.getBoard() | posToSpot(getPos((Pos_x + 10, Pos_y + 10))) #update board
        redBoard.setBoard(boardVal)      
    else:
        # Remove past position from board
        if blueTemp > 5:
            boardVal = blueBoard.getBoard() ^ posToSpot(shape.getPrevPos())
            blueBoard.setBoard(boardVal)
        boardVal = blueBoard.getBoard() | posToSpot(getPos((Pos_x + 10, Pos_y + 10))) #update board
        blueBoard.setBoard(boardVal)
    # Update board
    updateMasterBoard(redBoard, blueBoard)
   
    #Check if board is solved  
    if isSolved():
        return redShape[0]
 
    #Deactivate shape
    shape.setActive(False)
    
    # Point to next shape / change player
    if shape.getNum() < 5: 
        if shape.getPlayer() == 'Red':
            newCurShape = blueShape[shape.getNum()]
        elif shape.getPlayer() == 'Blue':
            newCurShape = redShape[shape.getNum() + 1]
    else:
        if shape.getPlayer() == 'Red':
            newCurShape = blueShape[shape.getNum()]
        if shape.getPlayer() == 'Blue':
            newCurShape = redShape[0]
            
    # Set shape active
    newCurShape.setActive(True)
    return newCurShape

def Reset():
    #Description: resets the board has no return
    #Pre: 
    #Arguments: 
    #Returns: 
    
    #Reset shape information
    for i in range(6):
        redShape[i].setVisible(False)
        redShape[i].setPosition((0,0))
        redShape[i].setSpot(('0','0'))
        redShape[i].setActive(False)
        blueShape[i].setVisible(False)
        blueShape[i].setPosition((0,0))
        blueShape[i].setSpot(('0','0'))
        blueShape[i].setActive(False)

    # Reset boards
    redBoard.setBoard(0b0)
    blueBoard.setBoard(0b0)
    masterBoard.setBoard(0b0)
    
    # Set first piece as active
    redShape[0].setActive(True)


#####################################################################
# "Graphic" Functions
#####################################################################
        
def toBin(n, count):
    #Credit: vegaseat
    #URL: http://www.daniweb.com/software-development/python/code/216539/decimal-to-binary-conversion-python
    #Description: Convert integer to string containing the binary representation of the integer
    #Pre:
    #Arguments:  n, count are integers
    #Returns: Convert integer to string containing the binary representation of the integer
    
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)]) 

def getPos((x,y)):
    #Description: Converts pixel position in window to coordinate form
    #Pre:
    #Arguments: (x,y) is in coordinate form
    #Returns: Coordinate form
    
    offset = 169
    base_x = 100
    base_y = 60
    out_x = ''
    out_y = '-1'
    
    if x >= base_x and x < base_x + offset:
        out_x = 'a'
        if y >= base_y and y < base_y + offset:
            out_y = '0'
        elif y >= base_y + offset and y < base_y + 2*offset:
            out_y = '1'
        elif y >= base_y + 2*offset and y < base_y + 3*offset:
            out_y = '2'
        elif y >= base_y + 3*offset and y < base_y + 4*offset:
            out_y = '3'
    elif x >= base_x + offset and x < base_x + 2*offset:
        out_x = 'b'
        if y >= base_y and y < base_y + offset:
            out_y = '0'
        elif y >= base_y + offset and y < base_y + 2*offset:
            out_y = '1'
        elif y >= base_y + 2*offset and y < base_y + 3*offset:
            out_y = '2'
        elif y >= base_y + 3*offset and y <= base_y + 4*offset:
            out_y = '3'
    elif x >= base_x + 2*offset and x < base_x + 3*offset:
        out_x = 'c'
        if y >= base_y and y < base_y + offset:
            out_y = '0'
        elif y >= base_y + offset and y < base_y + 2*offset:
            out_y = '1'
        elif y >= base_y + 2*offset and y < base_y + 3*offset:
            out_y = '2'
        elif y >= base_y + 3*offset and y <= base_y + 4*offset:
            out_y = '3'
    elif x >= base_x + 3*offset and x < base_x + 4*offset:
        out_x = 'd'
        if y >= base_y and y < base_y + offset:
            out_y = '0'
        elif y >= base_y + offset and y < base_y + 2*offset:
            out_y = '1'
        elif y >= base_y + 2*offset and y < base_y + 3*offset:
            out_y = '2'
        elif y >= base_y + 3*offset and y <= base_y + 4*offset:
            out_y = '3'
    # Current piece
    elif x >= 862 and x < 1155 and y < 650:
        out_x = 'p'
        if y >= 321 and y < 601:
            out_y = '0'
    # Accept button
    elif x >= 842 and x < 842 + 375:
        out_x = 'bu'
        if y >= 674 and y < 650 + 125:
            out_y = '0'
            
    return (out_x, out_y)

def dropPos((x,y)):
    #Description:  Converts  coordinate form to normalized pixel form
    # for drawing shapes on the board
    #Pre:
    #Arguments:  (x,y) is in coordinate form
    #Returns: Coordinate form
    
    offset = 169
    base_x = 100 - 2
    base_y = 60 - 2
    drop_x = 0
    drop_y = 0
        
    if x == 'a':
        drop_x = base_x
        if y == '0':
            drop_y = base_y
        elif y == '1':
            drop_y = base_y + offset
        elif y == '2':
            drop_y = base_y + 2*offset
        elif y == '3':
            drop_y = base_y + 3*offset
        elif y == '-1':
            drop_y = -200
    elif x == 'b':
        drop_x = base_x + offset 
        if y == '0':
            drop_y = base_y
        elif y == '1':
            drop_y = base_y + offset 
        elif y == '2':
            drop_y = base_y + 2*offset
        elif y == '3':
            drop_y = base_y + 3*offset
        elif y == '-1':
            drop_y = -200
    elif x == 'c':
        drop_x = base_x + 2*offset
        if y == '0':
            drop_y = base_y
        elif y == '1':
            drop_y = base_y + offset
        elif y == '2':
            drop_y = base_y + 2*offset
        elif y == '3':
            drop_y = base_y + 3*offset
        elif y == '-1':
            drop_y = -200
    elif x == 'd':
        drop_x = base_x + 3*offset
        if y == '0':
            drop_y = base_y
        elif y == '1':
            drop_y = base_y + offset
        elif y == '2':
            drop_y = base_y + 2*offset
        elif y == '3':
            drop_y = base_y + 3*offset
        elif y == '-1':
            drop_y = -200
    elif x == 'p':
        drop_x = 940 - 15
        if y == '0':
            drop_y = 390 - 15
        else:
            drop_y = -200
    else:   #Render piece outside window
        drop_x = drop_y = -200

    return (drop_x, drop_y)
 
def drawImage(image, pos, surface):
    #Description: Draws an image to the selected surface
    #Pre:
    #Arguments: image is an image, position is in tuple form (x,y), surface
    # is a pygame surface object
    #Returns: 
    
    drawImage = image
    drawRec = pos
    surface.blit(drawImage, drawRec) 
        
def drawText(string, color, bg, (x,y)):
    #Description:  Draws text to game screen
    #Pre:
    #Arguments: string is a string, color and bg are three element integer tuple (r,g,b), 
    # (x,y) is in coordinate form
    #Returns:
    
    text = GAME_FONT.render(string, True, color, bg)
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    GameWindow.blit(text, textRect)
        
def drawDebug(debug):
    #Description: Draws debug information to game screen
    #Pre:
    #Arguments: debug is a boolean
    #Returns:

    if debug:
        #     getPos((Curs_x, Curs_y))
        Curs_x, Curs_y = pygame.mouse.get_pos()
        # Shape location info
        drawText( str(dropPos(getPos(pygame.mouse.get_pos()))), BLACK, WHITE, (400, WINDOW_HEIGHT-FONT_SIZE) )
        #Shape sprite test
        #drawImage(SHAPE_SHADOW_IMG, dropPos(getPos(pygame.mouse.get_pos())), GameWindow)
        #drawImage(blueShape[5].getSprite(), dropPos(getPos(pygame.mouse.get_pos())), GameWindow)
        # Boolean statuses
        drawText('shape_box_visible: ' + str(shape_box_visible), BLACK, WHITE, (150, 36))
        drawText('shape_placed: ' + str(shape_placed), BLACK, WHITE, (450, 36))
        drawText(str(masterClock), BLACK, WHITE, (100, 765))
        #Current shape stats
        drawText('curShape #: ' + str(curShape.getNum()), BLACK, WHITE, (1015, 550))
        drawText('curShape player: ' + str(curShape.getPlayer()), BLACK, WHITE, (1015, 565))
        drawText('Active: ' + str(curShape.isActive()), BLACK, WHITE, (1015, 580))
        drawText('Visible: ' + str(curShape.isVisible()), BLACK, WHITE, (1015, 595))
        drawText('BoardPos: ' + str(toBin(posToSpot(getPos(curShape.getPosition())), 16)), BLACK, WHITE, (1015, 610))
        #Mouse cursor info
        drawText(str(pygame.mouse.get_pos()), BLACK, WHITE, (Curs_x + 50, Curs_y + 30))
        drawText(str(getPos(pygame.mouse.get_pos())), BLACK, WHITE, (Curs_x + 50, Curs_y + 50))
        drawText(str(toBin(posToSpot(getPos(pygame.mouse.get_pos())), 16)), BLACK, WHITE, (Curs_x + 50, Curs_y + 70))

def drawAcceptButton((x, y)):
    #Description: Draws the accept button on the game screen
    #Pre:
    #Arguments: (x,y) is n coordinate form
    #Returns:
    
    _x = 818
    _y = 650
    if getPos((x,y)) != ('bu', '0'):
        if shape_placed:
            GameWindow.blit(ACCEPT_PRESSED_IMG, (_x, _y))
        else:
            GameWindow.blit(ACCEPT_STATIC_IMG, (_x, _y))
    else:
        if shape_placed:
            GameWindow.blit(ACCEPT_PRESSED_IMG, (_x, _y))
        else:
            GameWindow.blit(ACCEPT_STATIC_IMG, (_x, _y))
       
def DrawScreen():
    #Description: Draws all the graphics to the screen
    #Pre:
    #Arguments:
    #Returns:
    
    #Draw game background first
    GameWindow.blit(BG_IMG, (0,0))
    #Draw button
    drawAcceptButton((Curs_x, Curs_y))
    # Draw side bar information
    drawText('Master:    ' + toBin(masterBoard.getBoard(), 16), BLACK, WHITE ,(1020, 625))
    drawText('Red:       ' + toBin(redBoard.getBoard(), 16), BLACK, WHITE, (1020, 625 + 27 - 10))
    drawText('Blue:      ' + toBin(blueBoard.getBoard(), 16), BLACK, WHITE, (1020, 625 + 2*27 - 2*10))
    #Draw shapes
    for i in range(6):
        if redShape[i].isVisible():
            GameWindow.blit(SHAPE_SHADOW_IMG, redShape[i].getPosition())
            GameWindow.blit(redShape[i].getSprite(), redShape[i].getPosition())
        if blueShape[i].isVisible():
            GameWindow.blit(SHAPE_SHADOW_IMG, blueShape[i].getPosition())
            GameWindow.blit(blueShape[i].getSprite(), blueShape[i].getPosition())

    #Draw draggable shape
    if shape_box_visible:
        GameWindow.blit(SHAPE_SHADOW_IMG, (940 - 15, 390 - 15))
        GameWindow.blit(curShape.getSprite(), (940 - 15, 390 - 15))
    elif not shape_placed:  #Draw curShape at cursor
        GameWindow.blit(SHAPE_SHADOWLARGE_IMG, (Curs_x - 175, Curs_y - 175))
        GameWindow.blit(curShape.getSprite(), (Curs_x - 175/2, Curs_y - 175/2))
    #else curShape is not drawn

#####################################################################  
# Pygame and graphics
#####################################################################  
  
# Initialize Pygame    
pygame.init()

# Cursor position
Curs_x = 0 
Curs_y = 0  

# Window constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Background plate
BG_FILENAME = 'BG_plate2.bmp'
BG_IMG = pygame.image.load(os.path.join('Board', BG_FILENAME))

# Splash / Credit Screen
SPLASH_SCREEN_FILE = 'SplashScreen.png'
CREDIT_SCREEN_FILE = 'Credits.png'
GREY_FILE = '20Grey.png'
SPLASH_SCREEN_IMG = pygame.image.load(os.path.join('Other', SPLASH_SCREEN_FILE))
CREDIT_SCREEN_IMG = pygame.image.load(os.path.join('Other', CREDIT_SCREEN_FILE))
GREY_OUT_IMG = pygame.image.load(os.path.join('Other', GREY_FILE))

# Default Font
FONT_SIZE = 14
FONT = 'menlo'
GAME_FONT = pygame.font.SysFont(FONT, FONT_SIZE)

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game Clock
masterClock = pygame.time.Clock()

# Setup game window and graphics
GameWindow = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Pyaera by #_0b0101")
GameWindow.fill(BLACK)

# Load Sounds
SND_HIT_FILE = 'Hard_Hit.wav'
SND_WIN_FILE = 'Cheering.wav'
SND_PLACE_FILE = 'PlaceShape.wav'
SND_ACCEPT_FILE = 'Accept.wav'
SND_HIT = pygame.mixer.Sound(os.path.join('Sounds', SND_HIT_FILE))
SND_WIN = pygame.mixer.Sound(os.path.join('Sounds', SND_WIN_FILE))
SND_PLACE = pygame.mixer.Sound(os.path.join('Sounds', SND_PLACE_FILE))
SND_ACCEPT = pygame.mixer.Sound(os.path.join('Sounds', SND_ACCEPT_FILE))
# Music
BG_MUSIC_FILE = 'DXBall.ogg'
BG_MUISC = pygame.mixer.music.load(os.path.join('Sounds', BG_MUSIC_FILE))

# Load images
## Shape
### Image size is 150x150
for i in range(6):
    sprite = pygame.image.load(os.path.join('Shapes', 'Red_Shape_' + str(i)) + '.png').convert_alpha()
    redShape[i].setSprite(sprite)
    
    sprite = pygame.image.load(os.path.join('Shapes', 'Blue_Shape_' + str(i)) + '.png').convert_alpha()
    blueShape[i].setSprite(sprite)
# Shadows
SHAPE_SHADOW_FILE = 'Shadow.png'
SHAPE_SHADOWLARGE_FILE = 'Shadow_Large.png' 
SHAPE_SHADOW_IMG = pygame.image.load(os.path.join('Shapes', SHAPE_SHADOW_FILE)).convert_alpha()
SHAPE_SHADOWLARGE_IMG = pygame.image.load(os.path.join('Shapes', SHAPE_SHADOWLARGE_FILE)).convert_alpha() # 350x350

# Accept Button
ACCEPT_PRESSED_FILE = 'Accept_pressed.bmp'
ACCEPT_STATIC_FILE = 'Accept_static.bmp'
ACCEPT_PRESSED_IMG = pygame.image.load(os.path.join('board', ACCEPT_PRESSED_FILE))
ACCEPT_STATIC_IMG = pygame.image.load(os.path.join('board', ACCEPT_STATIC_FILE))

#####################################################################
#####################################################################
# For splash screen loop
splash_screen_visible = True
# Splash Screen Loop
while splash_screen_visible:
    GameWindow.blit(SPLASH_SCREEN_IMG, (-1,57))
    for event in pygame.event.get():
        if event.type is MOUSEBUTTONDOWN:
            splash_screen_visible = False
    pygame.display.update()

# Start Music
## MUST BE OUTSIDE EVENT LOOP
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(.2)
#####################################################################
# Event loop
while True:

    # Draw functions
    DrawScreen()
    drawDebug(debug_mode)
    # Update each loop
    Curs_x, Curs_y = pygame.mouse.get_pos()
    CurPos_x, CurPos_y = curShape.getPosition()
    
    # Get events
    for event in pygame.event.get():

        # Click (x) on window
        if event.type is QUIT:
            pygame.quit()
            sys.exit()
        
        # Upclick
        if event.type is MOUSEBUTTONUP: 
            
            # Click on the Accept button
            if getPos(pygame.mouse.get_pos()) == ('bu','0'):
                if not shape_box_visible:
                    curShape = AcceptTurn(curShape)
                    SND_ACCEPT.play()
                    shape_placed = False 
                    
            # Shape was being click-dragged
            if not shape_box_visible and not shape_placed:   #Shape being dragged
                if isSpotOpen(posToSpot(getPos(pygame.mouse.get_pos()))):
                    PlaceShape(curShape, getPos(pygame.mouse.get_pos()))
                    SND_PLACE.play()
                    shape_box_visible = False 
                    shape_placed = True 
                else: # shape was placed
                    shape_box_visible = True
                    
        # Downclick    
        if event.type is MOUSEBUTTONDOWN:
            
            #Click on the shape box
            if getPos(pygame.mouse.get_pos()) == ('p','0'):
                if not shape_placed:
                    shape_box_visible = False #shape being dragged
                    
            # Click on placed shape, that hasn't been accepted
            if getPos(pygame.mouse.get_pos()) == getPos((CurPos_x + 10, CurPos_y + 10)):
                if not shape_box_visible:
                    curShape.setVisible(False)
                    shape_box_visible = False
                    shape_placed = False    # Place again
            
        # Press q     
        if event.type is KEYDOWN and event.key is pygame.K_q:
            pygame.quit()
            sys.exit()
            
        # Press d - DEBUG mode
        if event.type is KEYDOWN and event.key is pygame.K_d:
            if debug_mode:
                debug_mode = False
            else: 
                debug_mode = True
                
        # Press a - Accept Turn DEBUG mode only
        if event.type is KEYDOWN and event.key is pygame.K_a:
            if not shape_box_visible and debug_mode:
                curShape = AcceptTurn(curShape)
                shape_placed = False 
    
    if isSolved():
        SND_WIN.play()
    while isSolved():
        GameWindow.blit(GREY_OUT_IMG, (0,0))
        GameWindow.blit(CREDIT_SCREEN_IMG, (149,50))
        pygame.mixer.music.pause()
        for newEvent in pygame.event.get():
            if newEvent.type is MOUSEBUTTONDOWN:
                pygame.mixer.music.unpause()
                Reset()
        pygame.display.update()
        
    # Refresh graphics and masterClock  
    pygame.display.update()
    masterClock.tick(30)     
